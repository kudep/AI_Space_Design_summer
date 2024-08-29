import setuptools


def packages():
    return setuptools.find_packages()


setuptools.setup(
    name="openshape",
    version="0.1",
    author="flandre.info",
    author_email="flandre@scarletx.cn",
    description="Support library for OpenShape Demos.",
    packages=packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=3.7',
)
