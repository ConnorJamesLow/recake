import click
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

        if not (rid or name):
            return None

        # Try to find the state by Id
        state: Observer = next(
            (s for s in json.sources if s["id"] == rid),
            None)

        if not state:
            # If not found, try again by name
            state = next(
                (s for s in json.sources if s["name"] == name),
                None)

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

        src = util.calculate_path(util.conseq(
            no_cache, source["source"], source["remake"]))

        if not util.file_exists(src):
            return False
        with open(src, 'r') as f:
            pyperclip.copy(f.read())
        return True

    def ls(self, truncate: bool = False, *args):
        """
        List remake sources.
        """
        items = iter(self.__json.sources)
        rows = []
        lengths = {}

        i = next(items, None)
        while i != None:
            dict = {}
            for p in args:
                if p not in i.keys():
                    return f'Error: "{p}" is not an attribute of $.sources.'
                val = util.conseq(truncate, util.truncate(i[p], 33), i[p])
                dict[p] = val
                if p not in lengths.keys() or len(val) > lengths[p]:
                    lengths[p] = len(val)
            rows += [dict]
            i = next(items, None)

        # Add headers
        res = ['']
        res += [(' ' * 4).join(map(lambda k: k +
                                   (' ' * (lengths[k] - len(k))), args))]

        # Add divider line
        res += [(' ' * 4).join(map(lambda k: '-' * (lengths[k]), args))]
        # Add rows:
        for r in rows:
            res += [(' ' * 4).join(map(lambda k: r[k] +
                                       (' ' * (lengths[k] - len(r[k]))), args))]

        return '\n'.join(res) + '\n'

    def open(self, noi: str = None, no_cache: bool = False):
        """
        Open a source in an editor or the fs.

        noi - name or id
        """
        source = self.load(noi, noi)
        if not source:
            raise Exception(
                f'Not found. "{noi}" does not match any source ids or names.')

        src = util.calculate_path(
            util.conseq(no_cache, source["source"], source["remake"]))
        return click.launch(src)
