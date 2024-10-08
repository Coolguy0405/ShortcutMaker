import os
import sys
try:
    from pynput import keyboard
except ModuleNotFoundError:
    os.system(f"{sys.executable} -m pip install pynput")
    from pynput import keyboard
import csv
import time
import threading
import replacer
import re
import subprocess

os.chdir(os.path.dirname(__file__))

# check if keylogger.csv exists
if not os.path.exists("keylogger.csv"):
    with open("keylogger.csv", 'w') as f:
        f.write("")

recording = False
keystrokes = []

class KeyLogger:
    def __init__(self, keystrokes):
        self.currentKeys = []
        self.recordedKeys = []
        self.keystrokes = keystrokes

    def onPress(self, key):
        """
        Wolfoverflow
        Adds the given key to the currentKeys list if it is not already present.
        If recording is True, also adds the key to the recordedKeys list.
        Input validation not required as this is called from a listener

        Parameters:
            key (str): The key to be added to the currentKeys list.

        Returns:
            None
        """
        key = str(key).strip("'")
        if key not in self.currentKeys:
            key = replacer.translator(key)
            self.currentKeys.append(key)
            if recording and key not in self.recordedKeys:
                self.recordedKeys.append(key)

    def onRelease(self, key):
        """
        Wolfoverflow
        Removes the given key from the currentKeys list if it is present.
        Input validation not required as this is called from a listener

        Parameters:
            key (str): The key to be removed from the currentKeys list.

        Returns:
            None
        """
        key = str(key).strip("'")
        if key in self.currentKeys:
            key = replacer.translator(key)
            self.currentKeys.remove(key)
            if recording and key in self.recordedKeys:
                self.recordedKeys.remove(key)

    def keystrokeRecorder(self, key, recording=False):
        """
        Wolfoverflow
        Passes the given key to the appropriate function, returning a shortcut ID or current keystrokes.
        Input validation not required as this is called from a listener

        Parameters:
            key (str): The key to be parsed.
            recording (bool, optional): Whether the key is being recorded. Defaults to False.

        Returns:
            int or None: The ID of the shortcut if detected, None otherwise.
            currentKeys (set): The current keys being pressed.
        """
        self.onPress(key)
        currentKeys = set(self.currentKeys)
        if recording:
            return currentKeys
        else:
            if currentKeys in self.keystrokes:
                for IDNumber,shortcutID in enumerate(self.keystrokes):
                    if currentKeys == shortcutID:
                        # print(f"Shortcut {shortcutID} with ID {IDNumber} was pressed")
                        return IDNumber

        # print("Current keys:", ", ".join(self.currentKeys))
        # print(self.currentKeys)

def getToday():
    """
    Bowie
    Returns the current date in the format DD/MM/YYYY.
    Input validation not required as this takes no params

    Parameters:
        None

    Returns:
        str: The current date in the format DD/MM/YYYY.
    """
    return time.strftime("%d/%m/%Y")

def onPress(key):
    """
    Wolfoverflow
    Adds the given key to the currentKeys list if it is not already present.
    Input validation not required as this is called from a listener

    Parameters:
        key (str): The key to be added to the currentKeys list.

    Returns:
        None
    """
    global recording
    id = keyLogger.keystrokeRecorder(key, recording)
    if id is not None and not recording:
        commandRunner(id, csvParser("keylogger.csv"))

def onRelease(key):
    """
    Wolfoverflow
    Release the given key by calling the `onRelease` method of the `keyLogger` object.
    Input validation not required as this is called from a listener

    Parameters:
        key (str): The key to be released.

    Returns:
        None
    """
    keyLogger.onRelease(key)

def startRecording():
    """
    Wolfoverflow
    Starts the keylogger recording process.

    Sets the global recording flag to True, indicating that the keylogger is actively recording keystrokes.
    Input validation not required as it takes no params

    Parameters:
        None

    Returns:
        None
    """
    global recording
    recording = True

def stopRecording():
    """
    Wolfoverflow
    Stop the recording and return the set of recorded keys.
    Input validation not required as this is called from a listener

    This function sets the global `recording` variable to `False`, which stops the keylogger from blocking macros

    Returns:
        set: The set of recorded keys.
    """
    global recording
    recording = False
    return set(keyLogger.recordedKeys)

def setFormatChecker(string: str):
    """
    Wolfoverflow
    Checks if the given string matches the format for a set.

    Parameters:
        string (str): The string to be checked.

    Returns:
        bool: True if the string is in the correct format, False otherwise.
    """
    if re.match(r'\{[^{}]+\}', string):
        return True
    return False

# Usage
# Format for keystrokes:


# # CSV format
# | shortcutID | keys              | batchCommand | creationDate | shortcutName |
# |------------|-------------------|--------------|--------------|--------------|
# | 0          | {'Key.ctrl', 'm'} | echo Pass    | 1/1/1970     | Pass         |
# | 1          | {'Key.cmd', ';'}  | echo Pass1   | 1/1/2000     | Pass1        |
# |------------|-------------------|--------------|--------------|--------------|

