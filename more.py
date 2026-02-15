import os

# 目标目录
target_dirs = [
    r'C:\Users\32372\myBlog\source\_posts\离散',
    r'C:\Users\32372\myBlog\source\_posts\数学随笔'
]

def fix_and_add_more(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_yaml_section = []
    content_lines = []
    
    yaml_boundary_indices = [i for i, line in enumerate(lines) if line.strip() == '---']
    
    # 确保文件至少有两个 --- 构成 YAML 区
    if len(yaml_boundary_indices) >= 2:
        start, end = yaml_boundary_indices[0], yaml_boundary_indices[1]
        
        # 处理 YAML 区域并去重
        seen_keys = set()
        new_yaml_section.append(lines[start]) # 第一个 ---
        
        for i in range(start + 1, end):
            line = lines[i]
            if ':' in line:
                key = line.split(':')[0].strip()
                if key in seen_keys:
                    continue # 跳过重复的 key
                seen_keys.add(key)
            new_yaml_section.append(line)
            
        new_yaml_section.append(lines[end]) # 第二个 ---
        content_lines = lines[end + 1:] # 获取剩下的正文
    else:
        # 如果没有规范的 YAML 区，直接当作全文处理
        content_lines = lines

    # 将正文转为字符串用于检查是否已存在标签
    full_content_str = "".join(content_lines)
    
    # 如果已经有 more 标签，就不再插入，但依然会修复 YAML 报错
    if "<!-- more -->" not in full_content_str:
        first_para_end = -1
        in_para = False
        
        for i, line in enumerate(content_lines):
            # 找到第一个非空行作为段落起始
            if line.strip() and not in_para:
                in_para = True
            # 在段落开始后遇到的第一个空行作为段落结束
            elif in_para and not line.strip():
                first_para_end = i
                break
        
        if first_para_end != -1:
            content_lines.insert(first_para_end, "\n<!-- more -->\n")
        elif in_para:
            # 如果全文就一段话没有空行，加在最后
            content_lines.append("\n\n")

    # 合并 YAML 和正文并写回
    final_output = new_yaml_section + content_lines
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(final_output)
    print(f"Successfully processed: {file_path}")

def main():
    for directory in target_dirs:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    fix_and_add_more(os.path.join(root, file))

if __name__ == "__main__":
    main()