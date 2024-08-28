
def translator(x):
    # Mapping dictionary
    translations = {
        "x01": "a",
        "x02": "b",
        "x03": "c",
        "x04": "d",
        "x05": "e",
        "x06": "f",
        "x07": "g",
        "x08": "h",
        "x09": "i",
        "x0a": "j",
        "x0b": "k",
        "x0c": "l",
        "x0d": "m",
        "x0e": "n",
        "x0f": "o",
        "x10": "p",
        "x11": "q",
        "x12": "r",
        "x13": "s",
        "x14": "t",
        "x15": "u",
        "x16": "v",
        "x17": "w",
        "x18": "x",
        "x19": "y",
        "x1a": "z",
        "x1b": "[",
        "x1c": "\\",
        "x1d": "]",
        "x1e": "^",
        "x1f": "_",
        "x20": " ",
        "x21": "!",
        "x22": '"',
        "x23": "#",
        "x24": "$",
        "x25": "%",
        "x26": "&",
        "x27": "'",
        "x28": "(",
        "x29": ")",
        "x2a": "*",
        "x2b": "+",
        "x2c": ",",
        "x2d": "-",
        "x2e": ".",
        "x2f": "/"


    }
    # Remove backslash

    x = x.strip("\\")
    # Check if the key is in the dictionary
    if x in translations:
        # If it is, return the translation
        return translations[x]
    
    # If it's not, return the original key
    return x



