import tkinter as tk
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        """
        Initializes the Application class.

        This method is the constructor of the Application class. It sets up the GUI window with a title and geometry. It creates a listbox widget and packs it onto the window with some padding. It also creates a frame for the buttons and packs it onto the window with some padding. Inside the frame, it creates three buttons: "Add", "Delete", and "Edit". Each button is associated with a corresponding method of the Application class.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()
        self.title("Advanced Listbox Example")
        self.geometry("300x250")

        # Create listbox
        self.listbox = tk.Listbox(self, width=30, height=10)
        self.listbox.pack(pady=10)

        # Create buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add", command=self.add_item)
        add_button.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Delete", command=self.remove_item)
        remove_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(button_frame, text="Edit", command=self.edit_item)
        edit_button.pack(side=tk.LEFT, padx=5)

        self.ui_elements = []

    def add_item(self):
        """
        Adds a new item to the application by creating a new AddWindow instance.
        
        Parameters:
            None
        
        Returns:
            None
        """
        self.add_window = AddWindow(self)

    def remove_item(self):
        """
        Removes an item from the listbox.

        Parameters:
            None

        Returns:
            None
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            confirmation = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove '{self.listbox.get(selected_index)}'?")
            if confirmation:
                self.listbox.delete(selected_index)
        else:
            print("No item selected")

    def edit_item(self):
        """
        Edits an item in the listbox by replacing it with a new value.

        Parameters:
            None

        Returns:
            None
        """
        selected_index = self.listbox.curselection()
        if selected_index:
            original_text = self.listbox.get(selected_index)
            entry = tk.Entry(self)
            entry.insert(0, original_text)
            entry.focus_set()

            def save_edit():
                new_text = entry.get()
                self.listbox.delete(selected_index)
                self.listbox.insert(selected_index, new_text)
                entry.destroy()

            button = tk.Button(self, text="Save Changes", command=save_edit)
            button.pack(pady=10)

            entry.pack(pady=10)
        else:
            print("No item selected")

class AddWindow(tk.Toplevel):
    def __init__(self, master):
        """
        Initializes the AddWindow class, creating a new window for adding shortcuts.

        Parameters:
            master (tkinter.Tk): The parent window of the AddWindow instance.

        Returns:
            None
        """
        super().__init__(master)
        self.master = master
        self.title("Add New Shortcut")
        self.geometry("300x300")

        label1 = tk.Label(self, text="Shortcut Name:")
        label1.pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        label2 = tk.Label(self, text="Keystrokes:")
        label2.pack(pady=5)
        self.keystrokes_entry = tk.Entry(self)
        self.keystrokes_entry.pack(pady=5)

        label3 = tk.Label(self, text="Action:")
        label3.pack(pady=5)
        self.actions_entry = tk.Entry(self)
        self.actions_entry.pack(pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        save_button = tk.Button(button_frame, text="Save", command=self.save_changes)
        save_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5)

    def save_changes(self):
        """
        Saves the changes made in the AddWindow instance.

        Retrieves the values from the name_entry, keystrokes_entry, and actions_entry fields.
        If all fields are filled, inserts the values into the master listbox and destroys the AddWindow instance.
        Otherwise, displays a warning message prompting the user to fill out all fields.

        Parameters:
            None

        Returns:
            None
        """
        Shortcut_name = self.name_entry.get()
        keystrokes = self.keystrokes_entry.get()
        actions = self.actions_entry.get()
        
        if Shortcut_name and keystrokes and actions:
            self.master.listbox.insert(tk.END, f"{Shortcut_name} - keystrokes: {keystrokes}, actions: {actions}")
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def cancel(self):
        """
        Cancels the current operation by destroying the window.

        Parameters:
            None

        Returns:
            None
        """
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
