

# Python Modules Documentation

## Introduction

Python modules are files containing reusable code, such as functions, classes, and variables. They help programmers organize their code and use existing features without writing everything from scratch.

This documentation covers four built-in Python modules, their purposes, important functions, and practical code examples.

### Modules Covered

| No. | Module | Main Purpose |
|---|---|---|
| 1 | `tkinter` | Creating graphical user interfaces |
| 2 | `datetime` | Working with dates and time |
| 3 | `json` | Storing and retrieving data |
| 4 | `os` | Managing files and directories |

---

# 1. Tkinter Module

## Overview

`tkinter` is Python's standard module for creating graphical user interfaces (GUIs). A GUI allows users to interact with an application through visual elements such as windows, buttons, labels, and text fields.

It is commonly used for developing desktop applications because it provides built-in tools for designing interactive interfaces.

## Common Functions and Components

| Function / Component | Description |
|---|---|
| `Tk()` | Creates the main application window. |
| `Label()` | Displays text or information. |
| `Button()` | Creates a clickable button. |
| `Entry()` | Creates a single-line text input field. |
| `pack()` | Arranges widgets inside their parent container. |
| `mainloop()` | Keeps the application running and responsive. |

## Code Examples

### Example 1: Creating a Window

```python
import tkinter as tk

root = tk.Tk()
root.title("My First Application")
root.geometry("400x300")

root.mainloop()
```

**Explanation:**

- `tk.Tk()` initializes the main window.
- `title()` sets the window's title.
- `geometry()` defines the window's width and height.
- `mainloop()` keeps the window open and responsive.

**Expected Output:** A window titled "My First Application" with a size of 400 by 300 pixels.

### Example 2: Adding a Label

```python
import tkinter as tk

root = tk.Tk()

label = tk.Label(root, text="Welcome to Python!")
label.pack()

root.mainloop()
```

**Explanation:**

- `Label()` creates a text widget.
- `root` identifies the window where the label will appear.
- `text` specifies the message to display.
- `pack()` places the label inside the window.

**Expected Output:** A window displaying "Welcome to Python!"

### Example 3: Creating a Button

```python
import tkinter as tk

root = tk.Tk()

button = tk.Button(root, text="Click Me")
button.pack()

root.mainloop()
```

**Explanation:**

- `Button()` creates the button widget.
- `text` defines the words displayed on the button.
- `pack()` arranges the button inside the window.

**Expected Output:** A window containing a button labeled "Click Me".

---

# 2. Datetime Module

## Overview

`datetime` is a built-in Python module used for working with dates and time. It provides tools for retrieving the current date and time, formatting time values, comparing dates, and performing time-related calculations.

It is useful in applications involving schedules, reminders, calendars, and other time-based activities.

## Common Functions and Methods

| Function / Method | Description |
|---|---|
| `datetime.now()` | Gets the current local date and time. |
| `strftime()` | Converts a date or time into a formatted string. |
| `strptime()` | Converts a formatted string into a datetime object. |
| `date.today()` | Gets the current local date. |
| `timedelta()` | Represents a duration or difference between dates and times. |

## Code Examples

### Example 1: Getting the Current Date and Time

```python
from datetime import datetime

now = datetime.now()

print(now)
```

**Explanation:**

- `datetime.now()` gets the current local date and time.
- The result is stored in the variable `now`.
- `print()` displays the retrieved information.

**Expected Output:** A date and time similar to `2026-11-20 08:30:15`. The actual result depends on when the program runs.

### Example 2: Formatting the Current Time

```python
from datetime import datetime

now = datetime.now()

formatted_time = now.strftime("%I:%M %p")

print(formatted_time)
```

**Explanation:**

- `%I` represents the hour in 12-hour format.
- `%M` represents the minutes.
- `%p` displays AM or PM.
- `strftime()` converts the datetime value into the specified format.

**Expected Output:** A time such as `08:30 AM`.

### Example 3: Comparing the Current Time with an Alarm

```python
from datetime import datetime

alarm_time = "07:00 AM"
current_time = datetime.now().strftime("%I:%M %p")

if current_time == alarm_time:
    print("Alarm is ringing!")
else:
    print("Waiting for alarm...")
```

**Explanation:**

- `alarm_time` stores the scheduled time.
- `datetime.now()` retrieves the current time.
- `strftime()` formats the current time.
- The `if` statement checks whether the two values match.

**Expected Output:** The program displays "Alarm is ringing!" if the current time matches the scheduled alarm. Otherwise, it displays "Waiting for alarm..."

