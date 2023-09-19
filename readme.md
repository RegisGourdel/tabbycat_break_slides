# Tabbycat break generator

Version 0.2

This tool is used to create break slides starting from csv files as exported from Tabbycat.
It has to outputs:

1.  PDF slides generated with LuaLatex.
2.  RevealJS slides, in html format, generated with [Quarto](https://quarto.org/).

It is necessary to have at least one of these tools installed in order to the program to produce a final output.

_Warning:_ the tool has only been tested on Linux and might not work without adaptation for other OS types.

Note that the pdf generation has a limited compatibility with non-latin character, and that any change in the font is likely to further reduce that compatibility, while the RevealJS one has a very large coverage.

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

## Future changes (if time allows)

- Order of the break categories
- Compatibility with Windows
- Pass `with_safety` as a command-line argument
