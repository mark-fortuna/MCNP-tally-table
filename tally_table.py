# script for exporting tally meassurements to neat table
# uses GUI to select files and display table

import tkinter as tk
import tkinter.filedialog as fd
import re

# SCRIPT PARAMETERS
# **************************************************************************
debug = True  # turn to 'True' to debug program - to 'False' to not debug
pad_in = 5
pad_out = 2
default_tallies_separator = '\n' # each tally in new line
# **************************************************************************

root = tk.Tk()
root.title('Tally to table')
root.geometry('500x800')

# see if 'default_tallies' exists
# if it doesn't leave entry field blank
try:
    with open('default_tallies', 'r') as f:
        if debug: print('default_tallies file present')
        dt = open('default_tallies', 'r')
        default_tallies = dt.read().split(default_tallies_separator)
except FileNotFoundError:
    if debug: print('default_tallies file is not present')
    default_tallies = ''


lines = []
input_name = ''
def open_file():
    global lines
    global input_name
    input_name = fd.askopenfilename(defaultextension='.o', title='Select MCNP output file')
    f = open(input_name, 'r')
    lines = f.readlines()
    f.close()
    if debug: print('FILE HAS {} LINES'.format(len(lines)))
    tk.Label(file_frame, text=input_name).pack()

file_frame = tk.LabelFrame(root, text='')
file_frame.pack()
select_button = tk.Button(file_frame, text='Select MCNP output file', padx=pad_in,pady=pad_in, command=open_file)
select_button.pack(padx=pad_out,pady=pad_out)

# define tallies of interest
entry_frame = tk.LabelFrame(root, text='', padx=2, pady=2)
entry_frame.pack(padx=5, pady=5)
tk.Label(entry_frame, text='Enter tallies of interest:').grid(row=0,column=0)
blank = ''
for i in range(90): blank += ' '
tk.Label(entry_frame, text=blank).grid(row=0,column=1)
def_tally = tk.Entry(entry_frame, width = 70)
def_tally.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
def_tally.insert(0, default_tallies)
tk.Label(entry_frame, text="Default tallies are read from 'default_tallies' file.").grid(row=2, column=0, columnspan=2)

tally = []
def read_tally():
    global tally
    global read_button
    global def_tally
    global lines

    input_tally = def_tally.get()
    # we must convert input_tally to string list of tally numbers!
    tally_number = input_tally.split(' ')   # only for TESTING - not universal enough
    N = len(tally_number)
    if debug: print(tally_number)
    # matrix with tally name, tally count and tally error
    tally = [[i for i in tally_number],[None for i in tally_number],[None for i in tally_number]]

    i = 0
    for k in range(len(tally_number)):
        form = '1tally(\s+)' + tally_number[k] + '(.*)'
        found = None
        while found == None:
            found = re.search(form, lines[i])
            i += 1
        if debug: print('TALLY INFO BEGINS AT LINE {}: {}'.format(i, lines[i-1][:-1]))   # [:-1] is added to remove '\n' from string
        # now we know at wich line tally info begins
        # the line before tally count begins with ' cell '
        # the line with tally count begins with whitespace
        # tally count and error are sepperated with white space
        found2 = None
        while found2 == None:
            found2 = re.search('\scell(\s+)', lines[i])
            i += 1
        # line i has tally count and tally error
        t = re.split('\s+',lines[i])
        if debug: print('TALLY COUNT: {}  TALLY ERROR: {}\n\n'.format(t[1], t[2]))
        tally[1][k] = float(t[1]) # tally count
        tally[2][k] = float(t[2]) # tally error
        
        if debug: print('\n\n', tally)

    # display tally
    tk.Label(table_frame, text='Tally number').grid(row=0, column=0,padx=5)
    tk.Label(table_frame, text='Count').grid(row=0, column=1,padx=5)
    tk.Label(table_frame, text='Error').grid(row=0, column=2,padx=5)
    for i in range(N):
        tk.Label(table_frame, text=tally[0][i]).grid(row=i+1,column=0,padx=5)
        tk.Label(table_frame, text='{:e}'.format(tally[1][i])).grid(row=i+1,column=1,padx=5)
        tk.Label(table_frame, text=str(tally[2][i])).grid(row=i+1,column=2,padx=5)
    read_button.destroy()

read_button = tk.Button(root, text='Read tally',padx=pad_in,pady=pad_in, command=read_tally)
read_button.pack(padx=pad_out,pady=pad_out)

table_frame = tk.LabelFrame(root, text='TALLY TABLE', padx=10,pady=10)
table_frame.pack()

# command to write tally matrix to new file
def write_to_file():
    global input_name
    global tally
    name = input_name.split('.')[0]
    output = name + '-tally_table.txt'
    o = open(output, 'w')
    lines = [None for i in tally[0]]
    for i in range(len(lines)):
        lines[i] = tally[0][i] + '\t' + '{:e}'.format(tally[1][i]) + '\t' + '{}'.format(tally[2][i]) + '\n'
    o.writelines(lines)
    o.close()

def save_as():
    global tally
    output_name = fd.asksaveasfilename(defaultextension='.txt', title='Save as ...')
    o2 = open(output_name, 'w')
    lines = [None for i in tally[0]]
    for i in range(len(lines)):
        lines[i] = tally[0][i] + '\t' + '{:e}'.format(tally[1][i]) + '\t' + '{}'.format(tally[2][i]) + '\n'
    o2.writelines(lines)
    o2.close()

write_button = tk.Button(root, text='Write to .txt file', padx=pad_in,pady=pad_in, command=write_to_file)
write_button.pack(padx=pad_out,pady=pad_out)
save_as_button = tk.Button(root, text='Save as ...', padx=pad_in,pady=pad_in, command=save_as)
save_as_button.pack(padx=pad_out,pady=pad_out)

root.mainloop()