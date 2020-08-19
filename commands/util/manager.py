from commands.util.util import ensure_attr
import click
from os import getcwd, path
from commands.util import util
from commands.util.jef import subjectify, Observer
import pyperclip


class Manager:
    def __init__(self):
        self.__json = subjectify(util.get_jpath())

        # Load the state
        util.ensure_attr(self.__json, 'sources', [])

    def load(self, noi: str = None):
        """
        Find the state of the source using the name or the id.

        noi - "name or id"
        """
        json = self.__json

        if not noi:
            return None

        # Try to find the state by Id
        state: Observer = next(
            (s for s in json.sources if s["id"] == noi),
            None)

        if not state:
            # If not found, try again by name
            state = next(
                (s for s in json.sources if s["name"] == noi),
                None)

        # If no state found, return False
        return state

    def add(self, src: str = None, name: str = None, _type: str = None):
        """
        Create local copy of the source in the `.recakes/` cache.
        """
        if not src:
            raise Exception('Must include the src parameter')

        json = self.__json
        util.ensure_attr(json, 'sources', [])

        # Check for existing source.
        _id = util.gen_id()
        if next((s for s in iter(json.sources) if s["name"] == name), None):
            raise Exception(
                f'Cannot add source: one already exists with name "{name}".')

        # Generate a record for the source and copy it to the recakes folder.
        source = {
            "id": _id,
            "name": name,
            "type": _type,
            "source": util.calculate_path(src),
            "recake": f'.recakes/{_id}'
        }
        json.sources += [source]
        util.copy_source(src, f'.recakes/{_id}')

    def update(self, noi: str):
        """
        Recopy the content from the source to the cached recake.
        """
        source = self.load(noi)
        if not source:
            raise Exception(
                f'Not found. "{noi}" does not match any source ids or names.')
        util.copy_source(source["source"], source["recake"], True)

    def clear(self, noi: str, rm: bool = False):
        """
        Clear the cached source. If rm is set, also delete the record.
        """
        cache = self.__json.sources

        # Find source
        source = self.load(noi)
        if not source:
            raise Exception(
                f'Not found. "{noi}" does not match any source ids or names.')

        # Delete cached files
        util.uncopy_source(source["recake"])
        if not rm:
            return

        # Remove from list TODO
        sources = enumerate(cache)
        i = next((i for i, s in sources if s is source), None)

        del cache[i]
        self.__json.sources = cache

    def copy(self, dest: str, noi: str = None, no_cache: bool = False):
        """
        Create a copy of the source in a new directory.
        """
        if not noi:
            raise Exception(
                'Must include an id or a name to identify a source.')

        source = self.load(noi)

        # Get the src to copy from.
        src: str = util.conseq(no_cache, source["source"], source["recake"])
        ours = path.expanduser(path.join('~', src))
        dest = path.join(getcwd(), dest)

        # Verify the src requested actually exists.
        if not path.exists(ours):
            raise Exception(
                'Invalid source configuration. Check recakes.json for errors.')
        util.copy_source(ours, dest)

    def clip(self, noi: str, no_cache: bool = False):
        """
        Copy source file contents to the clipboard.
        """
        source = self.load(noi)
        if not source:
            raise Exception(
                f'Not found. "{noi}" does not match any source ids or names.')

        src = util.calculate_path(util.conseq(
            no_cache, source["source"], source["recake"]))

        if not util.file_exists(src):
            return False
        with open(src, 'r') as f:
            pyperclip.copy(f.read())
        return True

    def ls(self, truncate: bool = False, *args):
        """
        List recake sources.
        """
        if len(self.__json.sources) < 1:
            return 'No sources'

        items = iter(self.__json.sources)
        rows = []
        lengths = {}

        # Add to list until there are no more items in the iterable.
        i = next(items, None)
        while i != None:
            dict = {}
            for p in args:

                # Verify the property is present on the sources object
                if p not in i.keys():
                    return f'Error: "{p}" is not an attribute of $.sources[n].'
                val = util.conseq(truncate, util.truncate(i[p], 33), i[p])
                dict[p] = val

                # Calcualte the longest value for this property.
                if p not in lengths.keys() or len(val) > lengths[p]:
                    lengths[p] = len(val)
            rows += [dict]
            i = next(items, None)

        # Add headers
        res = ['']
        res += [(' ' * 4).join(
            map(lambda k: k + (' ' * (lengths[k] - len(k))), args)
        )]

        # Add divider line
        res += [(' ' * 4).join(
            map(lambda k: '-' * (lengths[k]), args)
        )]

        # Add rows:
        for r in rows:
            res += [(' ' * 4).join(
                map(lambda k: r[k] + (' ' * (lengths[k] - len(r[k]))), args)
            )]

        return '\n'.join(res) + '\n'

    def open(self, noi: str, cache: bool = False):
        """
        Open a source in an editor or the fs.

        noi - name or id
        """
        source = self.load(noi)
        if not source:
            raise Exception(
                f'Not found. "{noi}" does not match any source ids or names.')

        # Find the path to the source to open.
        src = util.calculate_path(
            util.conseq(cache, source["recake"], source["source"]))
        return click.launch(src)

    def load_ignore(self):
        """
        Create the ignore file if necessary
        """
        if not path.exists(self.__json.ignore):
            default_filename = '.reignore'
            ensure_attr(self.__json, 'ignores', default_filename)
            ignores = self.json.ignore


    def add_ignore(self, line):
        """

        """