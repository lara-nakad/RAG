#So our definition should be:
#A paragraph is a group of lines separated from the next group by one or more blank lines.

from .chunk import Chunk
from pathlib import Path


def get_start_index(lines: list[str])->list[int]:
    index = 0
    line_starts = []
    for line in lines:
        line_starts.append(index)
        index += len(line)
    
    return line_starts


def create_chunk(full_file_path, content, start_index, end_index):
    return Chunk(
                file_path= full_file_path, 
                text= content[start_index:end_index],
                first_character_index= start_index,
                last_character_index= end_index)


def text_chunk(file_path: str, max_chunk_size):
    res = []

    with open(file_path, "r") as fd:
        content = fd.read()

    lines = content.splitlines(keepends=True)

    paragraphs = []
    current_parag = []
    start_lines = get_start_index(lines)

    for i, line in enumerate(lines):
        #here it means we reach the end of the current paragraph
        if line.strip() == "":
            if current_parag:
                paragraphs.append(current_parag)
                current_parag = []
        else:
            current_parag.append((i, start_lines[i], line))

    #for the last paragraph inside the file
    if current_parag:
        paragraphs.append(current_parag)
    
    start_pos = 0
    end_pos = 0
    
    sections = []
    #[(0, 0, 'Python is a programming language.\n'), 
    #(1, 34, 'It is widely used for web development, data analysis, automation, and artificial intelligence.\n'), 
    #(2, 129, 'Python has a simple syntax that makes it easy to learn.\n')]
    for i, parag in enumerate(paragraphs):
        start_pos = 0
        end_pos = 0
        for j, line in enumerate(parag):
            #print(line)
            if j == 0:
                start_pos = line[1]
            if j == len(parag) - 1:
                end_pos = line[1] + len(line[2])
        sections.append((start_pos, end_pos, content[start_pos:end_pos]))
    
    for section in sections:
        piece = section[2]
        if len(piece) <= max_chunk_size:
            res.append(create_chunk(file_path, content, section[0], section[1]))
        else:
            curr_len = 0
            curr_start = section[0]
            curr_lines = ""

            splitted_section = piece.splitlines(keepends=True)

            for single_line in splitted_section:
                line_len = len(single_line)

                if curr_len + line_len <= max_chunk_size:
                    curr_lines += single_line
                    curr_len += line_len

                else:
                    #here when we want to get the end we make from where it starts and how many characters till the end
                    curr_end = curr_start + curr_len

                    res.append(create_chunk(file_path, content, curr_start, curr_end))

                    curr_start = curr_end
                    curr_lines = single_line
                    curr_len = line_len

            if curr_lines:
                curr_end = curr_start + curr_len
                res.append(create_chunk(file_path, content, curr_start, curr_end))
    return res
