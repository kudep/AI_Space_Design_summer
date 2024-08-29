import numpy
import trimesh
import trimesh.sample
import trimesh.visual
import trimesh.proximity
import objaverse
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plotlib


def get_bytes(x: str):
    import io, requests
    return io.BytesIO(requests.get(x).content)


def get_image(x: str):
    try:
        return plotlib.imread(get_bytes(x), 'auto')
    except Exception:
        raise ValueError("Invalid image", x)


def model_to_pc(mesh: trimesh.Trimesh, n_sample_points=10000):
    f32 = numpy.float32
    rad = numpy.sqrt(mesh.area / (3 * n_sample_points))
    for _ in range(24):
        pcd, face_idx = trimesh.sample.sample_surface_even(mesh, n_sample_points, rad)
        rad *= 0.85
        if len(pcd) == n_sample_points:
            break
    else:
        raise ValueError("Bad geometry, cannot finish sampling.", mesh.area)
    if isinstance(mesh.visual, trimesh.visual.ColorVisuals):
        rgba = mesh.visual.face_colors[face_idx]
    elif isinstance(mesh.visual, trimesh.visual.TextureVisuals):
        bc = trimesh.proximity.points_to_barycentric(mesh.triangles[face_idx], pcd)
        if mesh.visual.uv is None or len(mesh.visual.uv) < mesh.faces[face_idx].max():
            uv = numpy.zeros([len(bc), 2])
            st.warning("Invalid UV, filling with zeroes")
        else:
            uv = numpy.einsum('ntc,nt->nc', mesh.visual.uv[mesh.faces[face_idx]], bc)
        material = mesh.visual.material
        if hasattr(material, 'materials'):
            if len(material.materials) == 0:
                rgba = numpy.ones_like(pcd) * 0.8
                texture = None
                st.warning("Empty MultiMaterial found, falling back to light grey")
            else:
                material = material.materials[0]
        if hasattr(material, 'image'):
            texture = material.image
            if texture is None:
                rgba = numpy.zeros([len(uv), len(material.main_color)]) + material.main_color
        elif hasattr(material, 'baseColorTexture'):
            texture = material.baseColorTexture
            if texture is None:
                rgba = numpy.zeros([len(uv), len(material.main_color)]) + material.main_color
        else:
            texture = None
            rgba = numpy.ones_like(pcd) * 0.8
            st.warning("Unknown material, falling back to light grey")
        if texture is not None:
            rgba = trimesh.visual.uv_to_interpolated_color(uv, texture)
    if rgba.max() > 1:
        if rgba.max() > 255:
            rgba = rgba.astype(f32) / rgba.max()
        else:
            rgba = rgba.astype(f32) / 255.0
    return numpy.concatenate([numpy.array(pcd, f32), numpy.array(rgba, f32)[:, :3]], axis=-1)


def trimesh_to_pc(scene_or_mesh):
    if isinstance(scene_or_mesh, trimesh.Scene):
        meshes = []
        for node_name in scene_or_mesh.graph.nodes_geometry:
            # which geometry does this node refer to
            transform, geometry_name = scene_or_mesh.graph[node_name]

            # get the actual potential mesh instance
            geometry = scene_or_mesh.geometry[geometry_name].copy()
            if not hasattr(geometry, 'triangles'):
                continue
            geometry: trimesh.Trimesh
            geometry = geometry.apply_transform(transform)
            meshes.append(geometry)
        total_area = sum(geometry.area for geometry in meshes)
        if total_area < 1e-6:
            raise ValueError("Bad geometry: total area too small (< 1e-6)")
        pcs = []
        for geometry in meshes:
            pcs.append(model_to_pc(geometry, max(1, round(geometry.area / total_area * 10000))))
        if not len(pcs):
            raise ValueError("Unsupported mesh object: no triangles found")
        return numpy.concatenate(pcs)
    else:
        assert isinstance(scene_or_mesh, trimesh.Trimesh)
        return model_to_pc(scene_or_mesh, 10000)


def input_3d_shape(key=None):
    if key is None:
        objaid_key = model_key = npy_key = swap_key = None
    else:
        objaid_key = key + "_objaid"
        model_key = key + "_model"
        npy_key = key + "_npy"
        swap_key = key + "_swap"
    objaid = st.text_input("Enter an Objaverse ID", key=objaid_key)
    model = st.file_uploader("Or upload a model (.glb/.obj/.ply)", key=model_key)
    npy = st.file_uploader("Or upload a point cloud numpy array (.npy of Nx3 XYZ or Nx6 XYZRGB)", key=npy_key)
    swap_yz_axes = st.radio("Gravity", ["Y is up (for most Objaverse shapes)", "Z is up"], key=swap_key) == "Z is up"
    f32 = numpy.float32

    def load_data(prog):
        # load the model
        prog.progress(0.05, "Preparing Point Cloud")
        if npy is not None:
            pc: numpy.ndarray = numpy.load(npy)
        elif model is not None:
            pc = trimesh_to_pc(trimesh.load(model, model.name.split(".")[-1]))
        elif objaid:
            prog.progress(0.1, "Downloading Objaverse Object")
            objamodel = objaverse.load_objects([objaid])[objaid]
            prog.progress(0.2, "Preparing Point Cloud")
            pc = trimesh_to_pc(trimesh.load(objamodel))
        else:
            raise ValueError("You have to supply 3D input!")
        prog.progress(0.25, "Preprocessing Point Cloud")
        assert pc.ndim == 2, "invalid pc shape: ndim = %d != 2" % pc.ndim
        assert pc.shape[1] in [3, 6], "invalid pc shape: should have 3/6 channels, got %d" % pc.shape[1]
        pc = pc.astype(f32)
        if swap_yz_axes:
            pc[:, [1, 2]] = pc[:, [2, 1]]
        pc[:, :3] = pc[:, :3] - numpy.mean(pc[:, :3], axis=0)
        pc[:, :3] = pc[:, :3] / numpy.linalg.norm(pc[:, :3], axis=-1).max()
        if pc.shape[1] == 3:
            pc = numpy.concatenate([pc, numpy.ones_like(pc) * 0.4], axis=-1)
        prog.progress(0.27, "Normalized Point Cloud")
        if pc.shape[0] >= 10000:
            pc = pc[numpy.random.permutation(len(pc))[:10000]]
        elif pc.shape[0] == 0:
            raise ValueError("Got empty point cloud!")
        elif pc.shape[0] < 10000:
            pc = numpy.concatenate([pc, pc[numpy.random.randint(len(pc), size=[10000 - len(pc)])]])
        prog.progress(0.3, "Preprocessed Point Cloud")
        return pc.astype(f32)

    return load_data


def render_pc(pc):
    rand = numpy.random.permutation(len(pc))[:2048]
    pc = pc[rand]
    rgb = (pc[:, 3:] * 255).astype(numpy.uint8)
    g = go.Scatter3d(
        x=pc[:, 0], y=pc[:, 1], z=pc[:, 2],
        mode='markers',
        marker=dict(size=2, color=[f'rgb({rgb[i, 0]}, {rgb[i, 1]}, {rgb[i, 2]})' for i in range(len(pc))]),
    )
    fig = go.Figure(data=[g])
    fig.update_layout(scene_camera=dict(up=dict(x=0, y=1, z=0)))
    fig.update_scenes(aspectmode="data")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig, use_container_width=True)
        # st.caption("Point Cloud Preview")
    return col2