**Note:** This is a basic demonstration. A complete alarm application would need to check the time repeatedly.

---

# 3. JSON Module

## Overview

`json` is a built-in Python module used to encode and decode JSON data.

JSON stands for JavaScript Object Notation. It is a lightweight data format commonly used to store and exchange information between applications.

Python's JSON module allows programmers to convert Python dictionaries and lists into JSON format and retrieve that information when needed.

## Common Functions

| Function | Description |
|---|---|
| `json.dump()` | Writes Python data into a JSON file. |
| `json.load()` | Reads JSON data from a file. |
| `json.dumps()` | Converts Python data into a JSON string. |
| `json.loads()` | Converts a JSON string into Python data. |

## Code Examples

### Example 1: Converting Python Data into JSON

```python
import json

student = {
    "name": "Alex",
    "age": 17,
    "course": "Computer Science"
}

result = json.dumps(student, indent=4)

print(result)
```

**Explanation:**

- `student` contains information stored as key-value pairs.
- `json.dumps()` converts the dictionary into JSON text.
- `indent=4` makes the output easier to read.
- `print()` displays the converted data.

**Expected Output:**

```json
{
    "name": "Alex",
    "age": 17,
    "course": "Computer Science"
}
```

### Example 2: Saving Data into a JSON File

```python
import json

student = {
    "name": "Alex",
    "age": 17
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)
```

**Explanation:**

- `open()` accesses or creates the file.
- `"w"` opens the file in write mode.
- `json.dump()` writes the dictionary into the file.
- `with` automatically closes the file after the operation.

**Expected Output:** A `student.json` file containing the saved student information.

### Example 3: Loading Data from a JSON File

```python
import json

with open("student.json", "r") as file:
    student = json.load(file)

print(student["name"])
```

**Explanation:**

- `"r"` opens the file in read mode.
- `json.load()` reads the JSON data and converts it into a Python dictionary.
- `student["name"]` accesses the value associated with the `"name"` key.

**Expected Output:**

```text
Alex
```

---

# 4. OS Module

## Overview

`os` is a built-in Python module that allows programs to interact with the operating system. It provides functions for managing files and folders, checking file paths, creating directories, and accessing information about the computer's environment.

It is useful when developing applications that need to organize or locate files automatically.

## Common Functions

| Function | Description |
|---|---|
| `os.path.exists()` | Checks whether a file or directory exists. |
| `os.makedirs()` | Creates a directory, including parent directories when needed. |
| `os.getcwd()` | Returns the current working directory. |
| `os.path.join()` | Combines folder and file names into a valid path. |
| `os.listdir()` | Lists the contents of a directory. |

## Code Examples

### Example 1: Checking if a File Exists

```python
import os

if os.path.exists("student.json"):
    print("File found!")
else:
    print("File not found.")
```

**Explanation:**

- `os.path.exists()` checks the specified file path.
- The `if` statement determines which message should be displayed.
- If the file exists, the program displays "File found!"
- Otherwise, it displays "File not found."

**Expected Output:** The message depends on whether the file exists.

### Example 2: Creating a Folder

```python
import os

os.makedirs("student_files", exist_ok=True)

print("Folder created successfully!")
```

**Explanation:**

- `os.makedirs()` creates the specified directory.
- `exist_ok=True` prevents an error if the folder already exists.
- `print()` displays a confirmation message.

**Expected Output:** A folder named `student_files` is created if it does not already exist.

### Example 3: Getting the Current Working Directory

```python
import os

location = os.getcwd()

print(location)
```

**Explanation:**

- `os.getcwd()` retrieves the directory where the program is currently running.
- The result is stored in `location`.
- `print()` displays the directory path.

**Expected Output:** A file path showing the current working directory, such as `C:\Users\User\Documents`.

---

# Conclusion

Python modules make programming more organized and efficient by providing reusable tools for different tasks. Instead of writing every feature from scratch, programmers can import modules that already contain useful functions and components.

The four modules discussed in this documentation demonstrate different areas of Python programming:

- `tkinter` is used to create graphical interfaces.
- `datetime` is used to manage dates and time.
- `json` is used to store and retrieve structured information.
- `os` is used to manage files and directories.

Understanding these modules helps programmers develop applications that are more functional, organized, and easier to maintain.

---

# References

- [Python Documentation – Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Python Documentation – Datetime](https://docs.python.org/3/library/datetime.html)
- [Python Documentation – JSON](https://docs.python.org/3/library/json.html)
- [Python Documentation – OS](https://docs.python.org/3/library/os.html)
