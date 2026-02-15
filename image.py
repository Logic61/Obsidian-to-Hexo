import os
import io
import sys
import re

# 强制标准输出使用 utf-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- 配置项 ---
# 请确保这两个路径正确
POSTS_DIR = r'C:\Users\32372\myBlog\source\_posts' 
IMAGES_DIR = r'C:\Users\32372\myBlog\source\images'

# 使用绝对根路径 /images/，兼容性最强
IMAGE_TARGET_PREFIX = '/images/'

def integrated_fix():
    # 1. 处理图片文件本身的空格问题
    print("🚚 正在重命名图片文件（空格 -> 下划线）...")
    if os.path.exists(IMAGES_DIR):
        for filename in os.listdir(IMAGES_DIR):
            if ' ' in filename:
                old_path = os.path.join(IMAGES_DIR, filename)
                new_filename = filename.replace(' ', '_')
                new_path = os.path.join(IMAGES_DIR, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f"  [重命名] {filename} -> {new_filename}")
                except Exception as e:
                    print(f"  ❌ 无法重命名 {filename}: {e}")
    else:
        print(f"  ❌ 警告：未找到图片目录 {IMAGES_DIR}")

    # 2. 处理 Markdown 内容
    print("\n📝 正在转换语法并修复链接...")
    processed_files = 0
    total_replacements = 0

    # 正则1: 匹配 ![[文件名.png]]
    OBSIDIAN_PATTERN = r'!\[\[(.*?)\]\]'
    # 正则2: 匹配已经转换过的 ![]() 里的空格（防止重复运行脚本时漏掉）
    MD_LINK_PATTERN = r'!\[\]\((.*?)\)'

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.lower().endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    
                    # 先把 ![[文件名.png]] 替换为 ![](/images/文件名_下划线.png)
                    obs_matches = re.findall(OBSIDIAN_PATTERN, content)
                    for match in obs_matches:
                        clean_name = match.replace(' ', '_')
                        old_syntax = f'![[{match}]]'
                        new_syntax = f'![]({IMAGE_TARGET_PREFIX}{clean_name})'
                        new_content = new_content.replace(old_syntax, new_syntax)
                        total_replacements += 1

                    # 再检查已经存在的 ![]() 语法，修复其中的空格和路径层级
                    md_matches = re.findall(MD_LINK_PATTERN, new_content)
                    for link in md_matches:
                        if ' ' in link or '../' in link or 'C:\\' in link:
                            # 提取文件名（取最后一段）
                            file_name_only = os.path.basename(link).replace(' ', '_')
                            new_link = f'{IMAGE_TARGET_PREFIX}{file_name_only}'
                            new_content = new_content.replace(f'({link})', f'({new_link})')
                            total_replacements += 1

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"  ✅ 已修复: {file}")
                        processed_files += 1
                        
                except Exception as e:
                    print(f"  ❌ 处理文件 {file} 出错: {e}")

    print(f"\n" + "="*20)
    print(f" 🎉 任务完成！")
    print(f" 修改文件数: {processed_files}")
    print(f" 总替换次数: {total_replacements}")
    print(f" 提示: 现在图片路径应统一为 /images/文件名_下划线.png")
    print("="*20)

if __name__ == "__main__":
    integrated_fix()