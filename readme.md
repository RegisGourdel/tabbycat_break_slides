# Tabbycat break generator

Version 0.1

This tool is used to create break slides starting from csv files as exported from Tabbycat.

_Warning:_ the tool has only been tested on Linux and might not work without adaptation for other OS types.

## Instructions

The code can be executed from the command line, passing as an argument the name of the folder where tournament files have been downloaded:
```
python break_generator.py "My tournament"
```
in which case the local folder `./My tournament` will be used.
Alternatively a full path to the folder can be specified:
```
python break_generator.py "/home/name/Documents/My tournament"
```
and the tournament's name can be provided as a second argument, e.g.
```
python break_generator.py "/home/name/Documents/My tournament" "Somewhere IV 2023"
```

The generation of slides is done by providing a single argument to the main function, with the following constraints:

-   The background used must be named "background.png".
-   The file with breaking judges must be named "judges.csv".
-   Other csv files in the folder will be used for the break categories, with the file names taken as the break titles.
    For instance, "Novice break.csv" will generate slides identified as the novice break.

## Future changes

- Compatibility with Windows
- Order of the break categories
