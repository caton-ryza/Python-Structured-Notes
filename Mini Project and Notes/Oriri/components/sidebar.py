
import tkinter as tk
from PIL import Image, ImageDraw, ImageFilter, ImageTk


class Sidebar(tk.Frame):

    WIDTH = 245

    def __init__(self, parent, navigate_callback):

        self.colors = {
            "sidebar": "#A9C7B1",
            "sidebar_light": "#C2D9C5",
            "sidebar_active": "#DCEBDD",
            "sidebar_text": "#294B3B",
            "text": "#315642",
            "muted": "#789381",
            "card": "#F8FAF5",
            "border": "#C9DCC9",
            "primary": "#47775D",
            "secondary": "#A9C7B1",
            "accent": "#8CA875",
        }

        super().__init__(
            parent,
            width=self.WIDTH,
            bg=self.colors["sidebar"],
            highlightthickness=0
        )

        self.navigate_callback = navigate_callback
        self.active_page = "overview"
        self.buttons = {}

        self.pack_propagate(False)

        self.canvas = tk.Canvas(
            self,
            width=self.WIDTH,
            bg=self.colors["sidebar"],
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_background)

        self.build_content()
        self.set_theme(self.colors)

    # ======================================================
    # COLOR UTILITIES
    # ======================================================

    def hex_to_rgb(self, value):

        value = value.lstrip("#")

        return tuple(
            int(value[i:i + 2], 16)
            for i in (0, 2, 4)
        )

    # ======================================================
    # BACKGROUND DESIGN
    # ======================================================

    def draw_background(self, event=None):

        width = max(self.winfo_width(), self.WIDTH)
        height = max(self.winfo_height(), 600)

        colors = self.colors

        top = self.hex_to_rgb(colors["sidebar_light"])
        bottom = self.hex_to_rgb(colors["sidebar"])

        image = Image.new("RGB", (width, height))
        pixels = image.load()

        for y in range(height):

            ratio = y / max(height - 1, 1)

            color = tuple(
                int(
                    top[i] * (1 - ratio)
                    + bottom[i] * ratio
                )
                for i in range(3)
            )

            for x in range(width):
                pixels[x, y] = color

        image = image.convert("RGBA")

        # Soft atmospheric glow
        glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(glow)

        accent = self.hex_to_rgb(colors["accent"])

        draw.ellipse(
            (-100, 100, 230, 480),
            fill=(*accent, 55)
        )

        draw.ellipse(
            (width - 130, height - 250, width + 90, height + 80),
            fill=(*accent, 40)
        )

        glow = glow.filter(
            ImageFilter.GaussianBlur(65)
        )

        image = Image.alpha_composite(image, glow)

        # Botanical leaf details
        leaves = Image.new("RGBA", image.size, (0, 0, 0, 0))
        leaf_draw = ImageDraw.Draw(leaves)

        for i in range(9):

            x = width - 20 - (i % 2) * 42
            y = height - 250 + i * 27

            leaf_draw.ellipse(
                (x - 20, y - 42, x + 20, y + 42),
                fill=(*accent, 45),
                outline=(*self.hex_to_rgb(colors["card"]), 65)
            )

        leaves = leaves.filter(
            ImageFilter.GaussianBlur(4)
        )

        image = Image.alpha_composite(image, leaves)

        self.background_photo = ImageTk.PhotoImage(image)

        self.canvas.delete("background")

        self.canvas.create_image(
            0,
            0,
            image=self.background_photo,
            anchor="nw",
            tags="background"
        )

        self.canvas.tag_lower("background")

    # ======================================================
    # SIDEBAR CONTENT
    # ======================================================

    def build_content(self):

        colors = self.colors

        # --------------------------------------------------
        # BRAND
        # --------------------------------------------------

        self.brand = tk.Frame(
            self.canvas,
            bg=colors["sidebar"]
        )

        self.canvas.create_window(
            25,
            35,
            window=self.brand,
            anchor="nw"
        )

        self.emblem = tk.Canvas(
            self.brand,
            width=40,
            height=40,
            highlightthickness=0,
            bg=colors["sidebar"]
        )

        self.emblem.pack(side="left")

        self.emblem.create_oval(
            3, 3, 37, 37,
            outline=colors["card"],
            width=1
        )

        self.emblem.create_oval(
            13, 7, 27, 29,
            fill=colors["accent"],
            outline=""
        )

        self.emblem.create_line(
            20, 12, 20, 31,
            fill=colors["primary"],
            width=2
        )

        self.brand_text = tk.Frame(
            self.brand,
            bg=colors["sidebar"]
        )

        self.brand_text.pack(
            side="left",
            padx=(10, 0)
        )

        self.brand_title = tk.Label(
            self.brand_text,
            text="ORIRI",
            font=("Georgia", 18, "bold"),
            bg=colors["sidebar"],
            fg=colors["sidebar_text"]
        )

        self.brand_title.pack(anchor="w")

        self.brand_subtitle = tk.Label(
            self.brand_text,
            text="A QUIETER START",
            font=("Arial", 7, "bold"),
            bg=colors["sidebar"],
            fg=colors["muted"]
        )

        self.brand_subtitle.pack(
            anchor="w",
            pady=(1, 0)
        )

        # --------------------------------------------------
        # TOP DIVIDER
        # --------------------------------------------------

        self.divider_top = self.canvas.create_line(
            24, 105, 220, 105,
            fill=colors["border"],
            width=1
        )

        # --------------------------------------------------
        # NAVIGATION HEADING
        # --------------------------------------------------

        self.workspace_heading = self.canvas.create_text(
            27,
            140,
            text="WORKSPACE",
            fill=colors["muted"],
            font=("Arial", 8, "bold"),
            anchor="w"
        )

        navigation = [
            ("overview", "⌂", "Overview"),
            ("alarms", "◷", "My Alarms"),
            ("themes", "✧", "Themes"),
            ("settings", "⚙", "Settings"),
        ]

        for index, (page, symbol, label) in enumerate(navigation):

            y = 174 + index * 61

            item = tk.Frame(
                self.canvas,
                bg=colors["sidebar"],
                width=205,
                height=47
            )

            item.pack_propagate(False)

            self.canvas.create_window(
                20,
                y,
                window=item,
                anchor="nw"
            )

            button = tk.Button(
                item,
                text=f"   {symbol}     {label}",
                font=("Arial", 10),
                anchor="w",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=9,
                command=lambda p=page: self.navigate(p)
            )

            button.pack(
                fill="both",
                expand=True
            )

            self.buttons[page] = button

        # --------------------------------------------------
        # BOTTOM SECTION
        # --------------------------------------------------

        self.divider_bottom = self.canvas.create_line(
            24, 450, 220, 450,
            fill=colors["border"],
            width=1
        )

        self.space_heading = self.canvas.create_text(
            27,
            480,
            text="YOUR SPACE",
            fill=colors["muted"],
            font=("Arial", 8, "bold"),
            anchor="w"
        )

        self.bottom_label = tk.Label(
            self.canvas,
            text="A little more calm,\none morning at a time.",
            bg=colors["sidebar"],
            fg=colors["sidebar_text"],
            font=("Georgia", 11),
            justify="left"
        )

        self.canvas.create_window(
            27,
            515,
            window=self.bottom_label,
            anchor="nw"
        )

        self.footer = self.canvas.create_text(
            27,
            585,
            text="ORIRI  •  BOTANICAL EDITION",
            fill=colors["muted"],
            font=("Arial", 7, "bold"),
            anchor="w"
        )

        self.set_active("overview")

    # ======================================================
    # APPLY GLOBAL THEME
    # ======================================================

    def set_theme(self, colors):

        self.colors = colors

        sidebar = colors["sidebar"]
        sidebar_text = colors.get(
            "sidebar_text",
            colors["text"]
        )

        self.configure(bg=sidebar)
        self.canvas.configure(bg=sidebar)

        self.brand.configure(bg=sidebar)
        self.brand_text.configure(bg=sidebar)

        self.brand_title.configure(
            bg=sidebar,
            fg=sidebar_text
        )

        self.brand_subtitle.configure(
            bg=sidebar,
            fg=colors["muted"]
        )

        self.emblem.configure(bg=sidebar)

        self.emblem.itemconfigure(
            1,
            outline=colors["card"]
        )

        self.emblem.itemconfigure(
            2,
            fill=colors["accent"]
        )

        self.emblem.itemconfigure(
            3,
            fill=colors["primary"]
        )

        self.bottom_label.configure(
            bg=sidebar,
            fg=sidebar_text
        )

        self.canvas.itemconfigure(
            self.divider_top,
            fill=colors["border"]
        )

        self.canvas.itemconfigure(
            self.divider_bottom,
            fill=colors["border"]
        )

        self.canvas.itemconfigure(
            self.workspace_heading,
            fill=colors["muted"]
        )

        self.canvas.itemconfigure(
            self.space_heading,
            fill=colors["muted"]
        )

        self.canvas.itemconfigure(
            self.footer,
            fill=colors["muted"]
        )

        self.set_active(self.active_page)
        self.draw_background()

    # ======================================================
    # NAVIGATION
    # ======================================================

    def navigate(self, page):

        self.set_active(page)
        self.navigate_callback(page)

    def set_active(self, page):

        self.active_page = page

        colors = self.colors

        for name, button in self.buttons.items():

            if name == page:

                button.configure(
                    bg=colors["sidebar_active"],
                    fg=colors["primary"],
                    activebackground=colors["sidebar_active"],
                    activeforeground=colors["primary"],
                    font=("Arial", 10, "bold")
                )

            else:

                button.configure(
                    bg=colors["sidebar"],
                    fg=colors.get("sidebar_text", colors["text"]),
                    activebackground=colors["sidebar_light"],
                    activeforeground=colors["primary"],
                    font=("Arial", 10)
                )




