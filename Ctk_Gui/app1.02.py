import customtkinter as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os


ct.set_appearance_mode("light")


class HalwaFestiveApp(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("980x670")
        self.minsize(860, 560)
        self.title("Halwa Festive Dashboard")

        # Festive saffron palette with high readability contrast.
        self.colors = {
            "bg": "#fff5e6",
            "header_grad_top": "#ffb347",
            "header_grad_bottom": "#ff8f3f",
            "header_text": "#2c1a0e",
            "sub_text": "#5a3922",
            "card_1": "#fff0d6",
            "card_2": "#ffe8c2",
            "card_3": "#ffe0ad",
            "card_border": "#f2b266",
            "card_title": "#6e3f16",
            "card_value": "#2f2f2f",
            "card_hint": "#875734",
            "graph_bg": "#fffaf2",
            "graph_line": "#d66a00",
            "graph_fill": "#ffcc8a",
            "grid": "#f0d3ae",
            "spine": "#d8a56d",
            "tick": "#7f5736",
        }

        self.configure(fg_color=self.colors["bg"])

        # Layout
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
        title_font = ct.CTkFont(family="Georgia", size=40, weight="bold")
        sub_font = ct.CTkFont(family="Verdana", size=14, weight="normal")

        self.header = ct.CTkFrame(
            self,
            fg_color=self.colors["header_grad_top"],
            corner_radius=20,
            border_width=2,
            border_color="#f38b2a",
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=14, pady=(14, 8), sticky="nsew")

        self.title = ct.CTkLabel(
            self.header,
            text="HALWA FESTIVE LIVE",
            font=title_font,
            text_color=self.colors["header_text"],
        )
        self.title.pack(pady=(14, 2))

        self.subtitle = ct.CTkLabel(
            self.header,
            text="Counters pulse at different intervals + full width animated graph",
            font=sub_font,
            text_color=self.colors["sub_text"],
        )
        self.subtitle.pack(pady=(0, 12))

    def _build_counters(self) -> None:
        self.counter_values = {
            "Cleaning": 0,
            "Cutting": 0,
            "Cooking": 0,
        }
        self.counter_widgets = {}

        specs = [
            ("Cleaning", "updates every 0.5s", self.colors["card_1"]),
            ("Cutting", "updates every 1.0s", self.colors["card_2"]),
            ("Cooking", "updates every 2.0s", self.colors["card_3"]),
        ]

        name_font = ct.CTkFont(family="Verdana", size=20, weight="bold")
        value_font = ct.CTkFont(family="Georgia", size=44, weight="bold")
        hint_font = ct.CTkFont(family="Verdana", size=12, weight="normal")

        for idx, (name, hint, bg_color) in enumerate(specs):
            card = ct.CTkFrame(
                self,
                fg_color=bg_color,
                corner_radius=18,
                border_width=2,
                border_color=self.colors["card_border"],
            )
            card.grid(row=1, column=idx, padx=10, pady=8, sticky="nsew")

            title = ct.CTkLabel(
                card,
                text=name,
                font=name_font,
                text_color=self.colors["card_title"],
            )
            title.pack(pady=(18, 8))

            value = ct.CTkLabel(
                card,
                text="0",
                font=value_font,
                text_color=self.colors["card_value"],
            )
            value.pack(pady=(2, 14))

            hint_label = ct.CTkLabel(
                card,
                text=hint,
                font=hint_font,
                text_color=self.colors["card_hint"],
            )
            hint_label.pack(pady=(0, 14))

            self.counter_widgets[name] = value

    def _build_graph(self) -> None:
        self.fig, self.ax = plt.subplots(figsize=(8.4, 3.9), dpi=100)

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
            alpha=0.30,
        )

        self.ax.set_title("Texture Rhythm Curve", fontsize=13, color="#724622", pad=10)
        self.ax.set_xlabel("Phase", fontsize=10, color="#724622")
        self.ax.set_ylabel("Intensity", fontsize=10, color="#724622")

        self.ax.set_facecolor(self.colors["graph_bg"])
        self.fig.patch.set_facecolor(self.colors["bg"])
        self.ax.grid(True, linestyle="--", linewidth=0.7, color=self.colors["grid"], alpha=1.0)

        for spine in self.ax.spines.values():
            spine.set_color(self.colors["spine"])
        self.ax.tick_params(colors=self.colors["tick"])

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        graph_widget = self.canvas.get_tk_widget()
        graph_widget.configure(bg=self.colors["bg"], highlightthickness=0)
        graph_widget.grid(row=2, column=0, columnspan=3, padx=14, pady=(6, 14), sticky="nsew")
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
            alpha=0.30,
        )

        self.canvas.draw_idle()
        self.after(450, self._animate_graph)


if __name__ == "__main__":
    app = HalwaFestiveApp()
    app.mainloop()