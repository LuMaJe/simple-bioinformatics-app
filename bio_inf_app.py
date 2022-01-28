# Started work on 23/01/2022

# A simple bioinformatics program that allows you to import genentic files
# and manipulate them in various ways ready for output.

from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import Notebook
from tkinter import messagebox
from PIL import ImageTk, Image

# Functions

def say_hello():
	messagebox.showinfo('You need help?', "No help to give I'm afraid!")

def MouseClick(event):
	print('The mouse was clicked')

def open_plotter(event):

	# Function to open larger plot of given picture.
	plot_window = Toplevel(root)
	plot_window.title('Expanded view of plot')
	plot_window.geometry('1000x700')

	# ADD IN HERE IF STATEMENT TO ONLY HAVE ONE WINDOW OPEN AT A TIME.
	plot_frame=Frame(plot_window)
	plot_frame.pack()

	expanded_plot = Label(plot_frame, image=large_img)
	expanded_plot.pack()

	close_button = Button(plot_frame, text="Close", command=plot_window.destroy)
	close_button.pack()

def reset():
	input_txt.config(state='normal')
	input_txt.delete(1.0,END)
	input_txt.config(state='disabled')

	output_txt.config(state='normal')
	output_txt.delete(1.0,END)
	output_txt.config(state='disabled')


root = Tk()
# root.geometry('800x500')
root.title('Bioinformatics Program')
root.resizable(False, False)



# Menu bar and File dropdown
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Add file')
filemenu.add_command(label='Save output')
filemenu.add_separator()
filemenu.add_command(label='Quit', command=root.quit)
menubar.add_cascade(label='File', menu=filemenu)

# Help dropdown
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='Help!', command=say_hello)
menubar.add_cascade(label='Help', menu=helpmenu)

root.config(menu=menubar)


# Side frame to inlcude file structure stuff.
# Sticky allows it to stretch to given dimensions
side_frame = Frame(root, width=200, height=470)
side_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)



# Widgets in sideframe

# Tabs at the top of the side-frame
notebook = Notebook(side_frame)
notebook.pack()


# All files frame and tabs.
all_frame = Frame(notebook)
all_frame.pack(fill='both', expand=True)

all_scroll = Scrollbar(all_frame)
all_scroll.pack(side=RIGHT, fill=Y)

all_file_list = Listbox(all_frame, yscrollcommand=all_scroll.set)
all_file_list.insert(1,'Rabbit')
all_file_list.insert(2,'Human')
all_file_list.insert(3,'Bacteria')

all_file_list.pack(side=LEFT, pady=5)
all_scroll.config(command=all_file_list.yview)


# Gene frame and tabs.
gene_frame = Frame(notebook)
gene_frame.pack(fill='both', expand=True)

gene_file_list = Listbox(gene_frame)
gene_file_list.insert(1,'Rabbit')

gene_file_list.pack(pady=5)

gene_scroll = Scrollbar(gene_frame)
gene_scroll.pack(side=RIGHT, fill=Y)
gene_file_list.pack(side=LEFT, pady=5)
gene_scroll.config(command=gene_file_list.yview)


# Protein files frame and tabs.
protein_frame = Frame(notebook)
protein_frame.pack(fill='both', expand=True)

protein_file_list = Listbox(protein_frame)
protein_file_list.insert(1,'Something')
protein_file_list.pack(pady=5)

protein_scroll = Scrollbar(protein_frame)
protein_scroll.pack(side=RIGHT, fill=Y)
protein_file_list.pack(side=LEFT, pady=5)
protein_scroll.config(command=protein_file_list.yview)

notebook.add(all_frame, text='All')
notebook.add(gene_frame, text='Genes')
notebook.add(protein_frame, text='Proteins')


# Plotter widget for showing graphs and images.

# RENAME PICTURE, PERHAPS EVENTUALLY CREATE INTO A FUNCTION.


default_img = ImageTk.PhotoImage(Image.open("dna.jpg").resize((150,150)))
large_img = ImageTk.PhotoImage(Image.open('dna.jpg').resize((900,650)))
corner_plot = Label(side_frame, image=default_img, width=150, height=150)
corner_plot.bind('<Button>', open_plotter)
corner_plot.pack(side=BOTTOM, padx=5, pady=5)



# IMPORT NEW WINDOW (TOPLEVEL) WIDGET TO ALLOW EXPANDED VIEW OF THE PLOT
# POSSIBLY WITH AN OPTION TO SAVE THE PLOT AS A SEPARATE FILE?

# Main frame to include text boxes, buttons and main tools.
main_frame = Frame(root, width=570, height=470)
main_frame.grid(row=0, column=2, sticky='NSEW', padx=5, pady=5)



# Widgets in mainframe.

# Main input Widgets
input_lbl = Label(main_frame, text='Input string', )
input_lbl.grid(row=0, column=0, sticky=NW, padx=5)

input_scroll = Scrollbar(main_frame)
input_scroll.grid(row=1, column=5, sticky='NSW')

input_txt = Text(main_frame, width=70, height=8, yscrollcommand=input_scroll.set)
input_txt.grid(row=1, columnspan=5, pady=5, sticky=N)

input_scroll.config(command=input_txt.yview)
input_txt.insert(INSERT, 'Add your sequence here.')
input_txt.config(state='disabled')



# Middle buttons

gc_btn = Button(main_frame, text="GC content")
gc_btn.grid(row=2, column=0, padx=5, pady=5)

rev_comp_btn = Button(main_frame, text="Reverse Complement")
rev_comp_btn.grid(row=2, column=1, padx=5, pady=5)

protein_btn = Button(main_frame, text="Translate to Protein")
protein_btn.grid(row=2, column=2, padx=5, pady=5)

reset_btn = Button(main_frame, text="Reset", command=reset)
reset_btn.grid(row=2, column=3, padx=5, pady=5)


# Motif Search area

motif_lbl = Label(main_frame, text="Enter motif:")
motif_lbl.grid(row=3, column=0, sticky=E)

motif_entry = Entry(main_frame)
motif_entry.grid(row=3, column=1, columnspan=1, padx=5, pady=5, sticky=W)

# REARRANGE TO ASK TO FIND A K-MER LENGTH MOTIF OR TO SEARCH FOR A SPECIFIC MOTIF
# POSSIBLY WITH A RADIO BUTTON?
# POSSIBLY ADD HAMMING DISTANCE TO THE KMER SEARCH IDEA?

kmer_lbl = Label(main_frame, text="K-mer")
kmer_lbl.grid(row=3, column=2, sticky=W)

kmer_spin = Spinbox(main_frame, from_=0, to_=15, width=5)
kmer_spin.grid(row=3, column=2, padx=5, pady=5)

motif_search = Button(main_frame, text="Search")
motif_search.grid(row=3, column=3)


# Output area

output_lbl = Label(main_frame, text='Output string')
output_lbl.grid(row=4, column=0, sticky=W, padx=5)

output_scroll = Scrollbar(main_frame)
output_scroll.grid(row=5, column=5, sticky='NSW')

output_txt = Text(main_frame, width=70, height=8, yscrollcommand=output_scroll.set)
output_txt.grid(row=5, columnspan=5, padx=5, pady=5)
output_txt.insert(INSERT, 'Your transformed sequence will appear here.')
output_txt.config(state='disabled')
output_scroll.config(command=output_txt.yview)


# Extra info label and misc info

info_lbl = Label(main_frame, text='Extra info appears here')
info_lbl.grid(row=6, column=0, sticky=SW, padx=5, pady=5)


root.mainloop()


# create functions for storing files.
# creating functions for transforming text into output.
