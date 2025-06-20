import os

# 设置根目录和输出文件名
root_dir = os.getcwd()
output_file = "merged_project.txt"

# 设定可接受的文件扩展名
include_ext = {".py", ".md", ".toml", ".txt", ".json", ".html", ".js", ".ts", ".vue",
               ".scss", ".lock"}

with open(output_file, "w", encoding="utf-8") as outfile:
    for folder, _, files in os.walk(root_dir):
        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext.lower() in include_ext:
                filepath = os.path.join(folder, filename)
                rel_path = os.path.relpath(filepath, root_dir)
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        outfile.write(f"\n\n#########################################################\n")
                        outfile.write(f"# 文件路径: ./{rel_path}\n")
                        outfile.write(content)
                except Exception as e:
                    print(f"跳过文件 {rel_path}: {e}")
