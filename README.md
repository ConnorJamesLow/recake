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


## Features
 - `add source`: cache code files and directories for later.
 - `copy`: copy a cached source to a new destination.
 - `clip`: Add the contents of a stored file to the clipboard.

## Wishlist / TODO  
Remake is still in early stages of development. Here are some things that could make it better:
 - [ ] Install-script and environment configuration for multi-platform support (currently only tested on Windows).
 - [ ] Separate `add clip` command that could also accept user input from the terminal.
 - [ ] Templating with variable injection.
 - [ ] `list source/clip` command to see all cached items.
 - [ ] Ability to add internet/github sources.
 - [ ] Remake script files to run on copy and select senarios.
 - [ ] `update/delete source/clip` commands.
 - [ ] Better console messages (maybe add some color?)
