#!/usr/bin/env python3
# tag相关的工具类

import json
from pathlib import Path
from typing import Dict
from typing import List

def get_tag_file(file: str) -> Path:
    """获取一个文件对应的tag文件

    Args:
        file (str): 文件路径

    Returns:
        Path: 代表tag文件的Path类型的对象
    """
    path = Path(file)
    tag_dir = path.parent / ".tag"
    tag_dir.mkdir(exist_ok=True)
    tag_file = tag_dir.joinpath(path.name + ".json")
    return tag_file


def load_tag_content(tag_file: Path) -> Dict:
    """加载tag文件中的内容

    Args:
        tag_file (Path): tag文件

    Returns:
        Dict: JSON对象
    """
    if tag_file.exists():
        content = json.loads(tag_file.read_text(encoding='utf-8'))
    else:
        content = json.loads('{}')
    return content


def write_tag_content(tag_file: Path, tag_content:Dict):
    """将tag文件的内容写到文件中

    Args:
        tag_file (Path): tag文件
        tag_content (Dict): 待写入的内容
    """
    with open(tag_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(tag_content, ensure_ascii=False, indent=2))


def get_file_tags(file: str) -> List[str]:
    """获取一个文件的tags

    Args:
        file (str): 文件路径

    Returns:
        List[str]: 该文件的所有tags
    """
    tag_file = get_tag_file(file)
    content = load_tag_content(tag_file)
    file_tags = content.get('tags', [])
    return file_tags


def get_files_tags(files: List[str]) -> List[str]:
    """获取一组文件使用到的tags

    Args:
        files (List[str]): 一组文件路径

    Returns:
        List[str]: 这组文件的所有tags
    """
    total_tags = []
    for file in files:
        file_tags = get_file_tags(file)
        for tag in file_tags:
            if tag not in total_tags:
                total_tags.append(tag)
    return sorted(total_tags)


def get_dir_tags(dir: str) -> List[str]:
    """获取一个目录下所有文件使用到的tags

    Args:
        dir (str): 目录的路径
    """
    path = Path(dir)
    files = list(path.iterdir())
    return get_files_tags(files)

