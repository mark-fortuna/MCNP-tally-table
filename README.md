Tally Table
==============


***DESCRIPTION***

'tally_table.py' script extracts a simple table from a MCNP output file.
It uses tkinter, regex, matplotlib, subprocess, openpyxl and os libraries.
The script can be converted into a standalone executable (see
section INSTALATION) or the script can simply be run in terminal.

![tally_table_v0 2 18](https://user-images.githubusercontent.com/91466996/150128001-1e023e92-518f-49b1-a8f6-890661d08246.png)


***LIMITATIONS***

Tally table is courently very limited. It only works for cell tallies with only
one output number (not tables). It searches for the keyword "1tally   <tally number>"
skips lines until it gets to the line begining with " cell ". It then takes the number
from the following line.
Flagging cells should be specified with '*' prefix. Example: *1904
All tallies have to be in order. Neutron tallies have to be before gamma tallies.
Example: 1904 1914 4014 *4024 2104 2114, where 2104 and 2114 are gamma tallies.


***USAGE***

User should first select the MCNP output file.

The user defines which tallies should be extracted. By default, the entries
are read from 'default_tallies' file. The 'default_tallies' file can be
modified by user - it can also be empty - it doesn't even have to exist.
Every tally number in 'default_tallies' file should be in its own line.
Read more in MODIFICATION section.

The tallies are shown in a simple table with columns:
  
[tally number]    [tally count]    [tally error]

The table can be exported as a text file (Write to .txt file).
The name is automatically generated: [name].o ----> [name]-tally_table.txt
The tally table can also be saved under a custom name (Save as ...).
Multiple files can be opened by opening an additional tab.
Data from one or more files can be ploted.


***INSTALATION***

**ON WINDOWS WITH ANACONDA**

0. open anaconda powershell promt
0. (If not installed) Install tkinter
0. (If not installed) Install pyinstaller
0. (If not installed) Install matplotlib
1. Go to script directory.
2. Run: pyinstaller --onefile tally_table.py
3. The standalone executable (tally_table.exe) is located in the dist folder.
4. tally_table.exe should work on your machine.
5. (If prefered) Create 'default_tallies' file where tally_table.exe is located.


***MODIFICATION***

If the default_tallies_separator in the 'tally_table.py' script is changed from
'\n' to ' ', then the tally numbers can be in a single line separated by a
space (' '). The choice of separator is up to the user.
