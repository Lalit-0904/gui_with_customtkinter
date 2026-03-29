import customtkinter as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

ct.set_appearance_mode("light")


class HalwamakerApp(ct.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x620")
        self.minsize(780, 520)
        self.title("Halwa maker")
        self.configure(fg_color="#f7f1e3")

        self.colors = {
            "surface": "#f7f1e3",
            "header_bg": "#2f4858",
            "header_text": "#fff8ed",
            "subtitle": "#d6e2e9",
            "card_a": "#ffe6b7",
            "card_b": "#ffd9a6",
            "card_c": "#ffc98e",
            "card_border": "#e3b165",
            "ink": "#2c2c2c",
            "graph_bg": "#fff8ed",
            "graph_line": "#cc6f2c",
            "graph_fill": "#f2c792",
            "grid": "#e9d8c0",
        }

        # 3-column layout: title, counters, and full-width graph.
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.title_font = ct.CTkFont(family="Palatino Linotype", size=42, weight="bold")
        self.subtitle_font = ct.CTkFont(family="Trebuchet MS", size=16, weight="normal")
        self.counter_label_font = ct.CTkFont(family="Trebuchet MS", size=21, weight="bold")
        self.counter_value_font = ct.CTkFont(family="Palatino Linotype", size=44, weight="bold")
        self.counter_hint_font = ct.CTkFont(family="Trebuchet MS", size=13, weight="normal")

        self.title_frame = ct.CTkFrame(
            self,
            fg_color=self.colors["header_bg"],
            corner_radius=18,
            border_width=2,
            border_color="#3d5f74",
        )
        self.title_frame.grid(row=0, column=0, columnspan=3, padx=12, pady=(12, 6), sticky="nsew")

        self.title_label = ct.CTkLabel(
            self.title_frame,
            text="Halwa Production Dashboard",
            font=self.title_font,
            text_color=self.colors["header_text"],
        )
        self.title_label.pack(pady=(12, 2))

        self.subtitle_label = ct.CTkLabel(
            self.title_frame,
            text="Live progress counters with animated quality curve",
            font=self.subtitle_font,
            text_color=self.colors["subtitle"],
        )
        self.subtitle_label.pack(pady=(0, 12))

        self.counter_values = {
            "Cleaning": 0,
            "Cutting": 0,
            "Cooking": 0,
        }

        self.counter_widgets = {}
        counter_specs = [
            ("Cleaning", self.colors["card_a"], "updates every 0.5s"),
            ("Cutting", self.colors["card_b"], "updates every 1.0s"),
            ("Cooking", self.colors["card_c"], "updates every 2.0s"),
        ]

        for idx, (name, card_color, hint_text) in enumerate(counter_specs):
            frame = ct.CTkFrame(
                self,
                fg_color=card_color,
                corner_radius=18,
                border_width=2,
                border_color=self.colors["card_border"],
            )
            frame.grid(row=1, column=idx, padx=10, pady=8, sticky="nsew")

            label = ct.CTkLabel(
                frame,
                text=name,
                font=self.counter_label_font,
                text_color=self.colors["ink"],
            )
            label.pack(pady=(16, 8))

            value_label = ct.CTkLabel(
                frame,
                text="0",
                font=self.counter_value_font,
                text_color="#1f2a30",
            )
            value_label.pack(pady=(8, 20))

            hint_label = ct.CTkLabel(
                frame,
                text=hint_text,
                font=self.counter_hint_font,
                text_color="#5e4a36",
            )
            hint_label.pack(pady=(0, 14))

            self.counter_widgets[name] = value_label

        fig, ax = plt.subplots(figsize=(8, 3.8), dpi=100)
        self.ax = ax
        self.time_values = np.arange(0, 2 * np.pi, 0.01)
        self.phase_shift = 0.0
        self.sine_values = np.sin(self.time_values)
        (self.sine_line,) = self.ax.plot(
            self.time_values,
            self.sine_values,
            color=self.colors["graph_line"],
            linewidth=2.6,
        )
        self.sine_fill = self.ax.fill_between(
            self.time_values,
            self.sine_values,
            0,
            color=self.colors["graph_fill"],
            alpha=0.35,
        )
        self.ax.set_title("Texture Rhythm Curve", fontsize=13, color="#5c4022", pad=10)
        self.ax.set_xlabel("Process Phase", fontsize=10, color="#5c4022")
        self.ax.set_ylabel("Intensity", fontsize=10, color="#5c4022")
        self.ax.set_facecolor(self.colors["graph_bg"])
        fig.patch.set_facecolor(self.colors["surface"])
        self.ax.grid(True, linestyle="--", linewidth=0.7, color=self.colors["grid"], alpha=0.9)
        for spine in self.ax.spines.values():
            spine.set_color("#bf9b6a")
        self.ax.tick_params(colors="#7a5b39")

        self.canvas = FigureCanvasTkAgg(fig, self)
        graph_widget = self.canvas.get_tk_widget()
        graph_widget.configure(bg=self.colors["surface"], highlightthickness=0)
        graph_widget.grid(row=2, column=0, columnspan=3, padx=12, pady=(4, 12), sticky="nsew")
        self.canvas.draw()

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Halwa.ico")
        try:
            self.iconbitmap(default=icon_path)
        except Exception:
            pass

        self.after(500, self._animate_graph)
        self.after(500, self._tick_cleaning)
        self.after(1000, self._tick_cutting)
        self.after(2000, self._tick_cooking)
        self.after(100, self.lift)

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
        self.phase_shift += 0.15
        self.sine_values = np.sin(self.time_values + self.phase_shift)
        self.sine_line.set_ydata(self.sine_values)
        self.sine_fill.remove()
        self.sine_fill = self.ax.fill_between(
            self.time_values,
            self.sine_values,
            0,
            color=self.colors["graph_fill"],
            alpha=0.35,
        )
        self.canvas.draw_idle()
        self.after(500, self._animate_graph)



Hm=HalwamakerApp()
Hm.mainloop()