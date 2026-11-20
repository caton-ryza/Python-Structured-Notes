
import tkinter as tk
import math
from PIL import Image, ImageDraw, ImageFilter, ImageTk


# ==========================================================
# ORIRI — THEME GALLERY
# ==========================================================

THEME_INFO = {
    "Rosé Garden": {
        "description": "A little romance in a botanical garden.",
        "tagline": "Blush petals, sage leaves, and soft mornings.",
        "mood": "ROMANTIC  •  BOTANICAL"
    },
    "Meadow": {
        "description": "A quiet morning surrounded by greenery.",
        "tagline": "Fresh sage, soft jade, and warm cream.",
        "mood": "FRESH  •  NATURAL"
    },
    "Ocean": {
        "description": "A calm, airy palette inspired by the sea.",
        "tagline": "Cool aqua, soft blue, and sea-glass tones.",
        "mood": "CALM  •  AIRY"
    },
    "Linen": {
        "description": "Warm, simple, and naturally understated.",
        "tagline": "Ivory, oatmeal, and gentle earthy details.",
        "mood": "WARM  •  TIMELESS"
    },
    "Mist": {
        "description": "A soft, dreamy atmosphere with muted color.",
        "tagline": "Dusty lavender, pale grey, and lilac tones.",
        "mood": "DREAMY  •  SOFT"
    }
}


