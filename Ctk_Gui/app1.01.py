import customtkinter as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os


ct.set_appearance_mode("dark")


class HalwaStudioApp(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("980x660")
        self.minsize(860, 560)
        self.title("Halwa Studio")

        # Color system: deep charcoal + warm amber accents.
        self.colors = {
            "bg": "#111417",
            "panel": "#1a1f24",
            "panel_alt": "#202730",
            "title": "#f6e7c1",
            "muted": "#c4ced8",
            "accent": "#f5a524",
            "accent_soft": "#ffd58a",
            "counter_a": "#2a3139",
            "counter_b": "#252d36",
            "counter_c": "#2b2833",
            "counter_border": "#394555",
            "text_primary": "#f3f7fb",
            "text_dim": "#9caab8",
            "graph_bg": "#14191f",
            "graph_line": "#ffb443",
            "graph_fill": "#ffcf7d",
            "graph_grid": "#2a3340",
        }

        self.configure(fg_color=self.colors["bg"])

        # Grid: big title row, counter row, full-width graph row.
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self._build_header()
        self._build_counters()
        self._build_graph()
        self._setup_icon()
        self._start_timers()

    def _build_header(self) -> None:
        self.header = ct.CTkFrame(
            self,
            fg_color=self.colors["panel"],
            corner_radius=18,
            border_width=1,
            border_color="#2a323b",
        )
        self.header.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=14, pady=(14, 8))

        title_font = ct.CTkFont(family="Segoe UI", size=40, weight="bold")
        sub_font = ct.CTkFont(family="Segoe UI", size=15, weight="normal")

        self.title_label = ct.CTkLabel(
            self.header,
            text="HALWA STUDIO LIVE BOARD",
            font=title_font,
            text_color=self.colors["title"],
        )
        self.title_label.pack(pady=(14, 2))

        self.subtitle_label = ct.CTkLabel(
            self.header,
            text="Real-time prep counters and process rhythm graph",
            font=sub_font,
            text_color=self.colors["muted"],
        )
        self.subtitle_label.pack(pady=(0, 12))

    def _build_counters(self) -> None:
        self.counter_values = {
            "Cleaning": 0,
            "Cutting": 0,
            "Cooking": 0,
        }

        self.counter_widgets = {}
        specs = [
            ("Cleaning", "updates every 0.5 s", self.colors["counter_a"]),
            ("Cutting", "updates every 1.0 s", self.colors["counter_b"]),
            ("Cooking", "updates every 2.0 s", self.colors["counter_c"]),
        ]

        label_font = ct.CTkFont(family="Segoe UI", size=20, weight="bold")
        value_font = ct.CTkFont(family="Segoe UI", size=42, weight="bold")
        hint_font = ct.CTkFont(family="Segoe UI", size=13, weight="normal")

        for i, (name, hint, card_color) in enumerate(specs):
            card = ct.CTkFrame(
                self,
                fg_color=card_color,
                corner_radius=16,
                border_width=1,
                border_color=self.colors["counter_border"],
            )
            card.grid(row=1, column=i, sticky="nsew", padx=10, pady=8)

            lbl = ct.CTkLabel(
                card,
                text=name,
                font=label_font,
                text_color=self.colors["text_primary"],
            )
            lbl.pack(pady=(18, 8))

            val = ct.CTkLabel(
                card,
                text="0",
                font=value_font,
                text_color=self.colors["accent_soft"],
            )
            val.pack(pady=(4, 14))

            hint_lbl = ct.CTkLabel(
                card,
                text=hint,
                font=hint_font,
                text_color=self.colors["text_dim"],
            )
            hint_lbl.pack(pady=(0, 14))

            self.counter_widgets[name] = val

    def _build_graph(self) -> None:
        fig, ax = plt.subplots(figsize=(8.2, 3.8), dpi=100)
        self.ax = ax
        self.fig = fig

        self.x = np.arange(0, 2 * np.pi, 0.01)
        self.phase = 0.0
        self.y = np.sin(self.x)

        (self.wave_line,) = self.ax.plot(
            self.x,
            self.y,
            color=self.colors["graph_line"],
            linewidth=2.8,
        )
        self.wave_fill = self.ax.fill_between(
            self.x,
            self.y,
            0,
            color=self.colors["graph_fill"],
            alpha=0.22,
        )

        self.ax.set_title("Process Rhythm", fontsize=13, color="#d7e1ea", pad=10)
        self.ax.set_xlabel("Phase", fontsize=10, color="#c8d2dc")
        self.ax.set_ylabel("Intensity", fontsize=10, color="#c8d2dc")
        self.ax.set_facecolor(self.colors["graph_bg"])
        self.fig.patch.set_facecolor(self.colors["bg"])
        self.ax.grid(True, linestyle="--", linewidth=0.7, color=self.colors["graph_grid"], alpha=1.0)

        for spine in self.ax.spines.values():
            spine.set_color("#3a4757")
        self.ax.tick_params(colors="#aab7c6")

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        widget = self.canvas.get_tk_widget()
        widget.configure(bg=self.colors["bg"], highlightthickness=0)
        widget.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=14, pady=(6, 14))
        self.canvas.draw()

    def _setup_icon(self) -> None:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Halwa.ico")
        try:
            self.iconbitmap(default=icon_path)
        except Exception:
            pass

    def _start_timers(self) -> None:
        self.after(500, self._tick_cleaning)
        self.after(1000, self._tick_cutting)
        self.after(2000, self._tick_cooking)
        self.after(450, self._animate_graph)

    def _increment_counter(self, name: str) -> None:
        self.counter_values[name] += 1
        self.counter_widgets[name].configure(text=str(self.counter_values[name]))

    def _tick_cleaning(self) -> None:
        self._increment_counter("Cleaning")
        self.after(500, self._tick_cleaning)

    def _tick_cutting(self) -> None:
        self._increment_counter("Cutting")
        self.after(1000, self._tick_cutting)

    def _tick_cooking(self) -> None:
        self._increment_counter("Cooking")
        self.after(2000, self._tick_cooking)

    def _animate_graph(self) -> None:
        self.phase += 0.14
        self.y = np.sin(self.x + self.phase)
        self.wave_line.set_ydata(self.y)

        self.wave_fill.remove()
        self.wave_fill = self.ax.fill_between(
            self.x,
            self.y,
            0,
            color=self.colors["graph_fill"],
            alpha=0.22,
        )

        self.canvas.draw_idle()
        self.after(450, self._animate_graph)


if __name__ == "__main__":
    app = HalwaStudioApp()
    app.mainloop()