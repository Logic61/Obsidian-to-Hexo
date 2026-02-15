import os
import re

# --- 配置区 ---
MD_DIR = r'C:\Users\32372\myblog\source\_posts'

def wrap_block_math_with_p():
    print("正在为块状公式添加 <p> 包装，并确保完全分行...")
    
    for root, dirs, files in os.walk(MD_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 1. 彻底清除之前产生的所有碎片化标签（<p>, </p>, <div> 等）
                    # 确保从干净的 Markdown 开始
                    content = re.sub(r'</?(p|div|span).*?>', '', content)

                    # 2. 规范化所有 $$ 符号，去掉前后可能多出的多余空格
                    content = re.sub(r'\$\$\s+', '$$', content)
                    content = re.sub(r'\s+\$\$', '$$', content)

                    # 3. 核心逻辑：精准匹配块状公式并包装
                    def reformat_block(match):
                        formula = match.group(1).strip()
                        # 构造 5 行结构：
                        # <p>
                        # $$
                        # 内容
                        # $$
                        # </p>
                        return f'\n\n<p>\n$$\n{formula}\n$$\n</p>\n\n'

                    # 匹配所有 $$...$$ 块
                    content = re.sub(r'\$\$(.*?)\$\$', reformat_block, content, flags=re.DOTALL)

                    # 4. 辅助修复：顺便修复行内公式 $...$ 内部的空格（防止脱节）
                    content = re.sub(r'(?<!\$)\$\s+([^\$\n]+?)\s+\$(?!\$)', r'$\1$', content)

                    # 5. 压缩多余空行，保持 MD 整洁
                    content = re.sub(r'\n{3,}', '\n\n', content)

                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f" 格式对齐完成: {file}")
                except Exception as e:
                    print(f" 修复 {file} 时出错: {e}")

if __name__ == "__main__":
    wrap_block_math_with_p()