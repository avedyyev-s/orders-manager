import os

# Получаем папку, где лежит сам скрипт (others), и её родителя (корень проекта)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

def get_priority(file_name):
    if file_name == "main.py":
        return 1
    return 2

# Читаем файлы из корня проекта
files = os.listdir(project_root)
files.sort(key=get_priority)

# Сохраняем результат в папку со скриптом
output_path = os.path.join(script_dir, "context_all.txt")

with open(output_path, "w", encoding="utf-8") as outfile:
    for file in files:
        full_path = os.path.join(project_root, file)
        if os.path.isfile(full_path) and file.endswith(".py") and file != os.path.basename(__file__):
            with open(full_path, "r", encoding="utf-8") as infile:
                text = infile.read()
                outfile.write(f"\n\n======= ФАЙЛ: {file} =======\n")
                outfile.write(text)
