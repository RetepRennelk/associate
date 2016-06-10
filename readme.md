# Associate ideas

Randomly combine and display ideas from disparate text files. Surprise yourself! ;)

## Example
```
python associate.py heros.txt verbs.txt villains.txt
```
- Select one entry from each of the three files

```
python associate.py heros.txt verbs.txt villains.txt -N_layers 2
```
- Build one list from the three files and select two items at random

## Keys
- 'h', 'v': Switch to horizontal/vertical layout
- '+', '-': Increase font size
- '1','2', ..., '9': Build a single list from all files and select the chosen number of items
- '0': Revert to selecting one entry per file each

## Tested with 
- Windows 7, 10
- Python 3.4
- Pyqt5
