
import tkinter as tk
from tkinter import messagebox

# ==========================================================
# ORIRI — APPLICATION IMPORTS
# ==========================================================

from components.sidebar import Sidebar
from components.alarm_popup import AlarmPopup

from pages.dashboard import Dashboard
from pages.alarms import AlarmsPage
from pages.themes import ThemesPage
from pages.settings_page import SettingsPage

from modules.alarm_manager import AlarmManager
from modules.storage import storage


# ==========================================================
# ORIRI — THEME COLLECTION
# ==========================================================

THEMES = {
    "Rosé Garden": {
        "bg": "#F1EAE7", "panel": "#F7F0ED", "card": "#FFF9F5",
        "sidebar": "#795B59", "sidebar_light": "#A98A84",
        "sidebar_active": "#E9D8D1", "sidebar_text": "#FFF9F5",
        "text": "#594442", "muted": "#A38B85", "primary": "#956D70",
        "secondary": "#D8BDB9", "accent": "#B88D91",
        "accent_light": "#F0DFDA", "border": "#E5D1CB",
        "flower": "#E8C3B9"
    },
    "Meadow": {
        "bg": "#EAF1E8", "panel": "#F1F6EF", "card": "#F8FAF5",
        "sidebar": "#315B49", "sidebar_light": "#71947D",
        "sidebar_active": "#D5E5D5", "sidebar_text": "#F8FAF5",
        "text": "#315642", "muted": "#789381", "primary": "#47775D",
        "secondary": "#A9C7B1", "accent": "#8CA875",
        "accent_light": "#D5E5D5", "border": "#C9DCC9",
        "flower": "#E5C6A4"
    },
    "Ocean": {
        "bg": "#E8F0F2", "panel": "#EFF5F6", "card": "#F8FBFC",
        "sidebar": "#345B68", "sidebar_light": "#7299A3",
        "sidebar_active": "#D2E4E8", "sidebar_text": "#F8FBFC",
        "text": "#31515B", "muted": "#78949D", "primary": "#477C89",
        "secondary": "#A9C8CE", "accent": "#78A7A7",
        "accent_light": "#D7E9E9", "border": "#C9DDE0",
        "flower": "#D9C8B4"
    },
    "Linen": {
        "bg": "#F2EEE5", "panel": "#F7F3EA", "card": "#FCFAF5",
        "sidebar": "#756A55", "sidebar_light": "#A99B7C",
        "sidebar_active": "#E9E0CC", "sidebar_text": "#FCFAF5",
        "text": "#514A3C", "muted": "#978B75", "primary": "#887957",
        "secondary": "#D0C3A5", "accent": "#A99B70",
        "accent_light": "#EEE7D5", "border": "#DED5C1",
        "flower": "#D9BDA0"
    },
    "Mist": {
        "bg": "#EBEEF0", "panel": "#F2F4F5", "card": "#FAFBFC",
        "sidebar": "#505E68", "sidebar_light": "#8999A1",
        "sidebar_active": "#DCE3E7", "sidebar_text": "#FAFBFC",
        "text": "#3F4E57", "muted": "#84939A", "primary": "#647F8C",
        "secondary": "#B8C9CF", "accent": "#8DA8AA",
        "accent_light": "#DFE9E9", "border": "#D1DCE0",
        "flower": "#D9CFC0"
    }
}


# ==========================================================
# ORIRI — APPLICATION
# ==========================================================

