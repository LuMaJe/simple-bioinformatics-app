# An app that takes a word and adds it to a text box.
from tkinter import *
from tkinter import filedialog as fd


root = Tk()
root.geometry('800x500')
root.title('My New App')
root.resizable(False, False)


def button_print():
	text_1 = entry1.get()
	text_2 = entry2.get()
	final_text = text_1 + ' ' + text_2
	big_box.delete(1.0,END)
	big_box.insert(END, final_text)

	return None

def open_file():

	filetypes = (('text files', '*.txt'), ('All files', '*.*'))
	file = fd.askopenfile(title='Open a new file', filetypes=filetypes)

	file_text = file.readlines()

	big_box.delete(1.0, END)
	
	if var.get() == 1:
		for line in file_text:
			if line[0] == '>':
				big_box.insert(END, line)
	elif var.get() == 2:
		for line in file_text:
			splitline = line.split('\n')
			print(splitline)
			big_box.insert(END, line)

var = IntVar()

frame = Frame(root)

label_1 = Label(frame, text='Enter first thing here...').grid(row=0, column=0)
entry1 = Entry(frame, width=40)
entry1.grid(row=1, column=0)
label_2 = Label(frame, text='Enter second thing here...').grid(row=0, column=2)
entry2 = Entry(frame, width=40)
entry2.grid(row=1, column=2)


btn_1 = Button(frame, text='Print this...', command=button_print).grid(row=3, column=0)
btn2 = Button(frame, text='Open a new file', command=open_file).grid(row=3, column=1)

rad_id = Radiobutton(frame, text="Show ID's", variable=var, value=1)
rad_data = Radiobutton(frame, text='Show genetic data', variable=var, value=2)
rad_id.grid(row=3, column=2)
rad_data.grid(row=3, column=3)

big_box = Text(frame)
big_box.grid(row=4, columnspan=3, sticky='ew')

frame.pack(expand=True)
root.mainloop()

# make a selector that loads the files from a certain folder and shows them in a window, ready to pick.
