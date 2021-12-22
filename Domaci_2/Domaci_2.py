from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import tkinter.scrolledtext as st
import docx2txt
from db import Database

db = Database('store.db')

#Populate List
def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)
#Add Item
def add_item():
    if part_text.get() == '' or retailer_text.get() == '' :
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(part_text.get(), customer_entry.get(), retailer_text.get(), price_entry.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (part_text.get(), customer_entry.get(), retailer_text.get(), price_entry.get()))
    populate_list()
#Select from the list
def select_name():
    global selected_item
    index = parts_list.curselection()[0]
    selected_item = parts_list.get(index)
#Select  
def select_item(event):
    try: 
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)
    
        part_entry.delete(0,END)
        part_entry.insert(END, selected_item[1])
    
        customer_entry.delete(0,END)
        customer_entry.insert(END, selected_item[2])
    
        retailer_entry.delete(0,END)
        retailer_entry.insert(END, selected_item[3])
    
        price_entry.delete(0,END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


#Open the book window
def open_read():
    win = Toplevel(app)
    win['bg']='white'
    Story_name = part_text.get()
    Story_genre = price_entry.get()
    my_text = docx2txt.process('C:/Users/Pommel Knight/Desktop/Domaci_2/Price/'+Story_name+Story_genre+".docx")
    win.title(Story_name)
    
    
    Exit_Button = PhotoImage(file = r"C:\Users\Pommel Knight\Desktop\Domaci_2\Exit.png")
    sun = PhotoImage(file = r"C:\Users\Pommel Knight\Desktop\Domaci_2\sun32.png")
    moon = PhotoImage(file = r"C:\Users\Pommel Knight\Desktop\Domaci_2\moon32.png")
    
    #Dont collect garbage!
    Exit_label = Label(win, image=Exit_Button)
    Exit_label.image = Exit_Button
    
    def toggleText():  
        if(button['text']=='Light Mode'):
            button['text']='Night Mode'
            button['bg'] = 'black'
            button['fg']='white'
            button['image'] = moon
            text_area['background'] = 'black'
            text_area['foreground'] = 'white'
            win['bg']='black'
            remove_btn['bg']='black'
    
        else:
            button['text']='Light Mode'
            button['bg'] = 'white'
            button['fg']='black'
            button['image'] = sun
            text_area['background'] = 'white'
            text_area['foreground'] = 'black'
            win['bg']='white'
            remove_btn['bg']='white'

    
    # Title Label
    Title = Label(win, text = Story_name, font = ("Times New Roman", 15), background = 'black', foreground = "white")
    Title.grid(column = 0, row = 0)
    def set_font(size):
        text_area.configure(font=('Times new Roman', size))
    
    # scrolled text area widget with Read only by disabling the state(doesn't disable it :(...)
    text_area = st.ScrolledText(win, width = 60, height = 30, font = ('bold',14), background = 'white', foreground = "black", wrap=WORD)
    text_area.grid(row = 0,column = 0, pady = 10, padx = 10)
    text_area.grid_propagate(False)
    text_area.columnconfigure(0,weight = 10)
    
    #Light and Dark mode button
    button = Button(win, text = 'Light Mode', command = toggleText, bg = 'white', fg = 'black', image = sun, compound = LEFT)  
    button.grid(row=7, column=0, sticky =W)



    # Exit button.
    remove_btn = Button(win, command=win.destroy, image = Exit_Button, borderwidth=0, bg = 'white')
    remove_btn.grid(row=8, column=0)
    
   



    # Inserting Text
    text_area.insert(INSERT,my_text)


    # Making the text read only
    win.geometry('700x800')
    text_area.configure(state ='disabled')
    

    
#Remove
def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()

def update_item():
    db.update(selected_item[0], part_text.get(), customer_entry.get(), retailer_text.get(), price_entry.get())
    populate_list()

def clear_text():
    part_entry.delete(0,END)
    
    customer_entry.delete(0,END)
    
    retailer_entry.delete(0,END)
    
    price_entry.delete(0,END)

def pick_genre(e):
    customer_entry.get()
    
def pick_script(e):
    price_entry.get()



#Create window object
app = Tk()

bg = PhotoImage( file = "Light_background.png")
  
# Show image using label
label1 = Label( app, image = bg)
label1.place(x = 0,y = 0)
  
# Create Frame
frame1 = Frame( app, bg = "#02ccfe")
frame1.grid(pady = 20)

frame = ttk.Frame(app)
frame.grid(column=0, row=0)




#part/Name
part_text = StringVar()
part_label = Label(app, text = 'Story Name', font = ('bold,14'), pady = 20, bg = "#02ccfe")
part_label.grid(row = 0, column = 0, sticky = W)
part_entry = Entry(app,textvariable = part_text)    
part_entry.grid(row = 0, column = 1)

#Customer/Genre
Genre_OPTIONS = ["Other","Horror","Folk","Adventure","Mystery","Romance"]
customer_text = StringVar()
customer_label = Label(app, text = 'Genre', font = ('bold',14), bg = "#02ccfe")
customer_label.grid(row = 0, column = 2, sticky = W)
customer_entry = ttk.Combobox(app, value = Genre_OPTIONS)
customer_entry.current(0)
customer_entry.bind("<<ComboboxSelected>>", pick_genre)
customer_entry.grid(row = 0, column = 3, sticky="ew")



#Retailer/Author
retailer_label = Label(app, text = 'Author', font = ('bold',14), bg = "#02ccfe")
retailer_text = StringVar()
retailer_label.grid(row = 1, column = 0, sticky = W)
retailer_entry = Entry(app,textvariable = retailer_text)
retailer_entry.grid(row = 1, column = 1)

#Price/Script
Script_OPTIONS = [" - lat", " - ciril"]
price_text = StringVar()
price_label = Label(app, text = 'Script', font = ('bold',14), bg = "#02ccfe")
price_label.grid(row = 1, column = 2, sticky = W)
price_entry = ttk.Combobox(app, value = Script_OPTIONS)
price_entry.current(0)
price_entry.bind("<<ComboboxSelected>>", pick_script)
price_entry.grid(row = 1, column = 3, sticky = "ew")

#Parts List (Listbox)
parts_list = Listbox(app, height = 8, width = 70, border = 0)
parts_list.grid(row = 3, column = 0, columnspan = 3, rows = 6, pady = 20, padx = 20)

#Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

#Create Scrollbar
scrollbar = Scrollbar(app)
#scrollbar.grid(row = 3, column = 3) #Visible Scroll Box, looks like shit, can't centre

#Set scroll to listbox
parts_list.configure(yscrollcommand = scrollbar.set)
scrollbar.configure(command = parts_list.yview)


#Button Add
add_btn = Button(app, text = 'Add Part', width = 12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

#Button Remove
remove_btn = Button(app, text = 'Remove Part', width = 12, command=remove_item)
remove_btn.grid(row=2, column=1)

#Button Update
update_btn = Button(app, text = 'Update Part', width = 12, command=update_item)
update_btn.grid(row=2, column=2)

#Button Clear
clear_btn = Button(app, text = 'Clear Part', width = 12, command=clear_text)
clear_btn.grid(row=2, column=3)

#Button Open Story
read_btn = Button(app, text = 'Read Story', width = 12, command=open_read)
read_btn.grid(row=2, column=4)

app.title('Domaci 2')
app.geometry('700x320')

#Populate data
populate_list()

#start program
app.mainloop()