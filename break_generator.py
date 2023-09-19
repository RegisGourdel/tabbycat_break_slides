#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import os
import pandas as pd
from math import ceil, floor
import shutil
import tkinter.filedialog
import sys
from warnings import warn

# Number of names by column in the judge break slides
colmax = 5
# Whether to include safety slides
with_safety = True


def tabbycat_import(fname: str) -> pd.DataFrame:
    """
    Import a csv file with break data that has the Tabbycat formatting.

    Parameters
    ----------
    fname : str
        The path to the file to use, containing information on a break.

    Returns
    -------
    df : pd.DataFrame
        The data frame with all useful break data.
    """
    df = pd.read_csv(fname)
    df = df.loc[df['Rk'].notna() & (df['Rk'] != '---------')]
    # The following part might have to be changed to adapt for particular cases
    df = df.loc[df['break'].notna() & (df['break'] != '(different break)')]
    df['break'] = df['break'].astype(int)
    df['Pts'] = df['Pts'].astype(int)
    df['Spk'] = df['Spk'].astype(int)
    return df


def start_slides(tournament: str, dirct_back: str="") -> (str, str):
    """
    Creates the initial parts of both Latex and Quarto files.

    Parameters
    ----------
    tournament : str
        The name of the tournament.
    dirct_back : str, optional
        The variable for the path to the directory with a background picture if
        any. If no value is provided a blank background is used. The default is
        "".

    Returns
    -------
    (str, str)
        The encoding for the first slides, in Quarto and Latex respectively.

    """
    # Prepare the start of the latex file
    ltx_start = """
\\documentclass[20pt, aspectratio=169]{beamer}

\definecolor{myblue}{rgb}{0.2, 0.2, 0.8}

\\usepackage{fontspec}
\\setmainfont{DejaVu Sans}
"""
    if dirct_back:
        ltx_start += """
\\usepackage{graphicx}

\\setbeamercolor{frametitle}{fg=myblue!70!black}
\\setbeamerfont{frametitle}{family=\\normalsize}

\\setbeamertemplate{background}
{\\includegraphics[width=\\paperwidth, height=\\paperheight]{
"""
        ltx_start += dirct_back + ("" if dirct_back[-1] == "/" else "/")
        ltx_start += "background.png}}\n"
    ltx_start += """
\\beamertemplatenavigationsymbolsempty
\\setbeamersize{text margin left=4mm, text margin right=4mm}

\\begin{document}

\\begin{frame} \center
\\huge \\textbf{\\color{myblue} """
    ltx_start += tournament
    ltx_start += """
} \\\\[1em]
\\Large \\textbf{\\color{myblue!50!black} Break announcement}
\\end{frame}

    """

    # Prepare the start of the quarto file
    qmd_start = f"""
---
title: "Break announcement"
subtitle: "{tournament}"
"""
    if dirct_back:
        qmd_start += "\nbackground-image: background.png\n"
    qmd_start += f"""
format:
    revealjs:
        footer: "{tournament} -- Break announcement"
        incremental: true
---
    """
    return ltx_start, qmd_start


