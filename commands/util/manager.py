from commands.util.util import truncate
from os import getcwd, path
from typing import List
from commands.util import util
from commands.util.jef import subjectify, Observer
import pyperclip


class Manager:
    def __init__(self):
        self.__json = subjectify(util.get_jpath())

        # Load the state
        util.ensure_attr(self.__json, 'sources', [])

    def load(self, rid: str = None, name: str = None):
        """
        Find the state of the source using the name or the id.
        """
        json = self.__json
        if not rid or name:
            return None

        # Try to find the state by Id
        state: Observer = next(
            (s for s in json.sources if s["id"] == rid), None)

        if not state:
            # If not found, try again by name
            state = next(
                (s for s in json.sources if s["name"] == name), None)

        # If no state found, return False
        return state

    def add(self, src: str = None, name: str = None, _type: str = None):
        """
        Create local copy of the source in the `.remakes/` cache.
        """
        if not src:
            raise Exception('Must include the src parameter')

        json = self.__json
        util.ensure_attr(json, 'sources', [])

        # Check for existing source.
        _id = util.gen_id()
        existing = next(
            (s for s in enumerate(json.sources) if s["name"] == name),
            (-1, None))
        if existing:
            raise Exception(
                f'Cannot add source: one already exists with name "{name}".')

        # Generate a record for the source and copy it to the remakes folder.
        source = {
            "id": _id,
            "name": name,
            "type": _type,
            "source": src,
            "remake": f'.remakes/{_id}'
        }
        json.sources += [source]
        util.copy_source(src, f'.remakes/{_id}')

    def copy(self, dest: str, rid: str = None, name: str = None, no_cache: bool = False):
        """
        Create a copy of the source in a new directory.
        """
        if not rid and not name:
            raise Exception(
                'Must include an id or a name to identify a source.')

        source = self.load(rid, name)

        src: str = util.conseq(no_cache, source["source"], source["remake"])
        ours = path.expanduser(path.join('~', src))
        dest = path.join(getcwd(), dest)
        print(f'dest: {dest}, ours: {ours}')
        if not path.exists(ours):
            raise Exception(
                'Invalid source configuration. Check remakes.json for errors.')
        util.copy_source(ours, dest)

    def clip(self, rid: str, name: str, no_cache: bool = False):
        """
        Copy source file contents to the clipboard.
        """
        source = self.load(rid, name)
        if not source:
            raise Exception('Source not found')

        src = util.conseq(no_cache, source["source"], source["remake"])

        print(f'clip src:{src}')
        if not util.file_exists(src):
            return False
        with open(src, 'r') as f:
            pyperclip.copy(f.read())
            print('copied!')
        return True

    def list(self, truncate = False):
        namel = 0
        sourcel = 0
        ridl = 0

        items = iter(self.__json.sources)
        res = []
        i = next(items, None)
        while i != None:
            name: str = i["name"]
            rid: str = i["id"]
            source: str = f'{util.conseq(truncate, util.truncate(i["source"], 40), i["source"])}  '

            if not truncate:
                if i["type"] == 'local':
                    if path.exists(i["source"]):
                        source += util.conseq(
                            path.isfile(i["source"]),
                            '(local - file)', '(local - directory)')
                    else:
                        source += '(local - removed)'
                else:
                    source += f'({i["type"]})'
                # Add items
            res += [[name, rid, source]]

            # Get maxlength
            if len(name) > namel:
                namel = len(name)
            if len(source) > sourcel:
                sourcel = len(source)
            if len(rid) > ridl:
                ridl = len(rid)

            # Next item in the iterable
            i = next(items, None)

        mapped = map(
            lambda i: f'{i[0]}{" " * (namel - len(i[0]))}    {i[1]}{" " * (ridl - len(i[1]))}    {i[2]}{" " * (sourcel - len(i[2]))}',
            res)
        rows = list(mapped)

        return f'''
NAME{" " * (namel - 4)}    ID{" " * (ridl - 2)}    SOURCE{" " * (sourcel - 6)}
{"-" * namel}    {"-" * ridl}    {"-" * sourcel}
''' + ("\n".join(rows)) + '\n'
