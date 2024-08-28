import csv, os, time, keyloggerTest as kl, tkinter as tk, threading
from tkinter import messagebox
# Import necesary libraries


selected, homepage, editpage, returnedkeystrokes, shortcuts = None, True, False, None, kl.csvParser('keylogger.csv',True)
# Configure Variables

kl.csvCleaner('keylogger.csv')
# Clean current CSV file


def contentRenderer(shortcuts):
    # contentRenderer IPO:
    # INPUT:
    #   - shortcuts, <list> or <nonetype>, Contains list of all shortcuts
    # PROCESSING:
    #   - Sets up canvas and scroll-bar for frame
    #   - Iterates through each shortcut and renders each element as a frame with the keystrokes, commands, date and name in labels
    #   - If length of keystrokes text is above 25, add ellipsis to show that more info follows
    #   - If length of commands text is above 18, add ellipsis to show that more info follows
    #   - If length of name text is above 7, add ellipses to show that more info follows
    # OUTPUT:
    #   - Displays UI and Buttons

    canvas = tk.Canvas(frmBody, bg="Black", width=300, height=190, highlightbackground="White", highlightthickness=1)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrlbar = tk.Scrollbar(frmBody, orient='vertical', command=canvas.yview)
    scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrlbar.set)
    frmContent = tk.Frame(canvas, bg="Black", width=290, height=50)
    canvas.create_window((0, 0), window=frmContent, anchor=tk.NW)
    if shortcuts != '':
        for i, shortcut in enumerate(shortcuts):
            if shortcut in [None, '', ' ', '\n', []]:
                continue
            keystrokes, commands, date, name = shortcut[1], shortcut[2], shortcut[3], shortcut[4]
            # Sets variables for shortcut info/contents

            # Ellipsis Length Algorithms:
            if len(str(keystrokes)) > 25: # If the length of the keystrokes text is greater than 25 do
                if str(keystrokes)[22] == '.': # If the 23rd character of the keystrokes text is a full-stop do
                    keystrokes = str(keystrokes)[:22] + '..' # Add 2 dots (Becomes 3 when added with final dot from string making '...')
                else: # Else do
                    keystrokes = str(keystrokes)[:22] + '...' # Add 3 dots (Makes '...')

            if len(str(commands)) > 18: # If the length of the commands text is greater than 18 do
                if str(commands)[15] == '.': # If the 16th character of the commands text is a full-stop do
                    commands = str(commands)[:15] + '..' # Add 2 dots (Becomes 3 when added with final dot from string making '...')
                else: # Else do
                    commands = str(commands)[:15] + '...' # Add 3 dots (Makes '...')

            if len(str(name)) > 7: # If the length of the name text is greater than 7 do
                if str(name)[4] == '.': # If the 5th character of the name text is a full-stop do
                    name = str(name)[:4] + '..' # Add 2 dots
                else:
                    name = str(name)[:4] + '...' # Add 3 dots

            # Configure and pack UI elements:
            # Frame with black background, white outline of 1px width, frame width of 290 and height of 50
            frmContentRow = tk.Frame(frmContent, bg="Black", width=290, height=50, highlightbackground="White", highlightthickness=1)
            frmContentRow.pack(side=tk.TOP, pady=2, padx=5, anchor=tk.W)

            # Label for displaying shorcut name, text of ID of shorcut and name, black background, white foreground, courier new bold size 11 font
            lblName = tk.Label(frmContentRow, text=str(i+1) + ' - ' + name, bg="Black", fg="White", font=("Courier New", 11, 'bold'))
            lblName.place(relx=0.0, rely=0.0)

            # Label for displaying date, text of date, black background, white foreground, courier new bold size 9 font
            lblDate = tk.Label(frmContentRow, text=date, bg="Black", fg="#dddddd", font=("Courier New", 9, 'bold'))
            lblDate.place(relx=0.0, rely=0.5)

            # Label for displaying keystrokes, text of keystrokes, black background, white foreground, courier new size 9 font
            lblKeystrokes = tk.Label(frmContentRow, text=str(keystrokes), bg="Black", fg="White", font=("Courier New", 9))
            lblKeystrokes.place(relx=0.35, rely=0.0)

            # Label for displaying commands, text of commands, black background, white foreground, courier new size 9 font
            lblCommands = tk.Label(frmContentRow, text=commands, bg="Black", fg="White", font=("Courier New", 9))
            lblCommands.place(relx=0.35, rely=0.5)

            # Button for selecting the shorcut, text of select, black background, white foreground, arial size 9 font, command to select the shorcut
            bttnSelect = tk.Button(frmContentRow, text="Select", bg="Black", fg="White", font=("Arial", 9), command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: select(i, frmContentRow, frmContent))
            bttnSelect.place(relx=0.84, rely=0.44)


    # Frame with black background, frame width of 290 and height of 24, for buffer at bottom where buttons are
    frmBufferRow = tk.Frame(frmContent, bg="Black", width=290, height=24)
    frmBufferRow.pack(side=tk.TOP, pady=2, padx=5)

    # Button for creating a new shorcut, text of new +, black background, white foreground, arial size 9 font, command to create a new shorcut
    bttnNew = tk.Button(frmBody, width=13, text="New +", bg="Black", fg="White", font=("Arial", 9))
    bttnNew.configure(command=new)
    bttnNew.place(relx=0.005, rely=0.86)

    # Button for deleting the selected shorcut, text of delete -, black background, white foreground, arial size 9 font, command to delete the selected shorcut
    bttnDelete = tk.Button(frmBody, width=13, text="Delete -", bg="Black", fg="White", font=("Arial", 9))
    bttnDelete.configure(command=delete)
    bttnDelete.place(relx=0.315, rely=0.86)

    try:
        # Button for editing the selected shorcut, text of edit %, black background, white foreground, arial size 9 font, command to edit the selected shorcut
        bttnEdit = tk.Button(frmBody, width=13, text="Edit %", bg="Black", fg="White", font=("Arial", 9))
        bttnEdit.configure(command=lambda frmContentRow=frmContentRow, frmContent=frmContent: edit(selected, frmContentRow, frmContent))
        bttnEdit.place(relx=0.626, rely=0.86)
        bttnEdit['state'] = 'active'
    except:
        bttnEdit = tk.Button(frmBody, width=13, text="Edit %", bg="Black", fg="White", font=("Arial", 9))
        bttnEdit.place(relx=0.626, rely=0.86)
        bttnEdit['state'] = 'disabled'

    frmContent.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# Create the main window
