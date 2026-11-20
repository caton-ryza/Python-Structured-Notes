# Oriri
### A quieter start to every day.
Oriri is a desktop alarm and daily routine application developed using Python. It provides a simple and calming space for users to manage their alarms, organize their mornings, and personalize their experience through different themes.
## Features
- **Dashboard** – Displays the current time, date, greeting, next scheduled alarm, and upcoming alarms.
- **Alarm Management** – Allows users to create, edit, enable, disable, and delete alarms.
- **Repeat Options** – Lets users schedule alarms for specific days of the week.
- **Alarm Notifications** – Displays an alarm popup when a scheduled alarm goes off, with options to snooze or dismiss.
- **Theme Customization** – Includes five available themes: Rosé Garden, Meadow, Ocean, Linen, and Mist.
- **Settings** – Provides options for customizing application preferences and managing available sounds.
## Technologies Used
| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Creates the graphical user interface (GUI) |
| JSON | Stores alarm information and application data |
| datetime | Handles current time, dates, and alarm scheduling |
| Pillow (PIL) | Processes and displays images used in the interface |
## Project Structure
```text
Oriri/
│
├── assets/
│   └── sounds/
│
├── components/
│   ├── alarm_popup.py
│   └── sidebar.py
│
├── data/
│   ├── alarms.json
│   └── settings.json
│
├── modules/
│   ├── alarm_manager.py
│   ├── clock.py
│   ├── sound_manager.py
│   └── storage.py
│
├── pages/
│   ├── dashboard.py
│   ├── alarms.py
│   ├── themes.py
│   └── settings_page.py
│
└── main.py
```
## How It Works
Oriri uses different Python modules to handle its features:
- **Tkinter** manages the application's windows, buttons, pages, and other interface elements.
- **JSON** saves alarm details and other stored information so they can be loaded again when the application is reopened.
- **datetime** provides time and date information used by the dashboard and alarm scheduling system.
- **Pillow** helps process images used in the application's visual design.
These technologies work together to make Oriri a functional desktop application.
## Installation and Setup
1. Clone or download this repository.
2. Open the project folder in Visual Studio Code.
3. Make sure Python is installed.
4. Install the required library:
```bash
pip install pillow
```
5. Run the application:
```bash
python main.py
```
If you use additional sound-related dependencies, install those separately when supported by your Python version.
## Project Purpose
---
Oriri was developed as a Python mini project to demonstrate the use of Python modules, file handling, data storage, and graphical user interface development.
The project also explores how different components can work together to create an organized and interactive desktop application.
---
**Developed as a Python Mini Project.**
