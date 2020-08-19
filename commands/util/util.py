import re
import click
from os import path, makedirs, getcwd, remove, listdir
from shutil import copy, copytree, copy2 as copy_file, rmtree
from random import randint
from datetime import datetime
from fnmatch import fnmatch
from typing import Iterable

content_path = path.expanduser(path.join('~', '.recakes/'))


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


def copy_source(src, dest, overwrite: bool = False):
    """
    Copy content from src to dest folder.
    """
    src = calculate_path(src)
    dest = calculate_path(dest)
    print(f'copy_source: {src} -> {dest}')
    if path.isdir(src):
        if overwrite:
            uncopy_source(dest)
        if path.exists(dest):
            raise Exception('Could not copy. Please try again.')
        p = copytree(src, dest)
        print(p)
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
        rmtree(src, ignore_errors=True)


def calculate_path(src):
    if path.exists(src):
        return path.abspath(src)
    if re.search('[.]recakes/', src):
        return path.expanduser(path.join('~', src))
    return path.join(getcwd(), src)


def file_exists(src):
    return path.exists(src) and path.isfile(src)


def get_jpath():
    return path.expanduser(path.join('~', '.recakes\\recakes.json'))


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


def get_lines(file: str):
    with open(file, 'a+') as f:
        f.seek(0)
        lines = f.readlines()
    return lines


def fsitem_type(p):
    """Get an item from file-system and determine what it is (`dir` or `file`.)"""
    if path.isfile(p):
        return 'file'
    if path.isdir(p):
        return 'dir'
    if path.islink(p):
        return 'link'
    return 'unknown'


def glob_copy(source: str, destination: str, exclude: Iterable):
    """
    Copy `source` to `destination`, excluding items in the source which match any of `exclude`.
    """
    exclude = list(exclude)
    print(f'source: "{source}", dest: "{destination}"')
    if not path.exists(source):
        raise Exception(f'Source "{source}" not found.')
    def recurse(p: str):
        # print(f'try: "{p}"')
        full = path.abspath(p)
        # print(f'  full: "{full}"')
        rel = re.sub(r'^[\\/]|[\\/]$', '', full[len(source):])
        copy_path = path.join(destination, rel)
        # print(f'  rel: "{rel}" ({rel.strip("/")})')
        reason = next(
            (e for e in exclude if (fnmatch(rel.strip('/'), e.strip('/')))),
            None
        )
        for e in exclude:
            if not re.match(r'^\.?[/\\]', e):
                e = path.join('**', e)
            if fnmatch(rel.strip('/').strip('\\'), e.strip('/').strip('\\')):
                reason = e
        if reason and (not(reason.endswith('/')) or path.isdir(full)):
            print('EXCLUDE', full, f'(re: "{reason}")')
            return
        print(
            f' + ({rel}) \n\tcopy {fsitem_type(full)} \n\t\t"{full}" \n\tto \n\t\t"{copy_path}"')
        if path.isdir(full):
            makedirs(copy_path)
            for d in listdir(full):
                recurse(path.join(full, d))
        elif path.isfile(full):
            pass
            copy_file(full, copy_path)
    # top-level content:
    makedirs(destination)
    for d in listdir(source):
        recurse(d)

def test():
    dest = path.abspath('../__test')
    if path.exists(dest):
        rmtree(dest)
    glob_copy(
        path.abspath('.'),
        dest,
        (l.strip('\n') for l in get_lines('test') if re.match(r'^[^#\s]', l)))
