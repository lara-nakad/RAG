from .chunk import Chunk
from typing import Tuple

def create_chunk(full_file_path, content, start_index, end_index):
    return Chunk(
                file_path= full_file_path, 
                text= content[start_index: end_index],
                first_character_index= start_index,
                last_character_index= end_index)

def get_heading_info(line:str):
    counter = 0

    if not line.startswith('#'):
        return (False, counter)

    for c in line:
        if c == '#':
            counter += 1
        else:
            break
    
    if counter < len(line) and line[counter] == ' ':
        return (True, counter)
    return (False, counter)


def get_line_starts(lines: list[str]):
    start_nums = []
    index = 0

    for line in lines:
        start_nums.append(index)
        index += len(line)
    
    return start_nums


def get_section(list_headings, content):
    
    sections = []

    for i, heading in enumerate(list_headings):
        end = len(content)
        _, level, start, heading_title = heading
        
        if i == 0 and start > 0:
            start = 0

        for _, next_heading in enumerate(list_headings[i+1:]):
            _, next_level, next_start, _ = next_heading
            if next_level <= level:
                end = next_start
                break
        
        sections.append((level, start, end, heading_title))
    
    return sections


def split_by_size(file_path, content, start, end, max_chunk_size):
    res = []
    while start < end:
        next_end = min((start + max_chunk_size), end)
        res.append(create_chunk(file_path, content, start, next_end))

        start = next_end
    
    return res


def split_section(file_path, level, start, end, full_content, list_headings, max_chunk_size):
    children = []
    for i, heading in enumerate(list_headings):
        _, level_next, start_next, _ = heading
        if start < start_next < end and level_next == (level + 1):
            children.append(heading)
    
    #no sub headings we need to split by content inside
    if len(children) == 0:
        return (split_by_size(file_path, full_content, start, end, max_chunk_size))

    res = []
    boundaries = [start]
    boundaries = [start]

    for i, child in enumerate(children):
        if i == 0:
            continue
        boundaries.append(child[2])
    
    boundaries.append(end)

    for i in range(len(boundaries) - 1):
        piece_start = boundaries[i]
        piece_end = boundaries[i + 1]
        piece = full_content[piece_start: piece_end]
        if len(piece) <= max_chunk_size:
            res.append(create_chunk(file_path, full_content, piece_start, piece_end))
        else:

            piece_level = None
            for child in children:
                if child[2] == piece_start:
                    piece_level = child[1]
                    break
            
            if piece_level is not None:
                res.extend((split_section(file_path, piece_level, piece_start, piece_end, full_content, list_headings, max_chunk_size)))
            
            else:
                res.extend((split_by_size(file_path, full_content, piece_start, piece_end, max_chunk_size)))
    return res


def markdown_chunking(file_path : str, max_chunk_size=2000):
    res = []
    #read the content
    with open(file_path, "r") as fd:
        content = fd.read()

    #here we are splitting the lines based on '\n'
    lines = content.splitlines(keepends = True)

    start_lines = get_line_starts(lines)

    #get the headings 
    list_headings = []

    code_block = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            code_block = not code_block
        
        if code_block:
            continue

        heading_state, level = get_heading_info(line)
        if heading_state:
            list_headings.append((i, level, start_lines[i], line.strip()))
    
    if not list_headings:
        return split_by_size(file_path, content, 0, len(content), max_chunk_size)
        
    #get the start and end of each section
    sections = get_section(list_headings, content)

    #get the length of each section and check its leng

    min_level = min(level for level, _, _, _ in sections)
    
    for section in sections:
        level, start, end, _ = section

        if level != min_level:
            continue

        context = content[start:end]

        if len(context) <= max_chunk_size:
            res.append(create_chunk(file_path, content, start, end))
            
        else:
            res.extend(split_section(file_path,level,start,end,content,list_headings, max_chunk_size))

    return res