def judge_break(judges_info: pd.DataFrame) -> (str, str):
    """
    Generates the slides for the judge break.

    Parameters
    ----------
    judges_info : pd.DataFrame
        The data frame imported from a Tabbycat-generated csv, containing the
        list of breaking judges.

    Returns
    -------
    (str, str)
        The encodings for the slides in Quarto and Latex format respectively.
    """
    ncols = ceil(len(judges_info) / colmax)
    nslides = ceil(ncols / 2)
    # The lines below are used to determine the number of judge names displayed
    # in each column. It is meant to spread the judges over columns used and
    # avoid too much imbalance between the columns or the slides
    v1 = floor(len(judges_info) / ncols)
    col_lengths = [v1 + 1] * (len(judges_info) - v1 * ncols)
    col_lengths += [v1] * (ncols - len(judges_info) + v1 * ncols)
    
    ltxj, qmdj = "", ""
    if with_safety:
        ltxj += """
            \\begin{frame} \center
            \\Large Safety slide judge break
            \\end{frame}
            """
        qmdj += "\n## Safety slide {.center}\n"
    ltxj += "\\begin{frame}\\center\n\\textbf{\\color{myblue}\\Large Judge break}\n\\end{frame}"
    qmdj += "\n# Judge break {.center}\n"
    
    for i in range(ncols):
        if i % 2 == 0:
            if nslides > 1:
                cnt = " (" + str(i // 2 + 1) + "/" + str(nslides) + ")"
            else:
                cnt = ""
            # Create a new slide
            ltxj += "\\begin{frame}{Judge break" + cnt + "} \\small\n"
            qmdj += "## Judge break" + cnt + "\n"
            # Initiate the column environement
            ltxj += "\\begin{columns}\n"
            qmdj += ":::: {.columns}\n"
        
        # Start the column
        ltxj += "\\column{0.5\\textwidth}\n"
        qmdj += '::: {.column width="50%"}\n'
        # Start of the list
        ltxj += "\\begin{itemize}\n"
        qmdj += "\n"
        scol = sum(col_lengths[:i])
        for jdg in judges_info[scol:scol + col_lengths[i]]:
            ltxj += "\\item " + jdg + "\\\\\n"
            qmdj += "- " + jdg + "\n"
        # End of the list and of the column
        ltxj += "\\end{itemize}\n"
        qmdj += "\n:::\n"
        
        if i == ncols - 1 or i % 2 == 1:
            # End the column environment and the slide
            ltxj += "\\end{columns}\n\\end{frame}\n\n"
            qmdj += "::::\n\n"
    return qmdj, ltxj


def pos_str(i: int) -> str:
    """
    Auxiliary function that converts the position of a team to add ranking
    markers.

    Parameters
    ----------
    i : int
        The team position.

    Returns
    -------
    str
        The ranking.
    """
    return ["1st", "2nd", "3rd"][i - 1] if i <= 3 else str(i) + "th"


def break_slides(break_type: str, tab: pd.DataFrame) -> (str, str):
    """
    Function to create the slides for one break category.

    Parameters
    ----------
    break_type : str
        Name of the break category.
    tab : pd.DataFrame
        Data frame containing the break information.

    Returns
    -------
    qmdb : str
        Quarto encoding of the slides.
    ltxb : str
        Latex encoding of the slides.

    """
    ltxb, qmdb = "", ""
    if with_safety:
        ltxb += """
            \\begin{frame} \center
            \\Large Safety slide
            \\end{frame}
            """
        qmdb += "\n## Safety slide  {.center}\n"
    ltxb += "\n\\begin{frame}\\center\n\\textbf{\\color{myblue}\\Large "
    ltxb += break_type + "}\n\\end{frame}"
    qmdb += f"\n# {break_type}\n\n"
        
    for _, team in tab.iterrows():
        # Slide creation and break position
        ltxb += "\\begin{frame}\center\nBreaking "
        ltxb += pos_str(team['break']) + " " + break_type + "\\\\\n"
        qmdb += "## Breaking " + pos_str(team['break']) + " {.center}\n\n"
        # Team name
        ltxb += "\\vspace{1em}\\textbf{\\color{myblue}\\large "
        ltxb += team["team"].replace('&', '\&') + "} \\\\[0.6em]\n"
        qmdb += "### __" + team["team"] + "__\n\n"
        # Team points
        ltxb += "on " + str(team['Pts']) + " team points \\\\[0.6em]\n"
        qmdb += "on " + str(team['Pts']) + " team points \n\n"
        # Speaker points
        ltxb += "and " + str(team['Spk']) + " speaker points.\n"
        qmdb += "and " + str(team['Spk']) + " speaker points \n\n"
        # End the slide
        ltxb += "\\end{frame}\n\n"
        qmdb += "\n"
    return qmdb, ltxb


def main(folder: str="", tournament: str=""):
    """
    The central function to generate the slides: starting from the folder where
    the information is stored it will import all the data and call auxiliary
    functions to generate slides based on it.

    Parameters
    ----------
    folder : str, optional
        The path to the folder containing break info files. The default is "".
    tournament : str, optional
        The name of the tournament. The default is "".

    Returns
    -------
    None.
    """
    if not folder:
        folder = tkinter.filedialog.askdirectory()
    else:
        if not "/" in folder or "\\" in folder:
            if not tournament:
                tournament = folder
            folder = "./" + folder
        
    if not os.path.isdir(folder):
        warn("The path provided is not a folder. Operating with test files.")
        tournament = "Default IV"
        folder = "./test tournament"
    
    if folder[-1] != "/":
        folder = folder + "/"
    if not tournament:
        tournament = folder.split("/")[-2]
    
    ltx, qmd = start_slides(
        tournament, folder if os.path.isfile(folder + "background.png") else "")

    if os.path.isfile(folder + "judges.csv"):
        judges_info = judges_info = pd.read_csv(
            folder + 'judges.csv', header=0)['name'].sort_values()
        if not judges_info.empty:
            qmdj, ltxj = judge_break(judges_info)
            ltx += ltxj
            qmd += qmdj
    # Find all files that contain break data
    break_files = [fl for fl in os.listdir(folder) if fl[-4:] == '.csv' and not
                   'judges' in fl]
    # Loop over break  categories to create the slides
    for fl in break_files:
        qmdb, ltxb = break_slides(fl[:-4], tabbycat_import(folder + fl))
        ltx += ltxb
        qmd += qmdb
    
    ltx += "\\end{document}"
    
    # Write the latex output
    with open(folder + 'break_slides.tex', 'w') as fl:
        fl.write(ltx)
    # Write the quarto output
    with open(folder + 'break_slides.qmd', 'w') as fq:
        fq.write(qmd)
    # Operate a replacement so that spaces don't prevent code execution
    ex_fol = folder.replace(" ", "\ ")
    # Execute lualatex if available
    if shutil.which('lualatex'):
        os.system(f"lualatex -output-directory={ex_fol} {ex_fol}break_slides.tex")
    # Execute Quarto if available
    if shutil.which('quarto'):
        os.system(f"quarto render {ex_fol}break_slides.qmd --to revealjs")


if __name__=='__main__':
    args = [a for a in sys.argv if a != '']
    if len(args) == 3:
        sys.exit(main(args[1], args[2]))
    elif len(args) == 2:
        sys.exit(main(args[1]))
    else:
        sys.exit(main())