window = tk.Tk() # Initialize the window as 'window'
icon = tk.PhotoImage(file='shortcutmanagericon.ico') # Load the icon image
window.title('Shortcut Manager') # Set the title of the window to 'Shortcut Manager'
window.geometry('400x300') # Set the size of the window to 400x300
window.resizable(False, False) # Disable resizing of the window
window.iconphoto(False, icon) # Set the icon of the window to the icon image
window.config(bg='Black') # Set the background color of the window to black


# Create the frames for the title and body
frmTitle = tk.Frame(window, bg="Black", width=400, height=80) # Initialize the title frame as 'frmTitle'
frmTitle.grid(column=0, row=0)

lblTitle = tk.Label(frmTitle, text="Shortcut Manager", font=("Arial", 16), fg="White", bg="Black") # Initialize the title label as 'lblTitle'
lblTitle.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
lblSubtitle = tk.Label(frmTitle, text="v0.0.4 - Alpha", fg="White", bg="Black") # Initialize the subtitle label as 'lblSubtitle'
lblSubtitle.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

frmBody = tk.Frame(window, bg="Black", width=300, height=210, highlightbackground="White", highlightthickness=1) # Initialize the body frame as 'frmBody'
frmBody.grid(column=0, row=1, padx=50)


def select(i, frmContentRow, frmContent):
    # select function IPO
    # INPUT:
    #   - Selected shorcut from UI button
    # PROCESSING:
    #   - Change the background color of the selected shorcut to white and foreground color to black
    #   - Change the background color of all other shorcuts to black and foreground color to white
    # OUTPUT:
    #   - Returns the selected shorcut
    #   - UI Changes

    global selected
    for widget in frmContentRow.winfo_children():
        widget.configure(bg="White", fg="Black")
    frmContentRow.configure(bg="White")
    for widget in frmContent.winfo_children():
        if widget != frmContentRow:
            widget.configure(bg="Black")
            for child in widget.winfo_children():
                child.configure(bg="Black", fg="White")
    selected = i


