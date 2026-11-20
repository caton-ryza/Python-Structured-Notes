
import tkinter as tk
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageTk

from modules.clock import (
    get_current_time,
    get_current_date,
    get_greeting
)

# ==========================================================
# ORIRI — GLOBAL BOTANICAL GLASS DASHBOARD
# ==========================================================

DISPLAY_FONT = "Georgia"
BODY_FONT = "Arial"
CLOCK_FONT = "Consolas"


class Dashboard(tk.Frame):

    def __init__(self, parent, app=None):

        self.app = app
        self.colors = app.theme

        super().__init__(
            parent,
            bg=self.colors["bg"]
        )

        self.photos = []
        self.clock_job = None
        self.resize_job = None

        self.clock_item = None
        self.date_item = None
        self.greeting_item = None

        self.alarms = self.load_alarms()

        self.canvas = tk.Canvas(
            self,
            bg=self.colors["bg"],
            highlightthickness=0,
            bd=0,
            height=820
        )

        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        self.after(150, self.render)
        self.schedule_clock()

    # ======================================================
    # THEME UTILITIES
    # ======================================================

    def color(self, key):
        return self.colors[key]

    def rgb(self, color):

        color = color.lstrip("#")

        return tuple(
            int(color[i:i + 2], 16)
            for i in (0, 2, 4)
        )

    def text(self, x, y, value, size=11,
             color=None, font=BODY_FONT,
             weight="normal", anchor="nw"):

        return self.canvas.create_text(
            x,
            y,
            text=value,
            fill=color or self.colors["text"],
            font=(font, size, weight),
            anchor=anchor
        )

    def line(self, x1, y1, x2, y2, color=None, width=1):

        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color or self.colors["border"],
            width=width
        )

    def pill(self, x, y, label, width=100):

        c = self.colors

        self.canvas.create_oval(
            x, y,
            x + width, y + 28,
            fill=c["accent_light"],
            outline=c["border"],
            width=1
        )

        self.text(
            x + width / 2,
            y + 14,
            label,
            8,
            c["primary"],
            BODY_FONT,
            "bold",
            "center"
        )

    # ======================================================
    # ALARM DATA
    # ======================================================

    def load_alarms(self):

        try:

            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

            path = os.path.join(
                base_dir,
                "data",
                "alarms.json"
            )

            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_alarm_name(self, alarm):

        return alarm.get(
            "label",
            alarm.get("name", "Morning alarm")
        )

    def get_next_alarm(self):

        now = datetime.now()
        candidates = []

        for alarm in self.alarms:

            if not alarm.get("enabled", True):
                continue

            try:

                hour, minute = map(
                    int,
                    alarm["time"].split(":")
                )

                alarm_time = now.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0
                )

                repeat = alarm.get("repeat", [])

                if repeat:

                    days = [
                        str(day).lower()
                        for day in repeat
                    ]

                    if now.strftime("%A").lower() not in days:
                        continue

                if alarm_time > now:
                    candidates.append((alarm_time, alarm))

            except (KeyError, ValueError, TypeError):
                continue

        if not candidates:
            return None

        candidates.sort(key=lambda item: item[0])

        return candidates[0][1]

    # ======================================================
    # BOTANICAL BACKGROUND
    # ======================================================

    def create_background(self, width, height):

        c = self.colors

        top = self.rgb(c["bg"])
        bottom = self.rgb(c["secondary"])

        image = Image.new(
            "RGB",
            (width, height)
        )

        pixels = image.load()

        for y in range(height):

            ratio = y / max(height - 1, 1)

            current = tuple(
                int(
                    top[i] * (1 - ratio)
                    + bottom[i] * ratio * 0.48
                )
                for i in range(3)
            )

            for x in range(width):
                pixels[x, y] = current

        image = image.convert("RGBA")

        # Soft sunlight
        light = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(light)

        draw.ellipse(
            (
                width * 0.40,
                -height * 0.55,
                width * 1.10,
                height * 0.48
            ),
            fill=(255, 255, 255, 65)
        )

        light = light.filter(
            ImageFilter.GaussianBlur(100)
        )

        image = Image.alpha_composite(image, light)

        # Blurred botanical shapes
        foliage = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        draw = ImageDraw.Draw(foliage)

        primary = self.rgb(c["primary"])
        accent = self.rgb(c["accent"])

        draw.ellipse(
            (
                -width * 0.25,
                height * 0.18,
                width * 0.32,
                height * 0.95
            ),
            fill=(*primary, 48)
        )

        draw.ellipse(
            (
                width * 0.77,
                height * 0.15,
                width * 1.25,
                height * 0.90
            ),
            fill=(*accent, 50)
        )

        draw.ellipse(
            (
                width * 0.20,
                height * 0.75,
                width * 0.75,
                height * 1.25
            ),
            fill=(*primary, 35)
        )

        foliage = foliage.filter(
            ImageFilter.GaussianBlur(65)
        )

        image = Image.alpha_composite(image, foliage)

        # Decorative leaf silhouettes
        leaves = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 0)
        )

        for i in range(12):

            x = int(width * (0.80 + (i % 3) * 0.055))
            y = int(height * (0.12 + i * 0.065))

            angle = -30 + i * 7

            leaf = Image.new(
                "RGBA",
                (150, 65),
                (0, 0, 0, 0)
            )

            leaf_draw = ImageDraw.Draw(leaf)

            leaf_draw.ellipse(
                (5, 8, 145, 57),
                fill=(*primary, 65)
            )

            leaf = leaf.rotate(
                angle,
                resample=Image.Resampling.BICUBIC
            )

            leaves.alpha_composite(
                leaf,
                (x - 75, y - 32)
            )

        leaves = leaves.filter(
            ImageFilter.GaussianBlur(13)
        )

        image = Image.alpha_composite(image, leaves)

        return image.convert("RGB")

    # ======================================================
    # FROSTED GLASS PANEL ENGINE
    # ======================================================

    def create_glass(
        self,
        background,
        x,
        y,
        width,
        height,
        radius=25,
        tint=None,
        opacity=112
    ):

        c = self.colors

        tint = tint or self.rgb(c["card"])

        panel = background.crop(
            (x, y, x + width, y + height)
        ).filter(
            ImageFilter.GaussianBlur(19)
        ).convert("RGBA")

        tint_layer = Image.new(
            "RGBA",
            (width, height),
            (*tint, opacity)
        )

        panel = Image.alpha_composite(
            panel,
            tint_layer
        )

        # Soft top reflection
        reflection = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        reflection_pixels = reflection.load()

        for py in range(min(height, 105)):

            alpha = int(
                42 * (1 - py / 105)
            )

            for px in range(width):

                reflection_pixels[px, py] = (
                    255, 255, 255, alpha
                )

        panel = Image.alpha_composite(
            panel,
            reflection
        )

        # Rounded mask
        mask = Image.new(
            "L",
            (width, height),
            0
        )

        mask_draw = ImageDraw.Draw(mask)

        mask_draw.rounded_rectangle(
            (0, 0, width - 1, height - 1),
            radius=radius,
            fill=255
        )

        # Glass edge
        edge = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        edge_draw = ImageDraw.Draw(edge)

        edge_draw.rounded_rectangle(
            (1, 1, width - 2, height - 2),
            radius=radius,
            outline=(255, 255, 255, 195),
            width=2
        )

        edge_draw.line(
            (radius, 2, width - radius, 2),
            fill=(255, 255, 255, 170),
            width=2
        )

        edge_draw.line(
            (3, radius, 3, height - radius),
            fill=(255, 255, 255, 80),
            width=1
        )

        panel = Image.alpha_composite(
            panel,
            edge
        )

        clipped = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        clipped.paste(
            panel,
            (0, 0),
            mask
        )

        # Soft shadow
        shadow = Image.new(
            "RGBA",
            (width + 32, height + 32),
            (0, 0, 0, 0)
        )

        shadow_draw = ImageDraw.Draw(shadow)

        shadow_draw.rounded_rectangle(
            (14, 15, width + 17, height + 17),
            radius=radius + 3,
            fill=(35, 45, 40, 32)
        )

        shadow = shadow.filter(
            ImageFilter.GaussianBlur(13)
        )

        result = Image.new(
            "RGBA",
            (width + 32, height + 32),
            (0, 0, 0, 0)
        )

        result = Image.alpha_composite(
            result,
            shadow
        )

        result.alpha_composite(
            clipped,
            (16, 12)
        )

        return result

    def draw_glass(
        self,
        background,
        x,
        y,
        width,
        height,
        radius=25,
        tint=None,
        opacity=112
    ):

        width = max(1, int(width))
        height = max(1, int(height))

        glass = self.create_glass(
            background,
            int(x),
            int(y),
            width,
            height,
            radius,
            tint,
            opacity
        )

        photo = ImageTk.PhotoImage(glass)

        self.photos.append(photo)

        self.canvas.create_image(
            x - 16,
            y - 12,
            image=photo,
            anchor="nw"
        )

    # ======================================================
    # DASHBOARD RENDERING
    # ======================================================

    def render(self):

        if not self.winfo_exists():
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 650 or height < 500:
            return

        c = self.colors

        self.canvas.delete("all")
        self.photos.clear()

        background = self.create_background(
            width,
            height
        )

        self.background_photo = ImageTk.PhotoImage(
            background
        )

        self.canvas.create_image(
            0,
            0,
            image=self.background_photo,
            anchor="nw"
        )

        margin = 42
        content_width = width - margin * 2

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        self.text(
            margin,
            29,
            "O R I R I",
            11,
            c["primary"],
            BODY_FONT,
            "bold"
        )

        self.text(
            margin,
            52,
            "A quieter start to every day.",
            9,
            c["muted"]
        )

        self.greeting_item = self.text(
            margin,
            103,
            get_greeting() + ".",
            26,
            c["text"],
            DISPLAY_FONT,
            "bold"
        )

        self.date_item = self.text(
            margin,
            143,
            get_current_date(),
            10,
            c["muted"]
        )

        self.pill(
            width - margin - 142,
            48,
            "BOTANICAL EDITION",
            142
        )

        # --------------------------------------------------
        # HERO ROW
        # --------------------------------------------------

        hero_y = 185
        hero_height = 235
        gap = 20

        clock_width = int(content_width * 0.62)
        alarm_width = content_width - clock_width - gap

        alarm_x = margin + clock_width + gap

        self.draw_glass(
            background,
            margin,
            hero_y,
            clock_width,
            hero_height,
            radius=30,
            tint=self.rgb(c["card"]),
            opacity=125
        )

        self.draw_glass(
            background,
            alarm_x,
            hero_y,
            alarm_width,
            hero_height,
            radius=30,
            tint=self.rgb(c["panel"]),
            opacity=135
        )

        # Clock panel
        self.text(
            margin + 28,
            hero_y + 26,
            "YOUR MOMENT OF CALM",
            9,
            c["muted"],
            BODY_FONT,
            "bold"
        )

        self.text(
            margin + 28,
            hero_y + 58,
            "Make room for a new day.",
            16,
            c["text"],
            DISPLAY_FONT
        )

        self.clock_item = self.text(
            margin + 26,
            hero_y + 105,
            get_current_time(),
            48,
            c["primary"],
            CLOCK_FONT
        )

        self.text(
            margin + 30,
            hero_y + 179,
            "Breathe in. Begin again.",
            10,
            c["muted"]
        )

        # Clock decoration
        orbit_x = margin + clock_width - 75
        orbit_y = hero_y + 120

        self.canvas.create_oval(
            orbit_x - 34,
            orbit_y - 34,
            orbit_x + 34,
            orbit_y + 34,
            outline="#FFFFFF",
            width=2
        )

        self.canvas.create_oval(
            orbit_x - 25,
            orbit_y - 25,
            orbit_x + 25,
            orbit_y + 25,
            outline=c["secondary"],
            width=1
        )

        self.canvas.create_oval(
            orbit_x - 4,
            orbit_y - 4,
            orbit_x + 4,
            orbit_y + 4,
            fill=c["primary"],
            outline=""
        )

        # Next alarm panel
        self.text(
            alarm_x + 25,
            hero_y + 27,
            "NEXT ALARM",
            9,
            c["muted"],
            BODY_FONT,
            "bold"
        )

        alarm = self.get_next_alarm()

        if alarm:

            self.text(
                alarm_x + 25,
                hero_y + 76,
                alarm.get("time", "--:--"),
                34,
                c["primary"],
                CLOCK_FONT
            )

            self.text(
                alarm_x + 27,
                hero_y + 130,
                self.get_alarm_name(alarm),
                12,
                c["text"],
                BODY_FONT,
                "bold"
            )

            self.text(
                alarm_x + 27,
                hero_y + 163,
                "Your next moment to rise.",
                9,
                c["muted"]
            )

        else:

            self.text(
                alarm_x + 25,
                hero_y + 81,
                "No alarms",
                22,
                c["text"],
                DISPLAY_FONT
            )

            self.text(
                alarm_x + 27,
                hero_y + 127,
                "Nothing scheduled yet.",
                10,
                c["muted"]
            )

            self.text(
                alarm_x + 27,
                hero_y + 153,
                "Your mornings are open.",
                9,
                c["muted"]
            )

        # --------------------------------------------------
        # LOWER GRID
        # --------------------------------------------------

        lower_y = 450
        lower_height = height - lower_y - 38

        left_width = int(content_width * 0.58)
        right_width = content_width - left_width - gap

        right_x = margin + left_width + gap

        self.draw_glass(
            background,
            margin,
            lower_y,
            left_width,
            lower_height,
            radius=27,
            tint=self.rgb(c["card"]),
            opacity=135
        )

        self.draw_glass(
            background,
            right_x,
            lower_y,
            right_width,
            lower_height,
            radius=27,
            tint=self.rgb(c["panel"]),
            opacity=135
        )

        # --------------------------------------------------
        # UPCOMING ALARMS
        # --------------------------------------------------

        self.text(
            margin + 25,
            lower_y + 24,
            "Upcoming alarms",
            17,
            c["text"],
            DISPLAY_FONT,
            "bold"
        )

        self.text(
            margin + 27,
            lower_y + 54,
            "Your schedule, at a glance.",
            9,
            c["muted"]
        )

        self.line(
            margin + 25,
            lower_y + 83,
            margin + left_width - 25,
            lower_y + 83,
            c["border"],
            2
        )

        enabled = [
            alarm for alarm in self.alarms
            if alarm.get("enabled", True)
        ]

        if enabled:

            y = lower_y + 105

            for alarm in enabled[:4]:

                self.canvas.create_oval(
                    margin + 28,
                    y + 5,
                    margin + 36,
                    y + 13,
                    fill=c["accent"],
                    outline=""
                )

                self.text(
                    margin + 49,
                    y,
                    alarm.get("time", "--:--"),
                    12,
                    c["primary"],
                    CLOCK_FONT,
                    "bold"
                )

                self.text(
                    margin + 135,
                    y + 1,
                    self.get_alarm_name(alarm),
                    10,
                    c["muted"]
                )

                y += 43

                if y < lower_y + lower_height - 30:

                    self.line(
                        margin + 26,
                        y - 8,
                        margin + left_width - 25,
                        y - 8,
                        c["border"]
                    )

        else:

            self.text(
                margin + 27,
                lower_y + 117,
                "A fresh page awaits.",
                16,
                c["primary"],
                DISPLAY_FONT
            )

            self.text(
                margin + 28,
                lower_y + 150,
                "Your saved alarms will appear here.",
                9,
                c["muted"]
            )

        # --------------------------------------------------
        # DAILY REMINDER
        # --------------------------------------------------

        self.text(
            right_x + 24,
            lower_y + 24,
            "A LITTLE REMINDER",
            9,
            c["muted"],
            BODY_FONT,
            "bold"
        )

        self.text(
            right_x + 24,
            lower_y + 70,
            "There is no need",
            18,
            c["text"],
            DISPLAY_FONT
        )

        self.text(
            right_x + 24,
            lower_y + 96,
            "to rush the day.",
            18,
            c["text"],
            DISPLAY_FONT
        )

        self.line(
            right_x + 26,
            lower_y + 139,
            right_x + 76,
            lower_y + 139,
            c["accent"],
            2
        )

        self.text(
            right_x + 24,
            lower_y + 157,
            "Begin gently. Grow from there.",
            9,
            c["muted"]
        )

        # Decorative leaf
        leaf_x = right_x + right_width - 55
        leaf_y = lower_y + lower_height - 55

        self.canvas.create_oval(
            leaf_x - 17,
            leaf_y - 30,
            leaf_x + 17,
            leaf_y + 30,
            fill=c["accent_light"],
            outline=c["border"],
            width=1
        )

        self.canvas.create_line(
            leaf_x,
            leaf_y - 22,
            leaf_x,
            leaf_y + 22,
            fill=c["primary"],
            width=1
        )

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        self.text(
            width - margin,
            height - 13,
            "ORIRI  •  MADE FOR SLOWER MORNINGS",
            8,
            c["muted"],
            BODY_FONT,
            "bold",
            "se"
        )

    # ======================================================
    # CLOCK UPDATES
    # ======================================================

    def schedule_clock(self):
        self.update_clock()

    def update_clock(self):

        try:

            if self.clock_item is not None:

                self.canvas.itemconfig(
                    self.clock_item,
                    text=get_current_time()
                )

            if self.date_item is not None:

                self.canvas.itemconfig(
                    self.date_item,
                    text=get_current_date()
                )

            if self.greeting_item is not None:

                self.canvas.itemconfig(
                    self.greeting_item,
                    text=get_greeting() + "."
                )

            self.clock_job = self.after(
                1000,
                self.update_clock
            )

        except tk.TclError:
            self.clock_job = None

    # ======================================================
    # RESPONSIVE RESIZING
    # ======================================================

    def on_resize(self, event):

        if self.resize_job:

            try:
                self.after_cancel(self.resize_job)
            except tk.TclError:
                pass

        self.resize_job = self.after(
            200,
            self.render
        )

    # ======================================================
    # CLEANUP
    # ======================================================

    def destroy(self):

        for job in (self.clock_job, self.resize_job):

            if job:

                try:
                    self.after_cancel(job)
                except tk.TclError:
                    pass

        super().destroy()
