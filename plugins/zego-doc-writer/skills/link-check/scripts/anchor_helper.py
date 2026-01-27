"""
检验锚点是否有效或者生成锚点。
"""

import re
import os
import sys
from typing import List, Tuple, Optional


def slugify(text: str) -> str:
    """
    将文本转换为锚点格式。
    规则：转小写，移除特殊字符，空格转连字符
    """
    # 转小写
    text = text.lower()
    # 移除特殊字符，只保留字母数字和连字符/空格
    text = re.sub(r'[^\w\s-]', '', text)
    # 空格和下划线转连字符
    text = re.sub(r'[\s_]+', '-', text)
    # 移除首尾的连字符
    text = text.strip('-')
    return text


def extract_headings_with_anchors(content: str) -> List[Tuple[str, str, int]]:
    """
    提取所有标题及其对应的锚点。
    返回: [(标题文本, 锚点, 行号), ...]
    """
    headings = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]
        # 匹配 markdown 标题
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            # 提取标题文本（去掉行内可能存在的锚点标签）
            title_with_anchor = match.group(2).strip()
            title = re.sub(r'\s*<a\s+id=["\'][^"\']*["\']\s*/>\s*$', '', title_with_anchor)

            # 检查行内是否有 <a id="..." />
            inline_anchor_match = re.search(r'<a\s+id=["\']([^"\']+)["\']\s*/>', line)
            if inline_anchor_match:
                # 行内显式锚点
                anchor = inline_anchor_match.group(1)
            else:
                # 往上查找第一个非空行，如果是 <a id="..." /> 则作为锚点
                anchor = None
                j = i - 1
                while j >= 0:
                    prev_line = lines[j].strip()
                    # 如果遇到空行，继续往上找
                    if not prev_line:
                        j -= 1
                        continue
                    # 如果遇到标题，停止查找
                    if re.match(r'^#{1,6}\s', prev_line):
                        break
                    # 如果是 <a id="..." /> 标签，使用作为锚点
                    if re.match(r'^<a\s+id=["\'][^"\']+["\']\s*/>\s*$', prev_line):
                        anchor_match = re.search(r'<a\s+id=["\']([^"\']+)["\']\s*/>', prev_line)
                        if anchor_match:
                            anchor = anchor_match.group(1)
                        break
                    # 如果是其他内容，停止查找
                    break

                # 如果没有找到显式锚点，使用 slugified 标题
                if not anchor:
                    anchor = slugify(title)

            headings.append((title, anchor, i + 1))
        i += 1

    return headings


def extract_param_fields(content: str) -> List[dict]:
    """
    提取所有 ParamField 组件及其生成的锚点。
    返回: [ParamField 信息字典, ...]
    """
    param_fields = []

    # 匹配 ParamField 组件
    # 使用多行匹配模式
    pattern = r'<ParamField\s+(.*?)>(.*?)</ParamField>'
    matches = re.findall(pattern, content, re.DOTALL)

    for props_str, body in matches:
        props = {}

        # 提取 name 属性
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', props_str)
        if name_match:
            props['name'] = name_match.group(1)

        # 提取 anchor_suffix 属性
        suffix_match = re.search(r'anchor_suffix\s*=\s*["\']([^"\']+)["\']', props_str)
        if suffix_match:
            props['anchor_suffix'] = suffix_match.group(1)

        # 提取 parent_name 属性
        parent_name_match = re.search(r'parent_name\s*=\s*["\']([^"\']+)["\']', props_str)
        if parent_name_match:
            props['parent_name'] = parent_name_match.group(1)

        # 提取 parent_type 属性
        parent_type_match = re.search(r'parent_type\s*=\s*["\']([^"\']+)["\']', props_str)
        if parent_type_match:
            props['parent_type'] = parent_type_match.group(1)

        if props:
            param_fields.append(props)

    return param_fields


def generate_param_field_anchors(param_field: dict) -> List[str]:
    """
    根据 ParamField 属性生成所有可能的锚点。
    按照 mdx_writing_guide.md 中的 ParamField 锚点生成逻辑。
    """
    anchors = []

    name = param_field.get('name', '')
    anchor_suffix = param_field.get('anchor_suffix', '')
    parent_name = param_field.get('parent_name', '')
    parent_type = param_field.get('parent_type', '')

    if not name:
        return anchors

    # 基础锚点：name 转小写
    base_anchor = slugify(name)

    # 1. 如果有 anchor_suffix，基础锚点为 name + suffix
    if anchor_suffix:
        base_anchor = slugify(name) + anchor_suffix
        anchors.append(base_anchor)
    else:
        anchors.append(base_anchor)

    # 2. OC 冒号方法名，额外生成首段锚点
    # 例如: createEngineWithProfile:eventHandler: -> createenginewithprofile
    if ':' in name:
        # 提取第一个冒号之前的部分
        first_segment = name.split(':')[0]
        if first_segment != name:
            first_anchor = slugify(first_segment)
            if anchor_suffix:
                first_anchor += anchor_suffix
            anchors.append(first_anchor)

    # 3. 如果有 parent_name，生成带父类上下文的锚点
    if parent_name:
        parent_slug = slugify(parent_name)
        # name + parent_name
        anchors.append(base_anchor + '-' + parent_slug)

        # 如果还有 parent_type，生成 name + parent_name + parent_type
        if parent_type:
            anchors.append(base_anchor + '-' + parent_slug + '-' + parent_type)

    return list(set(anchors))  # 去重