def closing():
    # closing function IPO
    # INPUT:
    #   - User input to close the window
    # PROCESSING:
    #   - Ask the user if they want to quit
    #   - If yes, clean the CSV file and close the window
    #   - If no, do nothing
    # OUTPUT:
    #   - Closes the window and cleans the CSV file

    if messagebox.askyesno("Quit", "Do you want to quit?"): # If the user clicks yes do
        kl.csvCleaner('keylogger.csv') # Clean the CSV file
        window.destroy() # Close the window
        os.kill(os.getpid(), 9) # Kill the process

def edit(i, frmContentRow, frmContent):
    # edit function IPO
    # INPUT:
    #   - Selected shorcut from UI button
    # PROCESSING:
    #   - Create a new window for editing the selected shorcut
    #   - Add labels and entry fields for the name, keystrokes and commands
    #   - Add buttons for saving and cancelling the edit
    # OUTPUT:
    #   - Returns the edited shorcut
    #   - UI Changes


    # set global variables for homepage and editpage
    global homepage
    global editpage
    global selected
    homepage = False
    editpage = True

    if selected != None: # If a shortcut is selected do
        # make new window for editing the shortcut
        new_window = tk.Toplevel(window)
        new_window.title("Edit Shortcut")
        new_window.geometry("400x200")
        new_window.config(bg="Black")

        # create frame for editing the shortcut
        frmEdit = tk.Frame(new_window, bg="Black", width=400, height=200)
        frmEdit.pack()

        # create labels and entry fields for the name, keystrokes and commands
        lblEditTitle = tk.Label(frmEdit, text="Edit Shortcut", font=("Arial", 14), fg="White", bg="Black") # Initialize the title label as 'lblEditTitle'
        lblEditTitle.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        lblEditName = tk.Label(frmEdit, text="Name:", font=("Arial", 12), fg="White", bg="Black")   # Initialize the name label as 'lblEditName'
        lblEditName.place(relx=0.1, rely=0.3)

        lblEditKeystrokes = tk.Label(frmEdit, text="Keystrokes:", font=("Arial", 12), fg="White", bg="Black") # Initialize the keystrokes label as 'lblEditKeystrokes'
        lblEditKeystrokes.place(relx=0.1, rely=0.42)

        lblEditCommands = tk.Label(frmEdit, text="Commands:", font=("Arial", 12), fg="White", bg="Black") # Initialize the commands label as 'lblEditCommands'
        lblEditCommands.place(relx=0.1, rely=0.54)
        
        entrEditName = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White') # Initialize the name entry as 'entrEditName'
        entrEditName.place(relx=0.4, rely=0.3)

        bttnEditKeystrokes = tk.Button(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White', text='Record Keystrokes', command=recordkeystrokes) # Initialize the keystrokes button as 'bttnEditKeystrokes', set the text to 'Record Keystrokes' and set the command to 'recordkeystrokes'
        bttnEditKeystrokes.place(relx=0.4, rely=0.42)
        
        entrEditCommands = tk.Entry(frmEdit, width=20, font=("Arial", 12), bg='Black', fg='White') # Initialize the commands entry as 'entrEditCommands'
        entrEditCommands.place(relx=0.4, rely=0.59)

        bttnEditSave = tk.Button(frmEdit, text="Save", bg="Black", fg="White", font=("Arial", 12)) # Initialize the save button as 'bttnEditSave'
        bttnEditSave.place(relx=0.47, rely=0.8, anchor=tk.CENTER)
        bttnEditSave.configure(command=lambda i=i, frmContentRow=frmContentRow, frmContent=frmContent: save(i, frmContentRow, frmContent, entrEditName, returnedkeystrokes, entrEditCommands, new_window)) # Set the command to 'save'

        bttnEditCancel = tk.Button(frmEdit, text="Cancel", bg="Black", fg="White", font=("Arial", 12)) # Initialize the cancel button as 'bttnEditCancel'
        bttnEditCancel.place(relx=0.62, rely=0.8, anchor=tk.CENTER)
        bttnEditCancel.configure(command=lambda: cancel(new_window)) # Set the command to 'cancel'
        
        new_window.mainloop() # Run the new window

def recordkeystrokes():
    # recordkeystrokes function IPO
    # INPUT:
    #   - User input to record keystrokes
    # PROCESSING:
    #   - Start recording keystrokes
    #   - Wait for 4.5 seconds
    #   - Stop recording keystrokes
    #   - Save the captured shortcut
    # OUTPUT:
    #   - Returns the recorded keystrokes
    #   - Console output

    global returnedkeystrokes # Get the global variable 'returnedkeystrokes'
    kl.startRecording() # Start recording keystrokes
    #print("Recording started. Please hold shortcut for 5 seconds.")
    time.sleep(4.5)
    shortcut = kl.stopRecording() # After 4.5 seconds, stop recording keystrokes
    time.sleep(0.5)
    #print(f"Captured shortcut: {shortcut}") # Print the captured shortcut

def save(i, frmContentRow, frmContent, entrEditName, entrEditKeystrokes, entrEditCommands, new_window):
    global shortcuts # Get the global variable 'shortcuts'    
    #input validation
    #existance check
    if entrEditName.get() == '' or entrEditKeystrokes.get() == '' or entrEditCommands.get() == '': # If the name, keystrokes or commands are empty do
        messagebox.showerror("Error", "Please fill in all fields") # Show an error message
    #ensure that keystrokes are recorded as a set
    if entrEditKeystrokes.get().type() != set:
        messagebox.showerror("Error", "Please record keystrokes")
    #ensure that the name is unique
    for shortcut in shortcuts:
        if entrEditName.get() == shortcut[4]:
            messagebox.showerror("Error", "Name already exists")
    
    #update the csv file
    with open('keylogger.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for index, shortcut in enumerate(shortcuts): # For each shortcut in the list of shortcuts do
            if index == i:  # If the index is equal to the selected shortcut do
                writer.writerow([index,returnedkeystrokes, entrEditCommands.get(), shortcut[3], entrEditName.get()]) # Write the new shortcut to the CSV file
            else:
                writer.writerow(shortcut) # Write the old shortcut to the CSV file
    

    shortcuts = kl.csvParser('keylogger.csv',True) # Parse the new CSV file and set the shortcuts to the new list of shortcuts
    kl.csvCleaner('keylogger.csv') # Clean the CSV file
    refreshcontent() # Refresh the ui content
    cancel(new_window) # Kill the edit window

def cancel(new_window):
    new_window.destroy() # Destroy the edit window
    # set global variables for homepage and editpage back to true and false respectively as the edit window is closed
    global homepage 
    global editpage
    homepage = True
    editpage = False

def refreshcontent():
    # refreshcontent function IPO
    # INPUT:
    #   - function called
    # PROCESSING:
    #   - Destroy all widgets in the body frame
    #   - Render the content again
    # OUTPUT:
    #   - Refreshed UI content

    for widget in frmBody.winfo_children():
        widget.destroy()
    contentRenderer(shortcuts)

def delete():
    # delete function IPO
    # INPUT: 
    #   - Selected shorcut from UI button
    #   - List of all shorcuts from CSV file
    # PROCESSING:
    #   - 
    global selected # Get current selected 
    global shortcuts    
    #update the csv file
    with open('keylogger.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for index, shortcut in enumerate(shortcuts):
            if index != selected:
                
                writer.writerow(shortcut)

    
    kl.csvCleaner('keylogger.csv')
    shortcuts = kl.csvParser('keylogger.csv',True)

    refreshcontent()

def new():
    # new function IPO
    # INPUT:
    #   - User input to create a new shorcut
    # PROCESSING:
    #   - Create a new window for creating a new shorcut
    #   - Add labels and entry fields for the name, keystrokes and commands
    #   - Add buttons for saving and cancelling the new shorcut
    # OUTPUT:
    #   - Returns the new shorcut
    #   - UI Changes

    # set global variables for homepage and editpage
    global homepage
    global editpage
    homepage = False
    editpage = True

    # make new window for creating a new shortcut
    new_window = tk.Toplevel(window)
    new_window.title("New Shortcut")
    new_window.geometry("400x200")
    new_window.config(bg="Black")

    # create frame for creating the shortcut
    frmNew = tk.Frame(new_window, bg="Black", width=400, height=200)
    frmNew.pack()

    # create labels and entry fields for the name, keystrokes and commands
    lblNewTitle = tk.Label(frmNew, text="New Shortcut", font=("Arial", 14), fg="White", bg="Black")
    lblNewTitle.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
    lblNewName = tk.Label(frmNew, text="Name:", font=("Arial", 12), fg="White", bg="Black")
    lblNewName.place(relx=0.1, rely=0.3)
    lblNewKeystrokes = tk.Label(frmNew, text="Keystrokes:", font=("Arial", 12), fg="White", bg="Black")
    lblNewKeystrokes.place(relx=0.1, rely=0.42)
    lblNewCommands = tk.Label(frmNew, text="Commands:", font=("Arial", 12), fg="White", bg="Black")
    lblNewCommands.place(relx=0.1, rely=0.54)

    entrNewName = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewName.place(relx=0.4, rely=0.3)
    entrNewKeystrokes = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewKeystrokes.place(relx=0.4, rely=0.42)
    entrNewCommands = tk.Entry(frmNew, width=20, font=("Arial", 12), bg='Black', fg='White')
    entrNewCommands.place(relx=0.4, rely=0.54)

    # create buttons for saving and cancelling the new shortcut
    bttnNewSave = tk.Button(frmNew, text="Save", bg="Black", fg="White", font=("Arial", 12))
    bttnNewSave.place(relx=0.47, rely=0.8, anchor=tk.CENTER)
    bttnNewSave.configure(command=lambda: saveNew(entrNewName, entrNewKeystrokes, entrNewCommands, new_window))

    bttnNewCancel = tk.Button(frmNew, text="Cancel", bg="Black", fg="White", font=("Arial", 12))
    bttnNewCancel.place(relx=0.62, rely=0.8, anchor=tk.CENTER)
    bttnNewCancel.configure(command=lambda: cancelNew(new_window))

def saveNew(entrNewName, entrNewKeystrokes, entrNewCommands, new_window):
    # saveNew function IPO
    # INPUT:
    #   - User input to save the new shorcut
    # PROCESSING:
    #   - Validate the input
    #   - Append the new shorcut to the CSV file
    # OUTPUT:
    #   - Returns the new shorcut
    #   - UI Changes

    # get global variables for shorcuts
    global shortcuts


    # input validation TODO @Wolfoverflow

    # append the new shortcut to the csv file
    with open('keylogger.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([len(shortcuts)+1, entrNewKeystrokes.get(), entrNewCommands.get(), kl.getToday(), entrNewName.get()]) # Write the new shortcut to the CSV file
    kl.csvCleaner('keylogger.csv') # Clean the CSV file
    shortcuts = kl.csvParser('keylogger.csv',True) # Parse the new CSV file and set the shortcuts to the new list of shortcuts
    refreshcontent()    # Refresh the ui content
    cancelNew(new_window) # Kill the new window

def cancelNew(new_window):
    new_window.destroy() # Destroy the new window
    # set global variables for homepage and editpage back to true and false respectively as the new window is closed
    global homepage
    global editpage
    homepage = True
    editpage = False



window.protocol("WM_DELETE_WINDOW", closing) # Set the closing function to run when the window is closed

contentRenderer(shortcuts) # Render the content
thread = threading.Thread(target=kl.keyboardListener)
thread.start()
window.mainloop() # Run the window
