# Remake
A CLI tool for creating your own project templates and code snipits.  

## Usage
Install remake using `pyinstaller` and saving it to a destination tracked by `$Path`. Otherwise, use `py remake.py` instead of `remake(.exe)`.  

```bash
# cache a source
remake add source C:/source/project -n project

# copy to a new destination.
remake copy project C:/source/new-project
```


## Commands
 - `add`: Cache code files and directories for later.
 - `clip`: Add the contents of a stored file to the clipboard.
 - `copy`: Copy a cached source to a new destination.
 - `ls`: List added code sources.
 - `open`: Open a source in file explorer or the default editor.
 - `rm`: Delete an existing source.
 - `update`: cache code files and directories for later.


## Wishlist / TODO  
Remake is still in early stages of development. Here are some things that could make it better:
 - [ ] Install-script and environment configuration for multi-platform support (currently only tested on Windows).
 - [ ] Separate command like `add` to accept user input from the terminal.
 - [ ] Templating with variable injection.
 - [x] ~~`list source/clip` command to see all cached items.~~ implemented as `ls` command.
 - [ ] Ability to add internet/github sources.
 - [ ] Remake script files to run on copy and select senarios.
 - [x] ~~`update/delete source/clip` commands.~~ implemented as `update` and `rm`.
 - [ ] Better console messages (maybe add some color?)
 - [ ] Configure defaults (`ls --truncate`, `open --cached`, etc.)
