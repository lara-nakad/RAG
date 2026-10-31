import ast
from .chunk import Chunk
from pathlib import Path

#node.lineno => tells us the number of line in which where this node starts inside the file (where the first line of this node is located inside the file)
#node.end_lineno => tells us the number of line in which where this node ends inside the file (where the last line of this node is located inside the file)
#node.col_offset => btaateena wein l position la awl character b aleb haida node bs as related to its line mish bl file kellu
#node.end_col_offset => btaateena wein aw addei l position la ekher character b alb haida node bs as related to its line mish la file kellu 


#difference between append and extend:
    #ex:  list1 = [c1, c2, c3]
    #     list2 = [c4, c5, c6] if list1.append(list2)=> [c1, c2, c3, [c4, c5, c6]]
    #                          if list1.extend(list2)=>[c1, c2, c3, c4, c5, c6]


def get_line_starts(list_lines: list[str])->list[int]:
    index = 0
    start_lines = []
    for _ , line in enumerate(list_lines):
        start_lines.append(index)
        index += len(line)
    
    return start_lines


def get_start_end(node, lines_start)->tuple[int, int]:
    line_start = node.lineno
    line_end = node.end_lineno
    col_offset_start = node.col_offset
    col_offset_end = node.end_col_offset
    start_index = lines_start[line_start - 1] + col_offset_start
    end_index = lines_start[line_end -  1] + col_offset_end

    return (start_index, end_index)


def create_chunk(full_file_path, content, start_index, end_index):
    return Chunk(
                file_path= full_file_path, 
                text= content[start_index:end_index],
                first_character_index= start_index,
                last_character_index= end_index)


#this function is used in order to now the type of each node if is it class / function / async func/ if / for/ while / try.....
def get_structural_nodes(node, lines_start):
    children = []
    
    if isinstance(node, ast.If):
        children.extend(node.body)
        children.extend(node.orelse)
    
    elif isinstance(node, ast.Try):
        children.extend(node.body)

        for handler in node.handlers:
            children.extend(handler.body)

        children.extend(node.orelse)
        children.extend(node.finalbody)
    
    elif hasattr(node, "body"):
        children.extend(node.body)
    
    children.sort(
        key=lambda child: get_start_end(child, lines_start)[0]
    )
    return children

def split_large_node(child, start_child, end_child, full_content, lines_start, file_path, max_chunk_size, parent_header=""):
    res = []

    body_nodes = get_structural_nodes(child, lines_start)
    if not body_nodes:
        return []
    # Get this node's header
    first_child_start, _ = get_start_end(body_nodes[0], lines_start)
    
    #here it is used to preserve the header content
    if parent_header == "":
        header_start = start_child
        header_end = first_child_start
        header_content = full_content[header_start:header_end]
    else:
        # so here we are taking the header function the main one + the header of the current subchild that exceeds 2000
        header_content = parent_header + full_content[start_child:first_child_start]

    i = 0

    start_chunk = None
    end_chunk = None

    while i < len(body_nodes):
        sub_child = body_nodes[i]

        start_sub_child, end_sub_child = get_start_end(sub_child, lines_start)
        
        subchild_content = full_content[start_sub_child:end_sub_child]
        if len(subchild_content) > max_chunk_size:
            res.extend(
                split_large_node(
                    sub_child,
                    start_sub_child,
                    end_sub_child,
                    full_content,
                    lines_start,
                    file_path,
                    max_chunk_size,
                    header_content))
            #here since we process the current child so we should go to the next 
            i += 1
            continue
        
        if start_chunk is None:
            start_chunk = start_sub_child

        proposed_content = (header_content + full_content[start_chunk:end_sub_child])

        if len(proposed_content) <= max_chunk_size:
            end_chunk = end_sub_child
            i += 1
            continue

        if start_chunk is not None and end_chunk is not None:
            real_content = (header_content + full_content[start_chunk:end_chunk])
            res.append(
                create_chunk(
                    file_path,
                    full_content,
                    start_chunk,
                    end_chunk
                )
            )

        start_chunk = start_sub_child
        end_chunk = end_sub_child

        i += 1

    if start_chunk is not None and end_chunk is not None:
        final_body = full_content[start_chunk:end_chunk]
        final_content = (header_content + final_body)

        res.append(
            create_chunk(
                file_path,
                full_content,
                start_chunk,
                end_chunk))
    
    res.sort(key=lambda chunk: chunk.first_character_index)
    return res

     

def python_chunking(file_path: str, max_chunk_size)-> list[Chunk]:

    # here we get the content as a string
    with open(file_path, "r") as fd:
        content = fd.read()
        
    STRUCTURAL_NODES = (
        ast.ClassDef,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
    )
    
    res_chunks: list[Chunk] = []

    lines = content.splitlines(keepends = True)
    lines_start = get_line_starts(lines)
    tree = ast.parse(content)

    for child in ast.iter_child_nodes(tree):
        if not isinstance(child, STRUCTURAL_NODES):
            continue
        
        start_child_index, end_child_index = get_start_end(child, lines_start)

        context = content[start_child_index: end_child_index]
        if len(context) <= max_chunk_size:
            res_chunks.append(create_chunk(file_path, content, start_child_index, end_child_index))
        else:
            res_chunks.extend(split_large_node(child, start_child_index, end_child_index, content, lines_start, file_path, max_chunk_size))

    return res_chunks
    