def csvParser(filename, includeRowNumber = False):
    """
    Wolfoverflow
    This function parses a CSV file and returns the data in a structured format.

    Parameters:
        filename (str): The name of the CSV file to parse.
        includeRowNumber (bool): An optional parameter to include the row number in the parsed data. Defaults to False.

    Returns:
        list: A list of lists, where each sublist contains the parsed data for a row in the CSV file.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found.") # raise an error if the file doesn't exist
    
    parsedData = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            if row[0] == "":
                raise ValueError(f"Missing row number")
            if row[1] == "{}":
                raise ValueError(f"Invalid format for row {row[0]}: {row[1]}")
            if setFormatChecker(str(row[1])) == False:
                raise ValueError(f"Invalid format for row {row[0]}: {row[1]}")
            if row[2] == "":
                raise ValueError(f"Invalid format for row {row[0]}: {row[2]}")
            if row[3] == "":
                raise ValueError(f"Invalid format for row {row[0]}: {row[3]}")
            if row[4] == "":
                raise ValueError(f"Invalid format for row {row[0]}: {row[4]}")
            
            keys = set(eval(row[1]))
            batchCommand = row[2]
            creationDate = row[3]
            name = row[4]
            parsedRow = [keys, batchCommand, creationDate, name]
            if includeRowNumber:
                parsedRow.insert(0, int(row[0]))
            parsedData.append(parsedRow)

    return parsedData

def shortcutWriter(filename, parsedData: list):
    """
    Writes a new row to the given CSV file with the provided parsed data.

    Parameters:
        filename (str): The name of the CSV file to write to.
        parsedData (list): A list of data to write to the CSV file.

    Returns:
        None
    """
    if len(parsedData) != 4:
        raise ValueError("Invalid number of arguments for shortcutWriter")
    if setFormatChecker(str(parsedData[0])) == False:
        raise ValueError("Invalid format for shortcutWriter[1]")
    allottedID = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == []:
                continue
            if allottedID < int(row[0]):
                allottedID = int(row[0]) + 1
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([allottedID, parsedData[0], parsedData[1], parsedData[2], parsedData[3]])

def csvShortcutDeleter(filename, id, parsedData):
    """
    Wolfoverflow
    Deletes a shortcut from the specified CSV file.

    Args:
        filename (str): The name of the CSV file.
        id (int): The ID of the shortcut to delete.
        parsedData (list): The parsed data from the CSV file.

    Returns:
        None
    """
    global keystrokes
    correctedID = 0
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for currentID, shortcut in enumerate(parsedData):
            if currentID != id:
                print([correctedID, shortcut[0], shortcut[1], shortcut[2], shortcut[3]])
                print("ID of", currentID)
                writer.writerow([correctedID, shortcut[0], shortcut[1], shortcut[2], shortcut[3]])
                correctedID += 1
            else:
                print("Skipping ID", id)
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))


def keystrokeParser(parsedData):
    """
    Wolfoverflow
    Parses the given parsedData and returns a list of keystrokes.

    Parameters:
        parsedData (list): A list of lists, where each list represents a component of a shortcut.

    Returns:
        set: A set of keystrokes.
    """
    keystrokes = []
    for shortcut in parsedData:
        keystrokes.append(shortcut[0])
    return keystrokes

def commandRunner(id, parsedData):
    """
    Wolfoverflow
    Executes the command associated with the given shortcut.

    Parameters:
        id (int): The ID of the shortcut to execute.
        parsedData (list): A list of lists, where each list represents a component of a shortcut.

    Returns:
        None
    """
    global recording
    os.system(parsedData[id][1])

keystrokes = keystrokeParser(csvParser("keylogger.csv"))
keyLogger = KeyLogger(keystrokes)

# Start the listener
def keyboardListener():
    """
    Starts the keyboard listener.

    Parameters:
        None

    Returns:
        None
    """
    with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

thread = threading.Thread(target=keyboardListener)
thread.start()

def shortcutMaker(name, command, shortcut):
    global keystrokes
    shortcutData = [shortcut, command, time.strftime("%d/%m/%Y"), name]
    shortcutWriter("keylogger.csv", shortcutData)
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))

def shortcutEditor(id, shortcutData):
    global keystrokes
    csvShortcutDeleter("keylogger.csv", id, shortcutData)
    shortcutWriter("keylogger.csv", shortcutData)
    csvCleaner("keylogger.csv")
    keystrokes = keystrokeParser(csvParser("keylogger.csv"))

def csvCleaner(filename):
    with open(filename, 'r') as r:
        formattedData = []
        currentID = 0
        reader = csv.reader(r)
        for row in reader:
            if row == []:
                continue
            if row in formattedData:
                continue
            if row[0] != currentID:
                row[0] = currentID
            formattedData.append(row)
            currentID += 1

        with open(filename, 'w', newline = '' if os.name == 'nt' else '\n') as w: # Weird formatting fix for windows
            writer = csv.writer(w)
            writer.writerows(formattedData)


def editingMode():
    global keystrokes
    if "y"==input("Create shortcut? (y/n): "):
        name = input("Enter shortcut name: ")
        startRecording()
        print("Recording started. Please hold shortcut for 3 seconds.")
        time.sleep(2.5)
        shortcut = stopRecording()
        time.sleep(0.5)
        print(f"Captured shortcut: {shortcut}")
        keyLogger.recordedKeys = []
        while True:
            command = input("Enter action: ")
            if command == "":
                print("Empty field, please try again.")
                continue
            try:
                subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                break
            except subprocess.CalledProcessError as e:
                print(f"'{command}' failed with error: {e}")
        
        shortcutData = [shortcut, command, time.strftime("%d/%m/%Y"), name]
        shortcutWriter("keylogger.csv", shortcutData)
        keystrokes = keystrokeParser(csvParser("keylogger.csv"))
        print("The shortcut has been saved.")
    else:
        id = str(input("Enter shortcut ID to delete: "))
        if "" == id:
            print("Invalid ID.")
            return
        try:
            id = int(id)
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
        print("Shortcut deleted.")
        csvShortcutDeleter("keylogger.csv", int(id), csvParser("keylogger.csv"))
# Note: The following section will no longer be utilised in the tkinter version.

if __name__ == "__main__":
    while True:
        try:
            editingMode() if "y"==input("Edit shortcuts? (y/n): ") else False
            
        except KeyboardInterrupt:
            print("Quitting keylogger...")
            csvCleaner("keylogger.csv")
            os.kill(os.getpid(), 9)
