### Настройка Python для Windows и Linux

#### Установка Python на Windows

1. **Скачайте установочный файл Python**:
    - Перейдите на официальный сайт Python: [python.org](https://www.python.org/).
    - Перейдите в раздел "Downloads" и выберите последнюю версию для Windows.
    - Скачайте установочный файл.

2. **Установите Python**:
    - Запустите скачанный установочный файл.
    - В окне установки убедитесь, что установлена галочка "Add Python to PATH".
    - Выберите "Install Now" или "Customize installation" для более подробной настройки.
    - Дождитесь завершения установки.

3. **Проверьте установку**:
    - Откройте командную строку (Windows + R, введите "cmd" и нажмите Enter).
    - Введите `python --version` и `pip --version` для проверки успешной установки Python и пакетного менеджера pip.

4. **Установка Jupyter Notebook** (опционально):
    - В командной строке выполните команду `pip install notebook`.
    - После установки запустите Jupyter Notebook командой `jupyter notebook`.

#### Установка Python на Linux

1. **Проверьте установлен ли Python**:
    - Откройте терминал.
    - Введите `python3 --version` для проверки наличия установленной версии Python 3.

2. **Установите Python (если не установлен)**:
    - В зависимости от дистрибутива используйте следующие команды:
      - **Debian/Ubuntu**:
        ```bash
        sudo apt update
        sudo apt install python3 python3-pip
        ```
      - **Fedora**:
        ```bash
        sudo dnf install python3 python3-pip
        ```
      - **Arch Linux**:
        ```bash
        sudo pacman -S python python-pip
        ```

3. **Проверьте установку**:
    - Введите в терминале `python3 --version` и `pip3 --version` для проверки успешной установки Python и пакетного менеджера pip.

4. **Установка Jupyter Notebook** (опционально):
    - В терминале выполните команду `pip3 install notebook`.
    - После установки запустите Jupyter Notebook командой `jupyter notebook`.

### Запуск Jupyter Notebook и установка библиотек

1. **Запуск Jupyter Notebook**:
    - В командной строке (Windows) или терминале (Linux) введите `jupyter notebook`.
    - Откроется веб-браузер с интерфейсом Jupyter Notebook.

2. **Создание нового блокнота**:
    - В интерфейсе Jupyter Notebook выберите "New" и затем "Python 3" для создания нового блокнота.

3. **Установка необходимых библиотек**:
    - В новой ячейке блокнота введите команду для установки библиотеки OpenAI:
      ```python
      !pip install openai
      ```
    - Выполните ячейку, чтобы установить библиотеку.

### Пример использования OpenAI в Jupyter Notebook

1. **Откройте новый блокнот** и выполните следующие шаги:

    ```python
    from openai import OpenAI

    API_KEY = "ваш_ключ_здесь"

    client = OpenAI(
        api_key=API_KEY,
        base_url="http://193.187.173.33:8002/api/providers/openai/v1",
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}],
    )

    print(completion.choices[0].message)
    ```

2. **Запустите ячейку**, чтобы получить ответ от модели OpenAI.
