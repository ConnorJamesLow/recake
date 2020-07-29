import re
from os import path, makedirs, getcwd, remove
from shutil import copytree, copy2 as copy_file, rmtree
from random import randint
from datetime import datetime

import click

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

def uncopy_source(src):
    src = calculate_path(src)
    if not path.exists(src):
        raise Exception(
            f'Not found. "{src}" is not a valid path.')
    
    if path.isfile(src):
        remove(src)
    else:
        rmtree(src, ignore_errors = True)

def calculate_path(src):
    if path.exists(src):
        return src
    if re.search('[.]remakes/', src):
        return path.expanduser(path.join('~', src))

    return path.join(getcwd(), src)


def file_exists(src):
    return path.exists(src) and path.isfile(src)


def get_jpath():
    return path.expanduser(path.join('~', '.remakes\\remakes.json'))


def truncate(s: str, m: int):
    if len(s) < m:
        return s

    if m < 25:
        return f'...{s[:(m - 3)]}'

    return f'{s[:(m - 25)]}...{s[(len(s) - 22):]}'

def fin(message):
    click.secho(message + '\n', fg="green")

def err(message):
    click.secho(message + '\n', fg="red")

def warn(message):
    click.secho(message + '\n', fg="yellow")

