
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
import os
import re

# Be careful the following string is gonna be erased during this script execution
# So if you want to keep it, you should add it again at the end of the execution
COPYRIGHT_NOTICE = """
# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com
"""

def add_or_replace_copyright(file_path):
    with open(file_path, 'r+') as file:
        content = file.read()
        content = re.sub(r'(?m)^# # --- Copyright.*?\n(?:# # .*\n){3}', '', content)
        file.seek(0, 0)
        file.write(COPYRIGHT_NOTICE + content)
        file.truncate()

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.yaml', '.yml', '.toml')):
                file_path = os.path.join(root, file)
                add_or_replace_copyright(file_path)

if __name__ == "__main__":
    process_directory('.')