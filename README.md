# recake 🍰
**REC**ord and rem**AKE**. A CLI tool for creating your own project templates and code snipits.  

## Usage
Install recake using `pyinstaller` and saving it to a destination tracked by `$Path`. Otherwise, use `py recake.py` instead of `recake(.exe)`.  

```bash
# cache a source
recake add C:/source/project -n template

# copy to a new destination.
recake copy template C:/source/new-project
```

### Commands
 - `add`: Cache code files and directories for later.
 - `clip`: Add the contents of a stored file to the clipboard.
 - `copy`: Copy a cached source to a new destination.
 - `ls`: List added code sources.
 - `open`: Open a source in file explorer or the default editor.
 - `rm`: Delete an existing source.
 - `update`: cache code files and directories for later.


## Contributing
Feel free to tackle one of the items below, or suggest your own additions!

### Wishlist / TODO  
recake is still in early stages of development. Here are some things that could make it better:
 - [ ] Templating with variable injection.
 - [ ] Install-script and environment configuration for multi-platform support (currently only tested on Windows).
 - [ ] Separate command like `add` to accept user input from the terminal.
 - [x] ~~`list source/clip` command to see all cached items.~~ implemented as `ls` command.
 - [ ] Ability to add internet/github sources.
 - [ ] recake script files to run on copy and select senarios.
 - [x] ~~`update/delete source/clip` commands.~~ implemented as `update` and `rm`.
 - [ ] Better console messages (maybe add some color?)
 - [ ] Configure defaults (`ls --truncate`, `open --cached`, etc.)

### Installation
**Recomended**: use `pyinstaller` to create an executable:
 1. `pip install pyinstaller`
 2. `pyinstaller recake.py -F --distpath C:\PATH\aware\directory`
 3. `recake --version`
