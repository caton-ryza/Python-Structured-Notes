
import tkinter as tk


# ==========================================================
# ORIRI — SCROLLABLE FRAME
# Botanical Glass Edition
# ==========================================================

DEFAULT_COLORS = {
    "bg": "#EAF1E8",
    "card": "#F8FAF5",
    "primary": "#47775D",
    "secondary": "#A9C7B1",
    "muted": "#789381",
    "border": "#C9DCC9"
}


class ScrollableFrame(tk.Frame):

    def __init__(
        self,
        parent,
        colors=None,
        background=None,
        **kwargs
    ):
        self.colors = colors or DEFAULT_COLORS

        self.background = (
            background or self.colors["bg"]
        )

        super().__init__(
            parent,
            bg=self.background,
            bd=0,
            highlightthickness=0,
            **kwargs
        )

        self.build_scroll_area()
        self.bind_scroll_events()

    # ------------------------------------------------------
    # BUILD SCROLL AREA
    # ------------------------------------------------------

    def build_scroll_area(self):

        self.canvas = tk.Canvas(
            self,
            bg=self.background,
            bd=0,
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            bg=self.colors["secondary"],
            troughcolor=self.background,
            activebackground=self.colors["primary"],
            relief="flat",
            width=9,
            bd=0,
            highlightthickness=0
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 3),
            pady=8
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Content frame
        self.content = tk.Frame(
            self.canvas,
            bg=self.background,
            bd=0,
            highlightthickness=0
        )

        self.content_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_content_width
        )

    # ------------------------------------------------------
    # UPDATE SCROLL REGION
    # ------------------------------------------------------

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ------------------------------------------------------
    # UPDATE CONTENT WIDTH
    # ------------------------------------------------------

    def update_content_width(self, event):

        self.canvas.itemconfigure(
            self.content_window,
            width=event.width
        )

    # ------------------------------------------------------
    # MOUSE WHEEL
    # ------------------------------------------------------

    def bind_scroll_events(self):

        self.canvas.bind(
            "<Enter>",
            self.activate_mousewheel
        )

        self.canvas.bind(
            "<Leave>",
            self.deactivate_mousewheel
        )

        self.content.bind(
            "<Enter>",
            self.activate_mousewheel
        )

        self.content.bind(
            "<Leave>",
            self.deactivate_mousewheel
        )

    def activate_mousewheel(self, event=None):

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.canvas.bind_all(
            "<Button-4>",
            self.on_mousewheel_linux
        )

        self.canvas.bind_all(
            "<Button-5>",
            self.on_mousewheel_linux
        )

    def deactivate_mousewheel(self, event=None):

        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def on_mousewheel(self, event):

        if event.delta:
            self.canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )

    def on_mousewheel_linux(self, event):

        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")

        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    # ------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------

    def get_frame(self):
        return self.content

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)

    def scroll_to_bottom(self):
        self.canvas.yview_moveto(1)

    def destroy(self):

        self.deactivate_mousewheel()

        super().destroy()