def get_all_headings(mdx_file_path: str) -> List[str]:
    """
    获取文档中所有的 heading 标题文字。

    参数:
        mdx_file_path: MDX 文件路径

    返回:
        标题文字列表，按文档顺序排列
    """
    if not os.path.exists(mdx_file_path):
        return []

    with open(mdx_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    headings = extract_headings_with_anchors(content)
    return [title for title, _, _ in headings]


def is_valid_anchor(mdx_file_path: str, anchor: str) -> bool:
    """
    检验锚点是否有效。
    检查方法：
    1. 收集所有的 heading 行（以 # 开头），循环进行比较：
        1.1 将锚点和标题都转换为小写进行比较
        1.2 正则匹配在 heading 行内匹配 <a id="anchor_name" /> 这样的格式，取出 anchor_name 与传入的锚点进行比较
        1.3 从 heading 行往前逐行查找第一个非空行，如果能正则匹配单行 <a id="anchor_name" /> 这样的格式，取出 anchor_name 与传入的锚点进行比较
    2. 收集所有 ParamField 组件，循环进行比较：
        2.1 按 mdx_writing_guide.md 中的 ParamField 锚点生成逻辑，生成可能的锚点，与传入的锚点进行比较

    参数:
        mdx_file_path: MDX 文件路径
        anchor: 要检查的锚点

    返回:
        True 如果锚点有效，False 否则
    """
    if not anchor or not re.match(r'^[a-zA-Z0-9-]+$', anchor):
        return False

    if not os.path.exists(mdx_file_path):
        return False

    with open(mdx_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 检查 heading 锚点
    headings = extract_headings_with_anchors(content)
    for _, heading_anchor, _ in headings:
        if heading_anchor == anchor:
            return True

    # 2. 检查 ParamField 生成的锚点
    param_fields = extract_param_fields(content)
    for param_field in param_fields:
        anchors = generate_param_field_anchors(param_field)
        if anchor in anchors:
            return True

    return False


def add_anchor_to_file(mdx_file_path: str, title: str, anchor_name: str) -> bool:
    """
    在文件中为标题添加锚点定义。

    生成规则：
    1. 收集所有的 heading 行（以 # 开头），循环进行比较
    2. 如果 title 与 heading 行相同，则在该 heading 行后添加 <a id="anchor_name" /> 这样的内容

    参数:
        mdx_file_path: MDX 文件路径
        title: 标题文本
        anchor_name: 锚点名称

    返回:
        True 如果成功添加或已存在，False 否则
    """
    if not os.path.exists(mdx_file_path):
        return False

    with open(mdx_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # 查找匹配的标题行（支持标题后已有锚点标签）
        match = re.match(r'^(#{1,6})\s+' + re.escape(title) + r'(?:\s*<a\s+id=["\'][^"\']*["\']\s*/>)?\s*$', line)
        if match:
            # 检查行内是否已有锚点
            if '<a id=' in line:
                return True  # 已存在，不需要添加

            # 在标题行末尾添加锚点
            anchor_tag = f' <a id="{anchor_name}" />'
            lines[i] = line.rstrip() + anchor_tag

            # 写回文件
            with open(mdx_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            return True

    return False  # 没找到匹配的标题


# CLI 接口
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法:')
        print('  检查锚点: python anchor_helper.py check <文件路径> <锚点名>')
        print('  生成锚点: python anchor_helper.py generate <文件路径> <标题> <锚点名>')
        print('  获取标题: python anchor_helper.py headings <文件路径>')
        print('')
        print('示例:')
        print('  python anchor_helper.py check path/to/file.mdx document-structure-check')
        print('  python anchor_helper.py generate path/to/file.mdx "文档结构检查" document-structure-check')
        print('  python anchor_helper.py headings path/to/file.mdx')
        sys.exit(1)

    action = sys.argv[1]

    if action == 'check':
        if len(sys.argv) < 4:
            print('错误: check 模式需要文件路径和锚点名')
            print('用法: python anchor_helper.py check <文件路径> <锚点名>')
            sys.exit(1)
        file_path = sys.argv[2]
        anchor_name = sys.argv[3]
        result = is_valid_anchor(file_path, anchor_name)
        print('Valid' if result else 'Invalid')
        sys.exit(0 if result else 1)

    elif action == 'generate':
        if len(sys.argv) < 5:
            print('错误: generate 模式需要文件路径、标题和锚点名')
            print('用法: python anchor_helper.py generate <文件路径> <标题> <锚点名>')
            sys.exit(1)
        file_path = sys.argv[2]
        title = sys.argv[3]
        anchor_name = sys.argv[4]
        result = add_anchor_to_file(file_path, title, anchor_name)
        if result:
            print(f'成功添加锚点: {anchor_name}')
            sys.exit(0)
        else:
            print(f'失败: 未找到标题 "{title}" 或文件不存在')
            sys.exit(1)

    elif action == 'headings':
        if len(sys.argv) < 3:
            print('错误: headings 模式需要文件路径')
            print('用法: python anchor_helper.py headings <文件路径>')
            sys.exit(1)
        file_path = sys.argv[2]
        headings = get_all_headings(file_path)
        import json
        print(json.dumps(headings, ensure_ascii=False, indent=2))
        sys.exit(0)

    else:
        print(f'错误: 未知操作 "{action}"')
        print('支持的操作: check, generate, headings')
        sys.exit(1)
