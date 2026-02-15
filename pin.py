import os
import re

# ================= 配置区 =================
# 在这个列表里添加你想处理的所有目录路径
TARGET_DIRS = [
    r'C:\Users\32372\myBlog\source\_posts\离散',
    r'C:\Users\32372\myBlog\source\_posts\数学随笔'  # 替换为你的第二个目录
]

NEW_FIELD = "pinned: 10"
# ==========================================

def update_yaml_pinned(file_path):
    """更新单个文件的 YAML 头部"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 YAML Front-matter
        yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
        match = yaml_pattern.search(content)

        if match:
            yaml_content = match.group(1)
            body_content = content[match.end():]
            
            # 如果已有 pinned，正则替换整个 key-value
            if 'pinned:' in yaml_content:
                new_yaml_content = re.sub(r'pinned:\s*.*', NEW_FIELD, yaml_content)
            else:
                # 如果没有，在末尾追加
                new_yaml_content = yaml_content.rstrip() + f"\n{NEW_FIELD}"
            
            new_file_content = f"---\n{new_yaml_content}\n---{body_content}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_file_content)
            return True
        return False
    except Exception as e:
        print(f"处理 {file_path} 时出错: {e}")
        return False

def run():
    total_count = 0
    
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            print(f" 跳过：找不到目录 {target_dir}")
            continue

        print(f"正在扫描目录: {target_dir}")
        dir_count = 0
        
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith('.md'):
                    file_path = os.path.join(root, file)
                    if update_yaml_pinned(file_path):
                        dir_count += 1
        
        print(f" 该目录处理完成，共修改 {dir_count} 个文件。\n")
        total_count += dir_count
    
    print(f" 全部任务完成！累计处理 {total_count} 个文件。")

if __name__ == "__main__":
    run()