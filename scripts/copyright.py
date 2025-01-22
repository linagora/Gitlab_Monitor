# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
"""
Run this script to add or replace the copyright notice of all file of this project.
Only for files with one of those extension : ".py", ".yaml", ".yml", ".toml", ".sh".
"""

import os
import re

COPYRIGHT_NOTICE = """
# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
"""
EXCLUDED_FILES = ["copyright.py"]


def add_or_replace_copyright(file_path):
    with open(file_path, "r+") as file:
        content = file.read()
        content = re.sub(r"(?m)^# # --- Copyright.*?\n(?:# # .*\n){3}", "", content)
        file.seek(0, 0)
        file.write(COPYRIGHT_NOTICE + content)
        file.truncate()


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                file.endswith((".py", ".yaml", ".yml", ".toml", ".sh"))
                and file not in EXCLUDED_FILES
            ):
                file_path = os.path.join(root, file)
                add_or_replace_copyright(file_path)


if __name__ == "__main__":
    process_directory("../.")
