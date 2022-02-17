# Started work on 23/01/2022

# A simple bioinformatics program that allows you to import genentic files
# and manipulate them in various ways ready for output.

from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import Notebook
from tkinter import messagebox
from PIL import ImageTk, Image
import Bio
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import GC
import Bio.SeqUtils



# =================================================================================
# Dictionary to keep track of what functions have run

run_list_dict = {'input_deleted': False,
				'plotter_open': False}

# Functions

def say_hello():
	messagebox.showinfo('You need help?', "No help to give I'm afraid!")

def MouseClick(event):
	print('The mouse was clicked')

def entry_click(event):
	if run_list_dict['input_deleted'] == False:
		input_txt.config(state='normal')
		input_txt.delete(1.0, END)
	run_list_dict['input_deleted'] = True


def open_file():
	filepath = fd.askopenfilename()
	file = open(filepath, 'r')
	file_first_line = file.readline().strip()
	file_data = file.readlines()

	# CHANGE THIS ALGORITHM AS IT'S TOO SLOW FOR THE PROGRAM. USING TOO MUCH MEMORY.
	# MAYBE THIS SHOULD BE PART OF THE DATABASE IDEA ALSO SO THAT THE INSERTED SEQUENCE IS SAVED IN THE DATABASE INSTEAD OF IN THE SCRIPT. 
	text_to_insert = ''
	for x in range(1,len(file_data)):
		line = file_data[x].strip('\n')
		text_to_insert += line

	text_inserter(input_txt, text_to_insert)
	info_var.set(file_first_line)
	info_lbl.config(text=info_var.get())
	# REVIEW THIS TO BE ABLE TO CHANGE THE INFO LABEL BELOW. BASED ON THE STRINGVAR.

	run_list_dict['input_deleted'] = True

	file.close()


# Function to open larger plot of given picture.
def open_plotter(event):

	if run_list_dict['plotter_open'] == False:
		plot_window = Toplevel(root)
		plot_window.title('Expanded view of plot')
		plot_window.geometry('1000x700')

		plot_frame=Frame(plot_window)
		plot_frame.pack()

		expanded_plot = Label(plot_frame, image=large_img)
		expanded_plot.pack()

		# FIGURE OUT HOW TO RE FALSIFY THE PLOTTER_OPEN BOOLEAN ONCE THE PLOTTER WINDOW HAS BEEN CLOSED
		# ALLOWING FOR THE PLOTTER TO BE OPENED AND CLOSED MULTIPLE TIMES

		close_button = Button(plot_frame, text="Close", command=plot_window.destroy)
		close_button.pack()
		run_list_dict['plotter_open'] = True
	else:
		messagebox.showinfo('Window already open', 'Please close the previous plotter window before opening another.')

def reset():
	input_txt.config(state='normal')
	input_txt.delete(1.0,END)
	input_txt.config(state='disabled')

	output_txt.config(state='normal')
	output_txt.delete(1.0,END)
	output_txt.config(state='disabled')



def text_inserter(textbox, insert_string):
	
	textbox.config(state='normal')
	textbox.delete(1.0,END)
	textbox.insert(INSERT, insert_string)
	textbox.config(state='disabled')


def find_gc_content():
	input_string = input_txt.get('1.0', END).strip().upper()
	input_intro = input_string[:10]
	gc_string = f'The GC content for sequence "{input_intro}..." is: {round(GC(input_string),2)} %\nLength of Sequence: {len(input_string)}'
	text_inserter(output_txt, gc_string)


def reverse_comp():
	input_string = input_txt.get('1.0', END).strip().upper()
	input_dna = Seq(input_string)
	rev_comp_string = input_dna.complement()

	rev_comp_output_string = f'Length of Sequence: {len(input_string)} \nThe Reverse Complement is: \n\n{rev_comp_string}'
	text_inserter(output_txt, rev_comp_output_string)


def translate():
	input_string = input_txt.get('1.0', END).strip().upper()
	input_dna = Seq(input_string)
	
	output_protein = input_dna.transcribe().translate()
	protein_string = f'Length of DNA Sequence: {len(input_string)} \nLength of Protein sequence: {len(output_protein)} \nThe translated protein sequence is: \n\n{output_protein}'		
	text_inserter(output_txt, protein_string)

# Chooses between the motif or the kmer search functions and then runs either one.
def search_button():
	choice = search_var.get()
	if choice == 1:
		search_motif()
	elif choice == 2:
		search_kmer()
	else:
		messagebox.showinfo('Error', 'Please select a search parameter.')
		


# THIS NEEDS TO RETRIEVE THE KMER NUMBER FROM THE SPINWHEEL AND SEARCH THE SEQUENCE FOR ALL KMERS OF THAT LENGTH
# AS WELL AS GIVING THE MOST POPULAR KMER. (POSSIBLY HIGHLIGHTING THEM SIMILAR TO MOTIF SEARCH)
def search_kmer():
	k = int(kmer_spin.get())
	input_string = input_txt.get('1.0', END).strip().upper()
	kmer_names = frequent_words(input_string, k)[0]
	kmer_frequency = frequent_words(input_string, k)[1]
	
	kmer_output_string = f'The most common {k}-mer is "{kmer_names[0]}" which was found: {kmer_frequency} times.'
	if len(kmer_names) == 1:
		text_inserter(output_txt, kmer_output_string)

	elif len(kmer_names) > 1:
		kmer_output_extra = f'Other {k}-mers found an equal number of times... \n\n{kmer_names[1:]}'
		kmer_output_string = kmer_output_string + '\n\n' + kmer_output_extra
		text_inserter(output_txt, kmer_output_string)



