import tkinter as tk
from tkinter import filedialog  # filedialog provide us an explorer to navigate through folders and accessing
                                # files in our system(can be used to say open a real file in our OS)
from tkinter import messagebox  # to generate some message boxes to display a message we want to show


class MenuBar:  # part deals with menubar part and its functionalities in our text editor
    def __init__(self, parent):  # Here 'parent' contains instance of pytext class
        font_specs = ("Gabriola", 14)  # font style of menu bar
        menubar = tk.Menu(parent.master, font=font_specs)  # access root window by using parent.master
        parent.master.config(menu=menubar)  # creating the menu bar to show it in master window
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)  # tear off=0 fixes menu bar and make it immovable
        file_dropdown.add_command(label="New File", command=parent.new_file,
                                  accelerator="Ctrl+N")  # string passed in accelerator is used show user, keybord Shortcuts
        file_dropdown.add_command(label="Open File", command=parent.open_file,
                                  accelerator="Ctrl+O")
        file_dropdown.add_command(label="Save", command=parent.save_file,
                                  accelerator="Ctrl+S")
        file_dropdown.add_command(label="Save As", command=parent.saveAs_file,
                                  accelerator="Ctrl+Shift+S")
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes", command=self.show_release_message)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About", command=self.show_about_message)

        menubar.add_cascade(label="File", menu=file_dropdown)  # to show the drop-down menu bar
        menubar.add_cascade(label="About", menu=about_dropdown)
    def show_about_message(self):
        Box_title = "About PyText"
        box_message = "A Python Text Editor!"
        messagebox.showinfo(Box_title, box_message)  # a message-box library to show dialog box
    def show_release_message(self):
        Box_title = "Release Notes"
        box_message = "PyText Version 0.1 - INDIA"
        messagebox.showinfo(Box_title, box_message)

class Statusbar:  # to create a responsive statusbar
    def __init__(self, parent):
        font_specs = ("Ink Free", 12)

        self.status = tk.StringVar()  # a method to create a string variable and we can also give an string value to it
        self.status.set("PyText - 0.1 INDIA")
        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor='sw', font=font_specs)  # anchor is used to position the label in textarea
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
            if isinstance(args[0], bool):  # incase the first parameter is boolean(isinstance is used to type-check a parameter passed)
                self.status.set("Your File Has Been Saved! :-) ")
            else:
                self.status.set("PyText - 0.1 INDIA")


class pytext:  # part deals with text functionality of text editor
    def __init__(self, master):
        master.title("untitled-pyText")  # adding title to our master window
        master.geometry("500x500")  # adding dimensions to our main window(width X height)
        font_specs = ("Comic Sans MS", 18)  # configured text font style for our text edit0or
        self.master = master  # created a reference to our root window(master)this allows us to acces our window from menubar using 'parent'
        self.filename = None  # represents name of the file we will be working on
        self.textarea = tk.Text(master, font=font_specs)  # adding the text area widget! and adding defined font style
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)  # adding the scrollbar widget along the y-axis
        self.textarea.configure(yscrollcommand=self.scroll.set)  # to configure the textarea to enable scrollbar to navigate along y using our mouse
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # to place our widget into our main window and place it on the left hand side
        # also we have used fill (BOTH) to fit the text area into our window in both sides,
        # we also putted expand as true to enable the expansion of the text area size
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)  # place scroll on the right hand side as a reference to textarea
        # also here fill is used to take scrollbar to take whole y-axis.
        # since our pytext act as main control of whole program.So we instantiate our menubar in init method of pytext
        self.menubar = MenuBar(self)
        self.statusbar = Statusbar(self)  # passing the instance of pytext in Satatusbar class
        # self.statusbar helps to access methods of the class Statusbar
        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:  # when we open the file we want name of that file to be displayed as title else we want "untitled" as title(as the case of say creating a file)
            self.master.title(name + "- pytext")
        else:
            self.master.title("untitled-pyText")

    def new_file(self, *args):  # *args is used to accept key-press event parameter sent by bind function
        # *args is used to help functions manage extra comming parameters
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title(self.filename)

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            # it helps to select the specific file within our system and return its name
            defaultextension=".txt",  # setting default extension as a .txt
            filetypes=[("All Files", "*.*"),
                       # as there may be some other formats of files to open,and it will be contained in a list,having tuples as its member
                       ("Text Files", "*.txt"),
                       # first part will contain a verbose name and the other will contain extention
                       ("Python Scripts", "*.py"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css"),
                       ("C Files", "*.c"),
                       ("C++ Files", "*.cpp")])
        if self.filename:  # if there is something associated with filename other than 'None'
            self.textarea.delete(1.0, tk.END)  # deleting everything in the text area from begining(1.0 is the begin of buffer) to end(tk.END)
            with open(self.filename, "r") as f:  # to open a file in read mode and open a file as "f"
                self.textarea.insert(1.0, f.read())  # insert the text from the beginning(1.0) of the text area and insert the content of the file which we can read(f.read())
            self.set_window_title(self.filename)

    def save_file(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(0.1, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                    self.statusbar.update_status(True)  # Updating Status Bar After Saving
            except Exception as e:
                print(e)
        else:
            self.saveAs_file()  # even if a user click on save for a newly created file,the will be able to actually create a new file

    def saveAs_file(self, *args):
        try:  # we use try method to manage an exception might occur
            new_file = filedialog.asksaveasfilename(
                # allow us to select a location in our system and a name for a new file that we want to create
                initialfile="Untitled.txt",  # name given to the save file if we don't provide the name
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                           ("Text Files", "*.txt"),
                           ("Python Scripts", "*.py"),
                           ("Markdown Documents", "*.md"),
                           ("JavaScript Files", "*.js"),
                           ("HTML Documents", "*.html"),
                           ("CSS Documents", "*.css"),
                           ("C Files", "*.c"),
                           ("C++ Files", "*.cpp")])
            textarea_content = self.textarea.get(1.0, tk.END)  # getting the text from beginning to the end
            with open(new_file, "w") as f:  # we open the file in write mode
                f.write(textarea_content)
                self.set_window_title(self.filename)
                self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def bind_shortcuts(self):  # we are defining it in init method of pytext as we want to run it as soon as program starts
        self.textarea.bind('<Control-n>', self.new_file)  # bind is sending the function it is triggering an key-press event(basically another parameter)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save_file)  # Ctrl+s
        self.textarea.bind('<Control-S>', self.saveAs_file)  # Ctrl+Shift+s
        self.textarea.bind('<Key>', self.statusbar.update_status)  # call the update_status method whenever a key is pressed


if __name__ == "__main__":  # running in main
    master = tk.Tk()  # creating the window
    pt = pytext(master)  # pytext act as a main controller of the window using init function and passing instance of the window to our pytext class
    master.mainloop()  # running the window infinitely until the cross button is pressed
