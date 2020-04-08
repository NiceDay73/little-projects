#!/usr/bin/env python
'''
Simple Editor by @Josep
using TKinter for GUI

TODO LIST:
    - New File -> Done
    - Open file -> Done
    - Save -> Done
    - Save As -> Done
    - Confirm exit if file has been modified ->
    - Move scrollbar to the last line when copy&paste ->
    - Backup before any discard ->
    - Recent files menu option ->
    - Shortcuts for file menu options ->
    - Change font size ->
'''
import tkinter as tk
from tkinter import messagebox, filedialog
import os


class Menubar():

    def __init__(self, parent):
        fonts_spec = ('Ubuntu', 16)

        # create the menubar initializing the font
        menubar = tk.Menu(parent.root, font=fonts_spec)
        # assign this menubar to the parents menu option
        parent.root.config(menu=menubar)

        # Create the dropdown menu for File management
        # tearoff=0 forces the dropdown menu to stay at its position (can not
        # be dragged with the mouse to another part of the screen)
        file_dropdown = tk.Menu(menubar, font=fonts_spec, tearoff=0)
        # create all the options of this menu, assigning a label and the
        # function that will be executed
        file_dropdown.add_command(label='New File', command=parent.new_file)
        file_dropdown.add_command(label='Open File', command=parent.open_file)
        file_dropdown.add_command(label='Save', command=parent.save)
        file_dropdown.add_command(label='Save As', command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label='Exit', command=parent.root.destroy)

        # add the dropdown menu to the menubar
        menubar.add_cascade(label='File', menu=file_dropdown)


class Editor(tk.Frame):
    '''
    This class is the main class. Contains the aplication.
    '''
    FIRST_FILE = 'untitled*'

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        root.name = self.FIRST_FILE
        # Set the window title
        root.title(f'{root.name} - SimEdit')
        # Set the initial size of the window
        root.geometry('800x600')

        fonts_spec = ('Ubuntu', 17)

        self.root = root
        self.font_size = 17
        self.original_text = ''
        self.filename = os.getcwd() + '/' + self.root.name
        self.filename = self.filename[:-1]  # remove last *
        # Create the text area, define background colour as grey,
        # foreground color as white and font using the tuple fonts_spec
        self.textarea = tk.Text(root, bg='#232323', fg='white',
                                font=fonts_spec, wrap=tk.WORD,
                                cursor='arrow', insertbackground='white')
        # create a vertical scroll bar
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.textarea.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.textarea.yview)

        # pack the scrollbar to the raight of the window and filling all the
        # height this has to be done before packing the textarea, otherwise
        # the bar will not appear if the window is not full size
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # pack the textarea to the window:
        # side to align to the left, fill to expand the text area up and down
        # and expand to expant all the way to the right of the window
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        # add the menu bar at the top
        self.menubar = Menubar(self)

    # METHODS
    def set_title(self):
        # updates the title and refresh the window
        self.root.wm_title(f'{self.root.name} - SimEdit')

    def confirm_message(self, msg_text):
        fonts_spec = ('Ubuntu', 18)
        return messagebox.askyesno(message=msg_text, icon='question',
                                   title='WARNING')

    def show_message(self, msg_text):
        fonts_spec = ('Ubuntu', 18)
        return messagebox.showerror(message=msg_text, icon='error',
                                    title='ERROR')

    def is_file_modified(self):
        # * means that the file has not been saved
        if self.root.name[-1] == '*':
            # if the text area has been modified
            if self.textarea.edit_modified():
                return True
            else:
                return False
        else:
            # if the file has been saved and ther is no * at the end
            # of the name, there are no modifications.
            return False

    def clean_textarea(self):
        # remove all content of the textarea and set the modified flag
        # to False
        self.textarea.delete('1.0', 'end')
        self.textarea.edit_modified(False)

    def new_file(self):
        msg = 'File has been modified.\nDiscard changes and continue?'
        if self.is_file_modified():
            if self.confirm_message(msg):
                # User wants to discard changes
                self.clean_textarea()
                self.root.name = self.FIRST_FILE
                self.set_title()
                self.original_text = ''
                self.filename = os.getcwd() + '/' + self.root.name
                self.filename = self.filename[:-1]  # remove last *
            else:
                # don't do anything if user don't want to discard changes
                pass
        else:
            self.clean_textarea()
            self.root.name = self.FIRST_FILE
            self.set_title()
            self.original_text = ''
            self.filename = os.getcwd() + '/' + self.root.name
            self.filename = self.filename[:-1]  # remove last *

    def open_file(self):
        msg = 'File has been modified.\nDiscard changes and continue?'
        filename = ''
        if self.is_file_modified():
            if self.confirm_message(msg):
                self.clean_textarea()
                filename = filedialog.askopenfilename()
                self.filename = filename
                self.root.name = filename + '*'
                self.set_title()
            else:
                # don't do anything if user don't want to discard changes
                pass
        else:
            self.clean_textarea()
            filename = filedialog.askopenfilename()
            self.filename = filename
            self.root.name = filename + '*'
            self.set_title()

        # if the user has choosen a file, open it and write its content
        # into the editor
        if len(filename) > 0:
            try:
                with open(filename, mode='r') as fd:
                    filetext = fd.read()
                    self.textarea.insert('1.0', filetext)
                    self.original_text = filetext
            except:
                msg = 'Error while opening the file!!!'
                self.show_message(msg)
                self.root.name = self.FIRST_FILE
                self.set_title()
                self.filename = os.getcwd() + '/' + self.root.name
                self.filename = self.filename[:-1]  # remove last *
                self.original_text = ''
            # initialize the modified flag to False
            self.textarea.edit_modified(False)

    def can_save(self):
        try:
            with open(self.filename, mode='r') as fd:
                filetext = fd.read()
                if self.original_text == filetext:
                    return True
                else:
                    msg = '''
                          The file has been modified by another application.
                          Please Save As with another name!!
                          '''
                    self.show_message(msg)
                    return False
        except:
            return True

    def save(self):
        if self.can_save():
            # this returns all the text.
            # end-1c means that subtract 1 char from the last position
            # because the function always return an extra \n
            filetext = self.textarea.get('1.0', 'end-1c')
            try:
                if self.root.name[-1] == '*':
                    self.root.name = self.root.name[:-1]
                with open(self.filename, mode='w') as fd:
                    fd.write(filetext)
                    self.set_title()
            except Exception as e:
                print('ERROR saving the file', e)
        else:
            print('Can not be saved!!!')

    def save_as(self):
        # this returns all the text. end-1c means that subtract 1 char from the
        # last position because the function always return an extra \n
        filetext = self.textarea.get('1.0', 'end-1c')
        new_filename = filedialog.asksaveasfilename()
        if new_filename != '':
            try:
                self.root.name = new_filename.split('/')[-1]
                self.filename = new_filename
                with open(self.filename, mode='w') as fd:
                    fd.write(filetext)
                    self.set_title()
            except Exception as e:
                print('ERROR saving the file', e)


def main():
    root = tk.Tk()
    ed = Editor(root)

    root.mainloop()


if __name__ == '__main__':
    main()
