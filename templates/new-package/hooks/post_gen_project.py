import os
import shutil

source_dir = os.getcwd()
target_dir = "{{ cookiecutter.__final_destination }}"

print(f"mv source_dir=[{source_dir}] to target_dir=[{target_dir}]")
shutil.move(source_dir, target_dir)
