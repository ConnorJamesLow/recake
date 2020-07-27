import shutil
import os
from util import conseq


class Source:
    def __init__(self, src):
        self.__src = src

    def get_src(self):
        return self.__src

    def try_copy(self, dest):
        if os.path.exists(dest):
            return False
        shutil.copytree(self.__src, dest)
        return True


def create_source(
    src,
    make_store=False,
    store=''
):
    if make_store or store:
        store_source(src, store or os.getcwd())
    s = Source(src)
    return s


def store_source(src, store):
    return True
