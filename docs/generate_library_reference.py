import os
import mkdocs_gen_files


module = "virus_total_telegram_bot"
library_path = "reference/library.md"
excluded_from_documentation = ["__init__.py", "_meta.py"]


def add_tittle_and_warning(file):
    print("# Library\n", file=file)
    print("???+ warning\n\tThis page is meant to be autogenerated from code. Do not edit it manually.", file=file)


def get_files_to_document():
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(module):
        for file in f:
            if file.endswith(".py") and file not in excluded_from_documentation:
                file_path = os.path.join(r, file)
                file_path = file_path.replace(".py", "").replace("/", ".")
                files.append(file_path)
    return files

files = get_files_to_document()

with mkdocs_gen_files.open(library_path, "w") as file:
    add_tittle_and_warning(file)
    for file_to_documentation in files:
        print(f"::: {file_to_documentation}", file=file)
