import os
import re

# ================= 配置区 =================
# 在这里填入你想要处理的目录列表
TARGET_DIRS = [
    r'C:\Users\32372\myBlog\source\_posts\离散',
    r'C:\Users\32372\myBlog\source\_posts\数学随笔'  # 替换为你的第二个目录
]

# 预设的标签名
DEFAULT_TAG = "数学"
# ==========================================

def update_markdown_yaml(file_path, category_name):
    try:
        # 使用 utf-8-sig 兼容带 BOM 的文件
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()

        # 正则匹配 YAML 头部
        yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
        match = yaml_pattern.search(content)

        if match:
            yaml_content = match.group(1)
            body_content = content[match.end():]
            
            # --- 处理 categories ---
            # 如果已存在 categories 字段则更新，否则追加
            if 'categories:' in yaml_content:
                yaml_content = re.sub(r'categories:.*', f'categories: [{category_name}]', yaml_content)
            else:
                yaml_content = yaml_content.rstrip() + f'\ncategories: [{category_name}]'

            # --- 处理 tags ---
            if 'tags:' in yaml_content:
                # 这里为了稳妥，如果原本有标签，可以决定是覆盖还是追加
                # 下面是覆盖为 "数学" 的逻辑，如果需要追加请告知
                yaml_content = re.sub(r'tags:.*', f'tags: [{DEFAULT_TAG}]', yaml_content)
            else:
                yaml_content = yaml_content.rstrip() + f'\ntags: [{DEFAULT_TAG}]'
            
            # 重新拼合
            new_content = f"---\n{yaml_content.strip()}\n---{body_content}"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def run():
    total_count = 0
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            print(f"Directory not found: {target_dir}")
            continue

        print(f"Processing directory: {target_dir}")
        dir_count = 0
        
        # os.walk 会遍历所有子目录
        for root, _, files in os.walk(target_dir):
            # 获取当前文件夹的名字作为分类名
            category_name = os.path.basename(root)
            # 如果根目录就是 _posts，分类名可能不合适，可以根据需要微调
            if category_name == "_posts":
                category_name = "未分类"

            for file in files:
                if file.lower().endswith('.md'):
                    file_path = os.path.join(root, file)
                    if update_markdown_yaml(file_path, category_name):
                        dir_count += 1
        
        print(f"Finished. Updated {dir_count} files in this directory.")
        total_count += dir_count
    
    print(f"\nAll tasks completed. Total modified: {total_count}")

if __name__ == "__main__":
    run()