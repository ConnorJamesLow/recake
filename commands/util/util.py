import json
from os import path, makedirs
from os.path import dirname
from shutil import copytree, copy2 as copy_file
from random import randint, shuffle
from datetime import datetime
import shutil

content_path = path.expanduser(path.join('~', '.remakes/'))

def conseq(cond, true, false):
    """
    Behaves like the tenary operator. 
    """
    if cond:
        return true
    else:
        return false


def ensure_attr(observer: object, prop: str, fallback):
    """
    Ensure an observer has an attribute (prop).
    """
    if not hasattr(observer, prop):
        setattr(observer, prop, fallback)


def gen_id() -> str:
    today = datetime.now()
    res = ''
    for c in f'{today.toordinal()}':
        res += chr(int(c, 10) + 65)
    res += '_'
    i = 0
    while i < 10:
        i += 1
        res += chr(randint(97, 122))
    return res


def copy_source(src, dest):
    """
    Copy content from src to dest folder.
    """
    print(f'copy_source: {src} -> {dest}')
    dest = path.expanduser(path.join('~', dest))
    print(f'dest: {dest}')
    if path.isdir(src):
        if path.exists(dest):
            raise Exception('Could not copy. Please try again.')
        copytree(src, dest)
    elif path.isfile(src):
        content_path = path.dirname(src)
        if not path.exists(content_path):
            makedirs(content_path)
        p = copy_file(src, dest)
        print(p)
        
    
def file_exists(src):
    print(f'src:{src} exists:{path.exists(src)} isfile:{path.isfile(src)}')
    return path.exists(src) and path.isfile(src)

def get_jpath():
    return path.expanduser(path.join('~', '.remakes\\remakes.json'))