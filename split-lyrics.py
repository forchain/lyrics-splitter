import re


def parse_time_to_seconds(time_str):
    """将时间标签转换为秒"""
    minutes, seconds = map(float, time_str.split(':'))
    return minutes * 60 + seconds


def seconds_to_time_str(seconds):
    """将秒转换回时间标签格式"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"[{minutes:02d}:{seconds:05.2f}]"


def split_lyrics_line(line, next_line_time):
    """递归地拆分每段歌词，确保每段长度都小于40"""

    if len(line) < 45:
        return [line]

    time_str, lyrics = line.split(']', 1)
    original_time = parse_time_to_seconds(time_str[1:-1])
    next_time = parse_time_to_seconds(next_line_time[1:-1])
    total_time = next_time - original_time

    words = lyrics.split()
    parts = []  # 存储所有拆分后的歌词部分
    current_part = []
    current_time = original_time

    for word in words:
        if len(seconds_to_time_str(current_time) + ' '.join(current_part + [word])) < 40:
            current_part.append(word)
        else:
            # 计算当前部分的时间比例
            part_ratio = len(current_part) / len(words)
            parts.append((current_time, ' '.join(current_part)))
            current_time += total_time * part_ratio
            current_part = [word]  # 开始新的一部分

    if current_part:  # 添加最后一部分
        parts.append((current_time, ' '.join(current_part)))

    # 格式化为LRC格式
    formatted_parts = [f"{seconds_to_time_str(part_time)}{part_lyrics}" for part_time, part_lyrics in parts]
    return formatted_parts


def process_lyrics(lines):
    """处理整个歌词文件的断句逻辑"""
    new_lines = []
    for i, line in enumerate(lines[:]):
        if ']' in line and all(c.isdigit() or c in [':', '.', '[', ']'] for c in line.split(']', 1)[0]):
            # 忽略多个时间标签的行
            if line.count('[') > 1:
                new_lines.append(line)
                continue

            next_line_time = lines[i + 1].split(']', 1)[0] + ']'
            new_lines.extend(split_lyrics_line(line, next_line_time))
        else:
            new_lines.append(line)
    return new_lines


def process_lyrics(lines):
    """处理整个歌词文件的断句逻辑"""
    new_lines = []
    for i, line in enumerate(lines[:-1]):
        if ']' in line and all(c.isdigit() or c in [':', '.', '[', ']'] for c in line.split(']', 1)[0]):
            # 忽略多个时间标签的行
            if line.count('[') > 1:
                new_lines.append(line)
                continue

            next_line_time = lines[i + 1].split(']', 1)[0] + ']'
            new_lines.extend(split_lyrics_line(line, next_line_time))
        else:
            new_lines.append(line)
    new_lines.append(lines[-1])  # 添加最后一行
    return new_lines


def read_lrc_file(file_path):
    """读取LRC文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def write_lrc_file(file_path, lines):
    """将处理后的歌词写入到新的LRC文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')


# 使用示例
input_file_path = 'input.lrc'  # 这里替换成实际的输入文件路径
output_file_path = 'output.lrc'  # 这里指定输出文件的路径

original_lyrics = read_lrc_file(input_file_path)
processed_lyrics = process_lyrics(original_lyrics)
write_lrc_file(output_file_path, processed_lyrics)
