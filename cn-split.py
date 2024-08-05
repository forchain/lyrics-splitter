import re

def parse_time_to_seconds(time_str):
    """将时间标签转换为秒"""
    parts = time_str.split(':')
    if len(parts) == 3:
        minutes, seconds, milliseconds = parts
        return int(minutes) * 60 + float(seconds) + float(milliseconds) / 1000
    elif len(parts) == 2:
        minutes, seconds = map(float, parts)
        return minutes * 60 + seconds
    else:
        return float(parts[0])  # Assume it's all in seconds if only one part

def seconds_to_time_str(seconds):
    """将秒转换回时间标签格式"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"[{minutes:02d}:{seconds:05.2f}]"

def split_lyrics_line(line, next_line_time):
    """根据空格拆分歌词，并根据字符数分配时间"""
    time_str, lyrics = line.split(']', 1)
    original_time = parse_time_to_seconds(time_str[1:-1])
    next_time = parse_time_to_seconds(next_line_time[1:-1])
    total_time = next_time - original_time

    phrases = lyrics.split()
    total_chars = sum(len(phrase) for phrase in phrases)

    current_time = original_time
    parts = []

    for phrase in phrases:
        part_ratio = len(phrase) / total_chars
        part_duration = total_time * part_ratio
        parts.append(f"{seconds_to_time_str(current_time)}{phrase}")
        current_time += part_duration

    return parts

def process_lyrics(lines):
    """处理整个歌词文件的断句逻辑，忽略包含多个时间戳的行"""
    new_lines = []
    time_stamp_regex = re.compile(r'^(\[\d{1,3}:\d{2}\.\d{2,3}\])+')  # 正则表达式匹配一个或多个时间戳
    for i, line in enumerate(lines[:-1]):
        match = time_stamp_regex.match(line)
        if match and line.count('[') == 1:  # 匹配且只有一个时间戳
            next_line_time = lines[i + 1].split(']', 1)[0] + ']'
            new_lines.extend(split_lyrics_line(line, next_line_time))
        else:
            new_lines.append(line)
    if lines and time_stamp_regex.match(lines[-1]) and lines[-1].count('[') == 1:
        new_lines.append(lines[-1])  # 处理最后一行，如果它有一个有效的时间戳
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
input_file_path = 'input.lrc'  # 替换成实际的输入文件路径
output_file_path = 'output.lrc'  # 指定输出文件的路径

original_lyrics = read_lrc_file(input_file_path)
processed_lyrics = process_lyrics(original_lyrics)
write_lrc_file(output_file_path, processed_lyrics)