class OririApp:

    def __init__(self, root):

        self.root = root

        # Window setup
        self.root.overrideredirect(True)
        self.root.geometry("1280x820")
        self.root.minsize(1050, 680)

        # Window state
        self.is_maximized = False
        self.is_minimized = False
        self.normal_geometry = self.root.geometry()

        # Window dragging
        self.drag_x = 0
        self.drag_y = 0

        # Application state
        self.current_page = "overview"
        self.current_page_widget = None

        # Theme setup
        self.themes = THEMES
        self.selected_theme = self.load_saved_theme()
        self.theme = THEMES[self.selected_theme]

        self.root.configure(bg=self.theme["bg"])

        # Alarm system
        self.alarm_manager = AlarmManager()
        self.active_popup = None
        self.alarm_queue = []

        # Smooth scrolling state
        self.scroll_target = 0
        self.scroll_job = None
        self.scroll_speed = 0.22

        # Restore custom title bar after minimizing
        self.root.bind("<Map>", self.on_window_map, add="+")

        # Build interface
        self.build_layout()

        # Start alarm checking
        self.check_alarm_schedule()

    # ======================================================
    # CUSTOM WINDOW BAR
    # ======================================================

    def create_title_bar(self):

        c = self.theme

        self.title_bar = tk.Frame(
            self.root,
            bg=c["sidebar"],
            height=38
        )
        self.title_bar.pack(fill="x", side="top")
        self.title_bar.pack_propagate(False)

        self.title_label = tk.Label(
            self.title_bar,
            text="  ORIRI  |  A quieter start to every day.",
            bg=c["sidebar"],
            fg=c["sidebar_text"],
            font=("Georgia", 10),
            anchor="w"
        )
        self.title_label.pack(side="left", fill="y")

        # Close button
        self.close_button = tk.Button(
            self.title_bar,
            text="×",
            command=self.close_application,
            bg=c["sidebar"],
            fg=c["sidebar_text"],
            activebackground="#B96C70",
            activeforeground="#FFFFFF",
            font=("Arial", 19),
            bd=0,
            relief="flat",
            cursor="hand2",
            width=4
        )
        self.close_button.pack(side="right", fill="y")

        # Maximize / Restore button
        self.maximize_button = tk.Button(
            self.title_bar,
            text="□",
            command=self.toggle_maximize,
            bg=c["sidebar"],
            fg=c["sidebar_text"],
            activebackground=c["sidebar_light"],
            activeforeground="#FFFFFF",
            font=("Arial", 13),
            bd=0,
            relief="flat",
            cursor="hand2",
            width=4
        )
        self.maximize_button.pack(side="right", fill="y")

        # Minimize button
        self.minimize_button = tk.Button(
            self.title_bar,
            text="—",
            command=self.minimize_window,
            bg=c["sidebar"],
            fg=c["sidebar_text"],
            activebackground=c["sidebar_light"],
            activeforeground="#FFFFFF",
            font=("Arial", 14),
            bd=0,
            relief="flat",
            cursor="hand2",
            width=4
        )
        self.minimize_button.pack(side="right", fill="y")

        # Window dragging
        for widget in (self.title_bar, self.title_label):
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag_window)

        # Hover effects
        self.close_button.bind(
            "<Enter>",
            lambda e: self.close_button.configure(
                bg="#B96C70",
                fg="#FFFFFF"
            )
        )

        self.close_button.bind(
            "<Leave>",
            lambda e: self.close_button.configure(
                bg=self.theme["sidebar"],
                fg=self.theme["sidebar_text"]
            )
        )

        for button in (self.minimize_button, self.maximize_button):

            button.bind(
                "<Enter>",
                lambda e, b=button: b.configure(
                    bg=self.theme["sidebar_light"]
                )
            )

            button.bind(
                "<Leave>",
                lambda e, b=button: b.configure(
                    bg=self.theme["sidebar"],
                    fg=self.theme["sidebar_text"]
                )
            )

    # ======================================================
    # WINDOW CONTROLS
    # ======================================================

    def minimize_window(self):

        try:
            self.is_minimized = True

            # Temporarily restore the Windows window frame
            # so Windows can minimize it to the taskbar.
            self.root.overrideredirect(False)
            self.root.iconify()

        except tk.TclError:
            self.is_minimized = False
            self.root.overrideredirect(True)

    def on_window_map(self, event=None):

        if self.is_minimized:
            self.root.after_idle(
                self.restore_custom_title_bar
            )

    def restore_custom_title_bar(self):

        if not self.root.winfo_exists():
            return

        try:
            self.root.overrideredirect(True)
            self.is_minimized = False

        except tk.TclError:
            pass

    def toggle_maximize(self):

        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()

    def maximize_window(self):

        if self.is_maximized:
            return

        try:
            self.normal_geometry = self.root.geometry()

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            self.root.geometry(
                f"{screen_width}x{screen_height}+0+0"
            )

            self.is_maximized = True

            self.maximize_button.configure(
                text="❐"
            )

        except tk.TclError:
            pass

    def restore_window(self):

        if not self.is_maximized:
            return

        try:
            self.root.geometry(self.normal_geometry)

            self.is_maximized = False

            self.maximize_button.configure(
                text="□"
            )

        except tk.TclError:
            pass

    # ======================================================
    # WINDOW DRAGGING
    # ======================================================

    def start_drag(self, event):

        if self.is_maximized:
            return

        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()

    def drag_window(self, event):

        if self.is_maximized:
            return

        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y

        self.root.geometry(f"+{x}+{y}")

    # ======================================================
    # STORAGE / SETTINGS
    # ======================================================

    def load_saved_theme(self):

        settings = storage.load_json("settings.json", {})

        theme_name = settings.get("theme", "Meadow")

        if theme_name not in THEMES:
            theme_name = "Meadow"

        return theme_name

    def save_theme(self, theme_name):

        settings = storage.load_json("settings.json", {})

        if not isinstance(settings, dict):
            settings = {}

        settings["theme"] = theme_name
        storage.save_json("settings.json", settings)

    # ======================================================
    # MAIN LAYOUT
    # ======================================================

    def build_layout(self):

        self.root.configure(bg=self.theme["bg"])

        # Custom title bar
        self.create_title_bar()

        # Main application area
        self.app_area = tk.Frame(
            self.root,
            bg=self.theme["bg"]
        )
        self.app_area.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = Sidebar(
            self.app_area,
            self.navigate
        )
        self.sidebar.pack(side="left", fill="y")

        # Main content wrapper
        self.main_area = tk.Frame(
            self.app_area,
            bg=self.theme["bg"]
        )
        self.main_area.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollable canvas
        self.main_canvas = tk.Canvas(
            self.main_area,
            bg=self.theme["bg"],
            highlightthickness=0,
            bd=0
        )
        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollbar
        self.main_scrollbar = tk.Scrollbar(
            self.main_area,
            orient="vertical",
            command=self.main_canvas.yview,
            bg=self.theme["panel"],
            troughcolor=self.theme["bg"],
            activebackground=self.theme["secondary"],
            relief="flat",
            bd=0,
            width=10
        )
        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.main_canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        # Page container
        self.page_container = tk.Frame(
            self.main_canvas,
            bg=self.theme["bg"]
        )

        self.page_window = self.main_canvas.create_window(
            (0, 0),
            window=self.page_container,
            anchor="nw"
        )

        self.page_container.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.main_canvas.bind(
            "<Configure>",
            self.resize_page_container
        )

        # Mouse wheel bindings
        self.root.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.root.bind_all(
            "<Button-4>",
            self.on_mousewheel_linux
        )

        self.root.bind_all(
            "<Button-5>",
            self.on_mousewheel_linux
        )

        self.navigate("overview")

    # ======================================================
    # SCROLLING
    # ======================================================

    def update_scroll_region(self, event=None):

        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )

    def resize_page_container(self, event):

        self.main_canvas.itemconfigure(
            self.page_window,
            width=event.width
        )

        self.update_scroll_region()

    def is_inside_main_area(self, widget):

        while widget is not None:

            if widget == self.main_area:
                return True

            try:
                widget = widget.master
            except AttributeError:
                return False

        return False

    def get_max_scroll(self):

        self.update_scroll_region()

        bbox = self.main_canvas.bbox("all")

        if not bbox:
            return 0

        content_height = bbox[3] - bbox[1]
        visible_height = self.main_canvas.winfo_height()

        return max(0, content_height - visible_height)

    def on_mousewheel(self, event):

        if not self.is_inside_main_area(event.widget):
            return

        max_scroll = self.get_max_scroll()

        if max_scroll <= 0:
            return "break"

        movement = (event.delta / 120) * 90

        if self.scroll_job is None:
            self.scroll_target = self.main_canvas.canvasy(0)

        self.scroll_target -= movement

        self.scroll_target = max(
            0,
            min(self.scroll_target, max_scroll)
        )

        if self.scroll_job is None:
            self.animate_scroll()

        return "break"

    def on_mousewheel_linux(self, event):

        if not self.is_inside_main_area(event.widget):
            return

        max_scroll = self.get_max_scroll()

        if max_scroll <= 0:
            return "break"

        if self.scroll_job is None:
            self.scroll_target = self.main_canvas.canvasy(0)

        if event.num == 4:
            self.scroll_target -= 90

        elif event.num == 5:
            self.scroll_target += 90

        self.scroll_target = max(
            0,
            min(self.scroll_target, max_scroll)
        )

        if self.scroll_job is None:
            self.animate_scroll()

        return "break"

    def animate_scroll(self):

        self.scroll_job = None

        if not self.main_canvas.winfo_exists():
            return

        max_scroll = self.get_max_scroll()

        self.scroll_target = max(
            0,
            min(self.scroll_target, max_scroll)
        )

        current_scroll = self.main_canvas.canvasy(0)
        difference = self.scroll_target - current_scroll

        bbox = self.main_canvas.bbox("all")

        if not bbox:
            return

        content_height = max(bbox[3], 1)

        if abs(difference) < 1:

            self.main_canvas.yview_moveto(
                self.scroll_target / content_height
            )
            return

        new_position = (
            current_scroll + difference * self.scroll_speed
        )

        self.main_canvas.yview_moveto(
            new_position / content_height
        )

        self.scroll_job = self.root.after(
            12,
            self.animate_scroll
        )

    def reset_scroll(self):

        if self.scroll_job is not None:

            try:
                self.root.after_cancel(self.scroll_job)
            except tk.TclError:
                pass

            self.scroll_job = None

        self.scroll_target = 0

        self.main_canvas.yview_moveto(0)

    # ======================================================
    # PAGE NAVIGATION
    # ======================================================

    def navigate(self, page_name):

        valid_pages = [
            "overview",
            "alarms",
            "themes",
            "settings"
        ]

        if page_name not in valid_pages:
            return

        self.current_page = page_name

        self.reset_scroll()

        for widget in self.page_container.winfo_children():
            widget.destroy()

        if page_name == "overview":
            page = Dashboard(self.page_container, self)

        elif page_name == "alarms":
            page = AlarmsPage(self.page_container, self)

        elif page_name == "themes":
            page = ThemesPage(self.page_container, self)

        elif page_name == "settings":
            page = SettingsPage(self.page_container, self)

        page.pack(fill="both", expand=True)

        self.current_page_widget = page

        self.root.after_idle(self.finish_page_layout)

    def finish_page_layout(self):

        self.root.update_idletasks()

        if self.current_page == "themes":

            page = self.current_page_widget

            if page and hasattr(page, "canvas") and hasattr(page, "content"):

                try:
                    content_height = page.content.winfo_reqheight() + 60
                    current_height = page.canvas.winfo_height()

                    required_height = max(
                        content_height,
                        current_height
                    )

                    if abs(
                        page.canvas.winfo_reqheight() - required_height
                    ) > 2:

                        page.canvas.configure(
                            height=required_height
                        )

                except tk.TclError:
                    pass

        self.update_scroll_region()

        self.scroll_target = 0
        self.main_canvas.yview_moveto(0)

    # ======================================================
    # THEME SWITCHING
    # ======================================================

    def set_theme(self, theme_name):

        if theme_name not in THEMES:
            return

        self.selected_theme = theme_name
        self.theme = THEMES[theme_name]

        self.save_theme(theme_name)

        self.root.configure(bg=self.theme["bg"])
        self.app_area.configure(bg=self.theme["bg"])
        self.main_area.configure(bg=self.theme["bg"])
        self.main_canvas.configure(bg=self.theme["bg"])
        self.page_container.configure(bg=self.theme["bg"])

        # Update custom title bar
        self.title_bar.configure(bg=self.theme["sidebar"])

        self.title_label.configure(
            bg=self.theme["sidebar"],
            fg=self.theme["sidebar_text"]
        )

        self.close_button.configure(
            bg=self.theme["sidebar"],
            fg=self.theme["sidebar_text"]
        )

        self.minimize_button.configure(
            bg=self.theme["sidebar"],
            fg=self.theme["sidebar_text"]
        )

        self.maximize_button.configure(
            bg=self.theme["sidebar"],
            fg=self.theme["sidebar_text"]
        )

        if hasattr(self.sidebar, "set_theme"):
            self.sidebar.set_theme(self.theme)

        elif hasattr(self.sidebar, "apply_theme"):
            self.sidebar.apply_theme(self.theme)

        self.navigate(self.current_page)

    # ======================================================
    # ALARM SCHEDULER
    # ======================================================

    def check_alarm_schedule(self):

        try:

            self.alarm_manager.load_alarms()

            triggered = self.alarm_manager.check_alarms()

            for alarm in triggered:
                self.alarm_queue.append(alarm)

            self.show_next_alarm()

        except Exception as error:
            print("Oriri alarm scheduler error:", error)

        self.root.after(
            1000,
            self.check_alarm_schedule
        )

    # ======================================================
    # SHOW ALARM POPUP
    # ======================================================

    def show_next_alarm(self):

        if self.active_popup is not None:
            return

        if not self.alarm_queue:
            return

        alarm = self.alarm_queue.pop(0)

        self.active_popup = AlarmPopup(
            self.root,
            alarm=alarm,
            colors=self.theme,
            on_dismiss=self.dismiss_alarm,
            on_snooze=self.snooze_alarm
        )

    # ======================================================
    # DISMISS ALARM
    # ======================================================

    def dismiss_alarm(self, alarm):

        self.active_popup = None

        self.root.after(
            200,
            self.show_next_alarm
        )

    # ======================================================
    # SNOOZE ALARM
    # ======================================================

    def snooze_alarm(self, alarm):

        self.alarm_manager.snooze_alarm(alarm)

        self.active_popup = None

        self.root.after(
            200,
            self.show_next_alarm
        )

    # ======================================================
    # APPLICATION CLOSE
    # ======================================================

    def close_application(self):

        try:
            self.alarm_manager.save_alarms()
        finally:
            self.root.destroy()


# ==========================================================
# ORIRI — START APPLICATION
# ==========================================================

def main():

    root = tk.Tk()

    app = OririApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
