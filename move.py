import os
import shutil
import subprocess
import datetime
import re  # 引入正则，提取日期更精准

# ================= 配置区 =================
SOURCE_DIR = r'C:\Users\32372\Documents\Obsidian Vault'
HEXO_DIR = r'C:\Users\32372\myBlog'
IMAGE_DIR = os.path.join(HEXO_DIR, 'source', 'images')
EXCLUDE_DIRS = {'trash bin', '.trash', '.obsidian'} 
# ==========================================

def run():
    target_posts = os.path.join(HEXO_DIR, 'source', '_posts')
    os.makedirs(target_posts, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    print("Step 1: 正在分类同步文件 (MD -> _posts, Images -> images)...")
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDE_DIRS]
        
        for file in files:
            source_path = os.path.join(root, file)
            file_lower = file.lower()

            if file in ['move.py', 'workspace.json']:
                continue

            # --- 情况 A: 处理 Markdown 文件 ---
            if file_lower.endswith('.md'):
                rel_path = os.path.relpath(source_path, SOURCE_DIR)
                target_path = os.path.join(target_posts, rel_path)
                
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # 【修改点】：先提取旧日期，再执行拷贝
                existing_date = get_existing_date(target_path)
                
                shutil.copy2(source_path, target_path)
                
                # 【修改点】：传入旧日期，防止被覆盖
                check_and_fix_yaml(target_path, existing_date)
                print(f"已同步文章: {file}")

            # --- 情况 B: 处理图片文件 ---
            elif file_lower.endswith(image_extensions):
                target_path = os.path.join(IMAGE_DIR, file)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(source_path, target_path)

    print("\nStep 2: 执行 Hexo 部署...")
    # ... 剩下的部署逻辑保持不变 ...
    try:
        subprocess.run("hexo clean && hexo g -d", shell=True, cwd=HEXO_DIR)
        print("\n 同步并部署成功！")
    except Exception as e:
        print(f"部署出错: {e}")
    
    # 保持后续脚本调用
    for script in ["revise.py", "pin.py", "cate.py", "more.py", "image.py"]:
        if os.path.exists(script):
            subprocess.run(["python", script])

def get_existing_date(file_path):
    """尝试从现有的 Hexo 文章中读取 date 字段"""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用正则匹配 date: 2023-01-01 12:00:00 这种格式
            match = re.search(r'^date:\s*(.*)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except:
        pass
    return None

def check_and_fix_yaml(file_path, preserved_date=None):
    """自动补全 Front-matter，优先使用传入的旧日期"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果没有 YAML 头
        if not content.strip().startswith('---'):
            title = os.path.basename(file_path).replace('.md', '')
            # 优先级：旧文章日期 > 当前时间
            date_str = preserved_date if preserved_date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_content = f"---\ntitle: \"{title}\"\ndate: {date_str}\n---\n\n{content}"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            # 如果已有 YAML 头但你想强制保持日期不被 Obsidian 的空头覆盖
            # 可以在这里增加逻辑。但通常 Obsidian 只要带了 --- 就能保护住。
            pass
    except:
        pass

if __name__ == "__main__":
    run()