import os
import re

def remove_invalid_label(directory, invalid_label=None):
    """
    从YOLO标签文件中移除指定的无效标签
    
    参数:
        directory (str): 包含标签文件的目录路径
        invalid_label (int, optional): 需要移除的标签编号，默认为None
    """
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 只处理.txt文件（YOLO标签文件）
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(directory, filename)

        # 存储过滤后的行
        filtered_lines = []
        try:
            # 读取文件内容
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 处理每一行
            for line in lines:
                # 处理空行
                stripped_line = line.strip()
                if not stripped_line:
                    filtered_lines.append(line)  # 保留空行
                    continue

                # 分割第一个字段（标签编号）
                parts = stripped_line.split(maxsplit=1)
                try:
                    first_num = int(parts[0])
                    # 如果标签编号不等于要删除的标签，则保留该行
                    if first_num != invalid_label:
                        filtered_lines.append(line)
                    else:
                        # 符合删除条件，不保留该行
                        pass
                except (IndexError, ValueError):
                    # 格式错误的行也保留，只打印警告
                    print(f"Warning: Invalid format in file '{filename}' for line: {stripped_line}")
                    filtered_lines.append(line)

            # 将过滤后的内容写回文件
            with open(file_path, 'w') as f:
                f.writelines(filtered_lines)

        except Exception as e:
            # 处理文件读写异常
            print(f"Error processing {file_path}: {str(e)}")


def change_label(directory, old_label, new_label):
    """
    将目录中所有YOLO标签文件的指定标签编号替换为新编号
    
    参数:
        directory (str): 包含标签文件的目录路径
        old_label (int): 需要被替换的旧标签编号
        new_label (int): 新的标签编号
    """
    # 检查old_label和new_label是整数
    assert isinstance(old_label, int) and isinstance(new_label, int), "Both old_label and new_label must be integers."

    # 正则表达式匹配开头空白、数字和剩余内容
    pattern = r'^(\s*)(\d+)(.*)$'

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 只处理.txt文件（YOLO标签文件）
        if not filename.endswith('.txt'):
            continue

        file_path = os.path.join(directory, filename)

        try:
            # 读取文件内容
            with open(file_path, 'r') as f:
                lines = f.readlines()

            # 存储修改后的行
            new_lines = []
            for line in lines:
                # 使用正则表达式匹配行格式
                match = re.match(pattern, line)
                if not match:
                    # 格式不符合，保留原样
                    new_lines.append(line)
                    continue

                # 提取前导空白、数字部分和剩余内容
                leading_spaces = match.group(1)  # 前导空白（可能为空）
                number_part = match.group(2)     # 第一个数字字段（标签编号）
                rest_of_line = match.group(3)    # 后面的内容（包括分隔符等）

                try:
                    # 尝试将数字部分转换为整数
                    num_value = int(number_part)
                except ValueError:
                    # 数字转换失败，保留原样
                    new_lines.append(line)
                    continue

                # 如果数字等于旧标签编号，则替换为新标签编号
                if num_value == old_label:
                    # 替换为new_label并保持原始格式
                    modified_line = f"{leading_spaces}{new_label}{rest_of_line}"
                    new_lines.append(modified_line)
                else:
                    # 不修改
                    new_lines.append(line)

            # 将修改后的内容写回文件
            with open(file_path, 'w') as f:
                f.writelines(new_lines)

        except Exception as e:
            # 处理文件读写异常
            print(f"Error processing {file_path}: {str(e)}")


if __name__ == "__main__":
    # 指定目标目录
    target_dir = "/home/pc/sgcc/Datasets/SGData/det/detdata/Pole/validLabels"
    # 移除标签编号为2的无效标签
    remove_invalid_label(target_dir, invalid_label=2)
    # 将标签编号3替换为9
    change_label(target_dir, old_label=3, new_label=9)