class ThemesPage(tk.Frame):

    def __init__(self, parent, app=None):

        self.app = app

        self.colors = app.theme
        self.themes = app.themes
        self.selected_theme = app.selected_theme

        self.background_photo = None
        self.resize_job = None

        super().__init__(
            parent,
            bg=self.colors["bg"]
        )

        self.canvas = tk.Canvas(
            self,
            bg=self.colors["bg"],
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.background_item = self.canvas.create_image(
            0, 0,
            anchor="nw"
        )

        self.content = tk.Frame(
            self.canvas,
            bg=self.colors["bg"]
        )

        self.content_window = self.canvas.create_window(
            38,
            30,
            anchor="nw",
            window=self.content
        )

        self.canvas.bind(
            "<Configure>",
            self.on_resize
        )

        self.build_page()

        self.after(100, self.refresh_background)

    # ======================================================
    # COLOR UTILITIES
    # ======================================================

    def hex_rgb(self, color):

        color = color.lstrip("#")

        return tuple(
            int(color[i:i + 2], 16)
            for i in (0, 2, 4)
        )

    # ======================================================
    # BACKGROUND ARTWORK
    # ======================================================

    def create_background(self, width, height):

        c = self.colors

        image = Image.new(
            "RGBA",
            (width, height),
            c["bg"]
        )

        overlay = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(overlay)

        secondary = self.hex_rgb(c["secondary"])
        accent = self.hex_rgb(c["accent"])
        flower = self.hex_rgb(c["flower"])
        primary = self.hex_rgb(c["primary"])

        # Soft color atmosphere
        draw.ellipse(
            (-130, -150, 270, 250),
            fill=(*secondary, 65)
        )

        draw.ellipse(
            (width - 260, height - 300, width + 120, height + 100),
            fill=(*accent, 55)
        )

        # Botanical stems
        draw.line(
            [
                (20, height),
                (80, height - 180),
                (45, height - 300)
            ],
            fill=(*primary, 55),
            width=3
        )

        draw.line(
            [
                (width - 20, 0),
                (width - 85, 150),
                (width - 40, 270)
            ],
            fill=(*primary, 45),
            width=3
        )

        # Leaves
        for x, y, horizontal in [
            (50, height - 190, False),
            (75, height - 260, True),
            (width - 75, 110, False),
            (width - 60, 200, True)
        ]:

            if horizontal:
                bounds = (
                    x - 25, y - 10,
                    x + 25, y + 10
                )
            else:
                bounds = (
                    x - 10, y - 25,
                    x + 10, y + 25
                )

            draw.ellipse(
                bounds,
                fill=(*secondary, 100)
            )

        self.draw_flower(
            draw, 75, 85, 30, flower, accent
        )

        self.draw_flower(
            draw,
            width - 75,
            height - 95,
            38,
            flower,
            accent
        )

        overlay = overlay.filter(
            ImageFilter.GaussianBlur(1.5)
        )

        image = Image.alpha_composite(
            image,
            overlay
        )

        return ImageTk.PhotoImage(image)

    def draw_flower(self, draw, x, y, radius, petal, center):

        for angle in range(0, 360, 45):

            rad = math.radians(angle)

            px = x + math.cos(rad) * radius * 0.58
            py = y + math.sin(rad) * radius * 0.58

            r = radius * 0.42

            draw.ellipse(
                (px-r, py-r, px+r, py+r),
                fill=(*petal, 145)
            )

        r = radius * 0.24

        draw.ellipse(
            (x-r, y-r, x+r, y+r),
            fill=(*center, 200)
        )

    def on_resize(self, event):

        if event.width < 100:
            return

        if self.resize_job:
            self.after_cancel(self.resize_job)

        self.resize_job = self.after(
            80,
            self.refresh_background
        )

    def refresh_background(self):

        if not self.winfo_exists():
            return

        width = max(self.canvas.winfo_width(), 500)
        height = max(self.canvas.winfo_height(), 600)

        self.background_photo = self.create_background(
            width,
            height
        )

        self.canvas.itemconfigure(
            self.background_item,
            image=self.background_photo
        )

        self.canvas.itemconfigure(
            self.content_window,
            width=max(width - 76, 400)
        )

        self.canvas.tag_lower(
            self.background_item
        )

    # ======================================================
    # PAGE STRUCTURE
    # ======================================================

    def build_page(self):

        self.build_header()
        self.build_featured_preview()
        self.build_gallery()
        self.build_footer()

    # ======================================================
    # HEADER
    # ======================================================

    def build_header(self):

        c = self.colors

        self.header = tk.Frame(
            self.content,
            bg=c["bg"]
        )

        self.header.pack(
            fill="x",
            pady=(0, 23)
        )

        self.eyebrow = tk.Label(
            self.header,
            text="✦  MAKE YOUR SPACE YOURS",
            font=("Arial", 9, "bold"),
            fg=c["primary"],
            bg=c["bg"]
        )

        self.eyebrow.pack(anchor="w")

        self.heading = tk.Label(
            self.header,
            text="Find your atmosphere.",
            font=("Georgia", 30, "bold"),
            fg=c["text"],
            bg=c["bg"]
        )

        self.heading.pack(
            anchor="w",
            pady=(7, 3)
        )

        self.subtitle = tk.Label(
            self.header,
            text="A different little world for every kind of morning.",
            font=("Arial", 10),
            fg=c["muted"],
            bg=c["bg"]
        )

        self.subtitle.pack(anchor="w")

    # ======================================================
    # FEATURED PREVIEW
    # ======================================================

    def build_featured_preview(self):

        c = self.colors

        self.preview = tk.Frame(
            self.content,
            bg=c["card"],
            highlightbackground=c["border"],
            highlightthickness=1,
            padx=22,
            pady=20
        )

        self.preview.pack(
            fill="x",
            pady=(0, 27)
        )

        top = tk.Frame(
            self.preview,
            bg=c["card"]
        )

        top.pack(fill="x")

        self.preview_title = tk.Label(
            top,
            text="CURRENT ATMOSPHERE",
            font=("Arial", 8, "bold"),
            fg=c["muted"],
            bg=c["card"]
        )

        self.preview_title.pack(side="left")

        self.selected_badge = tk.Label(
            top,
            text="● ACTIVE THEME",
            font=("Arial", 8, "bold"),
            fg=c["primary"],
            bg=c["accent_light"],
            padx=12,
            pady=6
        )

        self.selected_badge.pack(side="right")

        self.preview_name = tk.Label(
            self.preview,
            text="",
            font=("Georgia", 23, "bold"),
            fg=c["text"],
            bg=c["card"]
        )

        self.preview_name.pack(
            anchor="w",
            pady=(13, 2)
        )

        self.preview_description = tk.Label(
            self.preview,
            text="",
            font=("Arial", 9),
            fg=c["muted"],
            bg=c["card"]
        )

        self.preview_description.pack(anchor="w")

        self.preview_art = tk.Canvas(
            self.preview,
            height=205,
            bg=c["bg"],
            highlightthickness=0
        )

        self.preview_art.pack(
            fill="x",
            pady=(18, 12)
        )

        self.preview_tagline = tk.Label(
            self.preview,
            text="",
            font=("Georgia", 11, "italic"),
            fg=c["primary"],
            bg=c["card"]
        )

        self.preview_tagline.pack(anchor="w")

        self.preview_mood = tk.Label(
            self.preview,
            text="",
            font=("Arial", 8, "bold"),
            fg=c["muted"],
            bg=c["card"]
        )

        self.preview_mood.pack(
            anchor="w",
            pady=(5, 0)
        )

        self.preview_art.bind(
            "<Configure>",
            lambda event: self.update_preview()
        )

        self.update_preview()

    def update_preview(self):

        if not hasattr(self, "preview_art"):
            return

        c = self.colors
        info = THEME_INFO[self.selected_theme]

        self.preview.configure(
            bg=c["card"],
            highlightbackground=c["border"]
        )

        self.preview_name.configure(
            text=self.selected_theme,
            bg=c["card"],
            fg=c["text"]
        )

        self.preview_description.configure(
            text=info["description"],
            bg=c["card"],
            fg=c["muted"]
        )

        self.preview_tagline.configure(
            text=info["tagline"],
            bg=c["card"],
            fg=c["primary"]
        )

        self.preview_mood.configure(
            text=info["mood"],
            bg=c["card"],
            fg=c["muted"]
        )

        self.selected_badge.configure(
            bg=c["accent_light"],
            fg=c["primary"]
        )

        self.preview_art.configure(
            bg=c["bg"]
        )

        self.preview_art.delete("all")

        width = max(
            self.preview_art.winfo_width(),
            500
        )

        height = 205

        # Background composition
        self.preview_art.create_rectangle(
            0, 0, width, height,
            fill=c["bg"],
            outline=""
        )

        self.preview_art.create_oval(
            -100, -100, 230, 240,
            fill=c["secondary"],
            outline=""
        )

        self.preview_art.create_oval(
            width - 250, -90,
            width + 100, 240,
            fill=c["accent_light"],
            outline=""
        )

        self.preview_art.create_oval(
            width - 180, 110,
            width + 40, 330,
            fill=c["accent"],
            outline=""
        )

        # Clock preview
        clock_x = width // 2
        clock_y = 105

        self.preview_art.create_rectangle(
            clock_x - 145,
            clock_y - 70,
            clock_x + 145,
            clock_y + 70,
            fill=c["card"],
            outline=c["border"],
            width=2
        )

        self.preview_art.create_text(
            clock_x,
            clock_y - 43,
            text="A QUIETER START",
            fill=c["muted"],
            font=("Arial", 8, "bold")
        )

        self.preview_art.create_text(
            clock_x,
            clock_y,
            text="07:30",
            fill=c["text"],
            font=("Consolas", 34, "bold")
        )

        self.preview_art.create_text(
            clock_x,
            clock_y + 43,
            text="GOOD MORNING",
            fill=c["primary"],
            font=("Arial", 8, "bold")
        )

        self.draw_canvas_flower(
            clock_x - 205,
            100,
            29,
            c["flower"],
            c["accent"]
        )

        self.draw_canvas_flower(
            clock_x + 205,
            100,
            29,
            c["flower"],
            c["accent"]
        )

    def draw_canvas_flower(self, x, y, radius, petal, center):

        for angle in range(0, 360, 60):

            rad = math.radians(angle)

            px = x + math.cos(rad) * radius * 0.55
            py = y + math.sin(rad) * radius * 0.55

            r = radius * 0.42

            self.preview_art.create_oval(
                px-r, py-r, px+r, py+r,
                fill=petal,
                outline=""
            )

        self.preview_art.create_oval(
            x-5, y-5, x+5, y+5,
            fill=center,
            outline=""
        )

    # ======================================================
    # THEME GALLERY
    # ======================================================

    def build_gallery(self):

        c = self.colors

        self.gallery_heading = tk.Frame(
            self.content,
            bg=c["bg"]
        )

        self.gallery_heading.pack(
            fill="x",
            pady=(0, 13)
        )

        self.gallery_title = tk.Label(
            self.gallery_heading,
            text="The collection",
            font=("Georgia", 20, "bold"),
            fg=c["text"],
            bg=c["bg"]
        )

        self.gallery_title.pack(side="left")

        self.gallery_count = tk.Label(
            self.gallery_heading,
            text="05 ATMOSPHERES",
            font=("Arial", 8, "bold"),
            fg=c["muted"],
            bg=c["bg"]
        )

        self.gallery_count.pack(
            side="right",
            pady=(8, 0)
        )

        self.gallery = tk.Frame(
            self.content,
            bg=c["bg"]
        )

        self.gallery.pack(fill="x")

        self.render_cards()

    def render_cards(self):

        for widget in self.gallery.winfo_children():
            widget.destroy()

        theme_names = list(self.themes.keys())

        for column in range(2):
            self.gallery.grid_columnconfigure(
                column,
                weight=1,
                uniform="themes"
            )

        for index, theme_name in enumerate(theme_names):

            theme_colors = self.themes[theme_name]

            self.create_theme_card(
                theme_name,
                theme_colors,
                index // 2,
                index % 2
            )

    def create_theme_card(
        self,
        name,
        colors,
        row,
        column
    ):

        active = name == self.selected_theme

        border = (
            colors["primary"]
            if active
            else colors["border"]
        )

        card = tk.Frame(
            self.gallery,
            bg=colors["card"],
            highlightbackground=border,
            highlightthickness=2 if active else 1,
            padx=13,
            pady=13,
            cursor="hand2"
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=(0, 10 if column == 0 else 0),
            pady=(0, 14)
        )

        art = tk.Canvas(
            card,
            height=112,
            bg=colors["bg"],
            highlightthickness=0,
            cursor="hand2"
        )

        art.pack(fill="x")

        art.create_oval(
            -45, -55, 115, 120,
            fill=colors["secondary"],
            outline=""
        )

        art.create_oval(
            170, -65, 330, 115,
            fill=colors["accent_light"],
            outline=""
        )

        art.create_oval(
            260, 40, 370, 155,
            fill=colors["accent"],
            outline=""
        )

        self.draw_card_flower(
            art,
            48,
            55,
            21,
            colors["flower"],
            colors["accent"]
        )

        # Color palette
        x = 155

        for color in (
            colors["primary"],
            colors["secondary"],
            colors["accent"],
            colors["bg"]
        ):

            art.create_oval(
                x - 10,
                44,
                x + 10,
                64,
                fill=color,
                outline=""
            )

            x += 32

        # Theme title
        title_row = tk.Frame(
            card,
            bg=colors["card"]
        )

        title_row.pack(
            fill="x",
            pady=(12, 4)
        )

        title = tk.Label(
            title_row,
            text=name,
            font=("Georgia", 14, "bold"),
            fg=colors["text"],
            bg=colors["card"],
            cursor="hand2"
        )

        title.pack(side="left")

        badge = tk.Label(
            title_row,
            text="✓ ACTIVE" if active else "SELECT",
            font=("Arial", 7, "bold"),
            fg="#FFFFFF" if active else colors["primary"],
            bg=colors["primary"] if active else colors["accent_light"],
            padx=8,
            pady=4,
            cursor="hand2"
        )

        badge.pack(side="right")

        description = tk.Label(
            card,
            text=THEME_INFO[name]["description"],
            font=("Arial", 8),
            fg=colors["muted"],
            bg=colors["card"],
            anchor="w",
            justify="left",
            wraplength=260,
            cursor="hand2"
        )

        description.pack(anchor="w")

        # Select the theme through main.py
        def select_theme(event=None, theme=name):

            if theme != self.app.selected_theme:
                self.app.set_theme(theme)

        for widget in (
            card,
            art,
            title_row,
            title,
            badge,
            description
        ):

            widget.bind(
                "<Button-1>",
                select_theme
            )

    def draw_card_flower(
        self,
        canvas,
        x,
        y,
        radius,
        petal,
        center
    ):

        for angle in range(0, 360, 60):

            rad = math.radians(angle)

            px = x + math.cos(rad) * radius * 0.55
            py = y + math.sin(rad) * radius * 0.55

            r = radius * 0.43

            canvas.create_oval(
                px-r,
                py-r,
                px+r,
                py+r,
                fill=petal,
                outline=""
            )

        canvas.create_oval(
            x-5,
            y-5,
            x+5,
            y+5,
            fill=center,
            outline=""
        )

    # ======================================================
    # FOOTER
    # ======================================================

    def build_footer(self):

        self.footer = tk.Frame(
            self.content,
            bg=self.colors["bg"],
            pady=18
        )

        self.footer.pack(fill="x")

        self.footer_label = tk.Label(
            self.footer,
            text="✿   A little change of scenery can make a new day.",
            font=("Georgia", 10, "italic"),
            fg=self.colors["muted"],
            bg=self.colors["bg"]
        )

        self.footer_label.pack(anchor="center")

    # ======================================================
    # CLEANUP
    # ======================================================

    def destroy(self):

        if self.resize_job:
            try:
                self.after_cancel(self.resize_job)
            except tk.TclError:
                pass

        super().destroy()

