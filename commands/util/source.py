from os import remove, getcwd
import pyperclip
from commands.util.jef import subjectify, Observer
from commands.util.util import ensure_attr, gen_id, randint, conseq, file_exists, copy_source, get_jpath
from shutil import Error, rmtree
from os.path import exists, isdir, isfile, join, expanduser
from datetime import datetime


class Source:
    def __init__(
            self,
            src: str = None,
            id: str = None,
            name: str = None,
            _type: str = None):
        self.__state = None
        self.__source = src
        self.__id = id
        self.__name = name
        self.__type = _type
        self.__remake = None

        # Check for existing source
        is_loaded = False
        if id:
            is_loaded = self.load(id=id)
        if not is_loaded and name:
            is_loaded = self.load(name=name)

        if not self.__source:
            raise Exception('Must include the src parameter')

    def __gen_id(self) -> str:
        today = datetime.now()
        res = ''
        for c in f'{today.toordinal()}':
            res += chr(int(c, 10) + 65)
        res += '_'
        i = 0
        while i < 10:
            i += 1
            res += chr(randint(97, 122))
        self.__id = res

    def load(self, id: str = None, name: str = None) -> str:
        """
        Find the state of the source using the name or the id.
        """
        if not id or name:
            return False
        #  Load the state file
        json = subjectify(get_jpath())

        # Load state from remakes.json file
        ensure_attr(json, 'sources', [])

        # Try to find the state by Id
        state: Observer = next(
            (s for s in json.sources if s["id"] == self.__id), None)
        if not state:
            # If not found, try again by name
            state = next(
                (s for s in json.sources if s["name"] == self.__name), None)

        # If no state found, return False
        if not state:
            return False

        # Load the state
        self.__state = state
        self.__source = state["source"]
        self.__id = state["id"]
        self.__name = state["name"]
        self.__type = state["type"]
        self.__remake = state["remake"]
        return True

    def save(self, name: str = None, _type: str = None):
        """
        Create local copy of the source in the `.remakes/` cache.
        """
        json = subjectify(get_jpath())
        ensure_attr(json, 'sources', [])

        # Try to find an existing source with that name
        name = conseq(name, name, self.__name)
        sources = json.sources

        index, existing = next(
            ((i, s) for i, s in enumerate(sources) if s["name"] == name),
            (-1, None))
        if existing:
            self.__id = existing["id"]
            if isdir(existing["remake"]):
                rmtree(existing["remake"])
            elif isfile(existing["remake"]):
                remove(existing["remake"])
            del sources[index]
            json.sources = sources
        else:
            self.__gen_id()

        # Generate a record for the source and copy it to the remakes folder.
        src = self.__source
        source = {
            "id": self.__id,
            "name": conseq(name, name, self.__name),
            "type": conseq(_type, _type, self.__type),
            "source": src,
            "remake": f'.remakes/{self.__id}'
        }
        json.sources += [source]
        copy_source(src, f'.remakes/{self.__id}')

    def remake(self, dest: str, no_cache: bool = False):
        """
        Create a copy of the source in a new directory.
        """
        state: Observer = self.__state
        src: str = self.__source
        ours: str = ''
        if state:
            ours = conseq(no_cache, src, state["remake"])
        else:
            ours = conseq(no_cache, src, self.__remake)

        ours = expanduser(join('~', ours))
        dest = join(getcwd(), dest)
        print(f'dest: {dest}, ours: {ours}')
        if not exists(ours):
            raise Exception(
                'Invalid source configuration. Check remakes.json for errors.')
        copy_source(ours, dest)

    def clip(self, no_cache=False):
        """
        Copy source file contents to the clipboard.
        """
        src = conseq(
            no_cache,
            self.__source,
            conseq(self.__state["remake"], self.__state["remake"], self.__remake))

        print(f'clip src:{src}')
        if not file_exists(src):
            return False
        with open(src, 'r') as f:
            pyperclip.copy(f.read())
            print('copied!')
        return True

    def remove(self):
        """
        Remove the source from `remakes.sources`.
        """
        raise NotImplementedError()


def find_source(attr, value):
    state = subjectify(get_jpath())
    ensure_attr(state, 'sources', [])
    el = next((getattr(i, attr) == value for i in state.sources), None)
    if not el:
        return None
    return el


def load(id: str = None, name: str = None) -> str:
    """
    Find the state of the source using the name or the id.
    """
    if not id or name:
        return False
    #  Load the state file
    json = subjectify(get_jpath())

    # Load state from remakes.json file
    ensure_attr(json, 'sources', [])

    # Try to find the state by Id
    state: Observer = next(
        (s for s in json.sources if s["id"] == id), None)
    if not state:
        # If not found, try again by name
        state = next(
            (s for s in json.sources if s["name"] == name), None)

    # If no state found, return False
    return state


def add_source(src: str = None, name: str = None, _type: str = None):
    """
    Create local copy of the source in the `.remakes/` cache.
    """
    if not src:
        raise Exception('Must include the src parameter')

    json = subjectify(get_jpath())
    ensure_attr(json, 'sources', [])

    # Check for existing source.
    id = gen_id()
    existing = next(
        (s for s in enumerate(json.sources) if s["name"] == name),
        (-1, None))
    if existing:
        raise Exception(f'Cannot add source: one already exists with name "{name}".')

    # Generate a record for the source and copy it to the remakes folder.
    source = {
        "id": id,
        "name": name,
        "type": _type,
        "source": src,
        "remake": f'.remakes/{id}'
    }
    json.sources += [source]
    copy_source(src, f'.remakes/{id}')