def frequency_map(text, k):
	freq = {}
	n = len(text)
	for i in range(n - k +1):
		pattern = text[i:i + k]
		if not pattern in freq:
			freq[pattern] = 1
		else:
			freq[pattern] += 1
	return freq

def frequent_words(text, k):
	words = []
	freq_map = frequency_map(text, k)
	max_val = max(freq_map.values())
	for key in freq_map:
		if freq_map[key] == max_val:
			words.append(key)
	return words, max_val

# THIS IS TO BE TAKEN OUT AND MADE INTO SEPARATE FILE FOR ALL FUNCTIONS.
def pattern_count(text, pattern):
	count = 0
	for i in range(len(text) - len(pattern) + 1):
		if text[i:i+len(pattern)] == pattern:
			count += 1
	return count

def search_motif():
	input_string = input_txt.get('1.0', END).strip().upper()
	input_intro = input_string[:10]
	motif = motif_entry.get().strip().upper()
	clean_motif = False

	if len(input_string) > 0:
		for letter in motif:
			if letter not in 'ACGT':
				messagebox.showinfo('Motif input error', 'Please only enter base nucleotide letters: A,C,G or T')
				return
			else:
				clean_motif = True
				motif_count = pattern_count(input_string, motif)
				motif_string = f'The motif {motif} is found {motif_count} times in the the sequence starting: "{input_intro}...".\n\n' + input_string
				text_inserter(output_txt, motif_string)
				# output_txt.config(state='normal')
				# highlighter(motif)
	elif len(input_string) == 0:
		messagebox.showinfo('Search error', 'Please enter a motif.')

def save_output_file():
	pass


	# ADD IN AND LEARN ABOUT TEXTBOX TAGMARKS, TAGGING AT THE LOCATIONS OF THE MOTIF INDEXES
	# THEN CHANGE ALL THE FONT COLOURS (AND LOWERCASE) FOR ALL THE TAGS?

# def hi1(motif):
# 	location = output_txt.search(motif, '1.0', END)
# 	print(location)

# 	output_txt.tag_add('highlight', '1.0', '1.11')
# 	output_txt.tag_config('highlight', foreground='red')


# def highlighter(motif):

# 	output_txt.tag_config('highlight', foreground='red')
# 	offset = '+%dc' % len(motif)

# 	start_pos = input_txt.find(motif, '1.0', END)

# 	while start_pos:
# 		end_pos = start_pos + offset
# 		print(start_pos, end_pos)
# 		input_txt.tag_add('highlight', start_pos, end_pos)
# 		start_pos = input_txt.find(motif, end_pos, END)



# =================================================================================
# =================================================================================


root = Tk()
root.title('Bioinformatics Program')
root.resizable(False, False)

input_var = StringVar(value='Add your sequence here...')
info_var = StringVar(value='Extra info will appear here...')
search_var = IntVar()
search_var.set(1)


# Menu bar and File dropdown
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Add file', command=open_file)
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

default_img = ImageTk.PhotoImage(Image.open("dna.jpg").resize((150,150)))
large_img = ImageTk.PhotoImage(Image.open('dna.jpg').resize((900,650)))
corner_plot = Label(side_frame, image=default_img, width=150, height=150)
corner_plot.bind('<Button>', open_plotter)
corner_plot.pack(side=BOTTOM, padx=5, pady=5)


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
input_txt.insert(INSERT, 'Add your sequence here...')
input_txt.bind('<Button-1>', entry_click)
input_txt.config(state='disabled', font=('System'))



# Middle buttons

gc_btn = Button(main_frame, text="GC content", command=find_gc_content)
gc_btn.grid(row=2, column=0, padx=5, pady=5)

rev_comp_btn = Button(main_frame, text="Reverse Complement", command=reverse_comp)
rev_comp_btn.grid(row=2, column=1, padx=5, pady=5)

protein_btn = Button(main_frame, text="Translate to Protein", command=translate)
protein_btn.grid(row=2, column=2, padx=5, pady=5)

reset_btn = Button(main_frame, text="Reset", command=reset)
reset_btn.grid(row=2, column=3, padx=5, pady=5)


# Motif Search area

motif_rad = Radiobutton(main_frame, text='Motif search:', variable=search_var, value=1)
motif_rad.grid(row=3,column=0)

motif_entry = Entry(main_frame)
motif_entry.grid(row=3, column=1, columnspan=1, padx=5, pady=5, sticky=W)

kmer_radio = Radiobutton(main_frame, text="K-mer search:", variable=search_var, value=2)
kmer_radio.grid(row=3, column=2, sticky=W)

kmer_spin = Spinbox(main_frame, from_=0, to_=15, width=5)
kmer_spin.grid(row=3, column=2, padx=5, pady=5, sticky=E)

motif_search_btn = Button(main_frame, text="Search", command=search_button)
motif_search_btn.grid(row=3, column=3)


# Output area

output_lbl = Label(main_frame, text='Output string')
output_lbl.grid(row=4, column=0, sticky=W, padx=5)

output_scroll = Scrollbar(main_frame)
output_scroll.grid(row=5, column=5, sticky='NSW')

output_txt = Text(main_frame, width=70, height=8, yscrollcommand=output_scroll.set)
output_txt.grid(row=5, columnspan=5, padx=5, pady=5)
output_txt.insert(INSERT, 'Your transformed sequence will appear here.')
output_txt.config(state='disabled', font=('System'))
output_scroll.config(command=output_txt.yview)


# Extra info label and misc info

info_lbl = Label(main_frame, text=info_var.get())
info_lbl.grid(row=6, columnspan=5, sticky=SW, padx=5, pady=5)


root.mainloop()


# create functions for storing files.
# creating functions for transforming text into output.
