import customtkinter as ct
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

try:
    import pywinstyles
except Exception:
    pywinstyles = None


ct.set_appearance_mode("dark")
ct.set_default_color_theme("blue")


class GlassLabDashboard(ct.CTk):
    def __init__(self):
        super().__init__()
        self.title("Glass Lab Dashboard")
        self.geometry("1060x720")
        self.minsize(920, 620)

        self.palette = {
            "app_bg": "#0b1220",
            "plate_1": "#182846",
            "plate_2": "#111d36",
            "glass": "#dce9ff",
            "glass_mid": "#bfd8ff",
            "glass_soft": "#a7c9ff",
            "ink": "#081227",
            "ink_sub": "#29406f",
            "accent": "#5bd6ff",
            "accent_2": "#8d72ff",
            "card_bg_a": "#d8e9ff",
            "card_bg_b": "#d2e1ff",
            "card_bg_c": "#c8dcff",
            "graph_bg": "#f2f8ff",
            "graph_line": "#3f8cff",
            "graph_fill": "#8bc3ff",
            "graph_grid": "#cfe3ff",
            "graph_spine": "#9dbfe6",
            "graph_tick": "#476b94",
        }

        self.configure(fg_color=self.palette["app_bg"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self._build_background_layers()
        self._build_header_glass()
        self._build_counter_cards()
        self._build_graph_glass()
        self._load_icon()
        self._apply_native_glass()

        self.counter_data = {"Cleaning": 0, "Cutting": 0, "Cooking": 0}
        self._start_timers()

    def _apply_native_glass(self) -> None:
        if os.name != "nt" or pywinstyles is None:
            return

        try:
            self.update_idletasks()
            # "transparent" gives the strongest compositor effect on supported systems.
            pywinstyles.apply_style(self, "transparent")
            pywinstyles.set_opacity(self.winfo_id(), value=0.96)
        except Exception:
            try:
                pywinstyles.apply_style(self, "acrylic")
            except Exception:
                try:
                    pywinstyles.apply_style(self, "mica")
                except Exception:
                    pass

    def _build_background_layers(self) -> None:
        self.bg_plate_top = ct.CTkFrame(
            self,
            fg_color=self.palette["plate_1"],
            corner_radius=34,
            border_width=0,
        )
        self.bg_plate_top.grid(row=0, column=0, columnspan=3, padx=24, pady=(22, 10), sticky="nsew")

        self.bg_plate_mid = ct.CTkFrame(
            self,
            fg_color=self.palette["plate_2"],
            corner_radius=30,
            border_width=0,
        )
        self.bg_plate_mid.grid(row=1, column=0, columnspan=3, padx=28, pady=(16, 10), sticky="nsew")

    def _build_header_glass(self) -> None:
        title_font = ct.CTkFont(family="Segoe UI", size=40, weight="bold")
        subtitle_font = ct.CTkFont(family="Trebuchet MS", size=14, weight="normal")

        self.header = ct.CTkFrame(
            self,
            fg_color=self.palette["glass"],
            corner_radius=24,
            border_width=2,
            border_color="#f5fbff",
        )
        self.header.grid(row=0, column=0, columnspan=3, padx=18, pady=(14, 8), sticky="nsew")

        self.header_tag = ct.CTkLabel(
            self.header,
            text="GLASSMORPHISM UI",
            font=ct.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.palette["accent_2"],
        )
        self.header_tag.pack(pady=(10, 0))

        self.title_label = ct.CTkLabel(
            self.header,
            text="HALWA WORKFLOW MONITOR",
            font=title_font,
            text_color=self.palette["ink"],
        )
        self.title_label.pack(pady=(4, 2))

        self.subtitle_label = ct.CTkLabel(
            self.header,
            text="Three asynchronous counters + full-width live rhythm graph",
            font=subtitle_font,
            text_color=self.palette["ink_sub"],
        )
        self.subtitle_label.pack(pady=(0, 12))

    def _build_counter_cards(self) -> None:
        label_font = ct.CTkFont(family="Trebuchet MS", size=20, weight="bold")
        value_font = ct.CTkFont(family="Segoe UI", size=44, weight="bold")
        sub_font = ct.CTkFont(family="Trebuchet MS", size=12, weight="normal")

        specs = [
            ("Cleaning", "interval: 0.50s", self.palette["card_bg_a"], self.palette["accent"]),
            ("Cutting", "interval: 1.00s", self.palette["card_bg_b"], "#53b6ff"),
            ("Cooking", "interval: 2.00s", self.palette["card_bg_c"], "#6d9fff"),
        ]

        self.counter_labels = {}

        for idx, (name, interval_text, bg_color, meter_color) in enumerate(specs):
            card = ct.CTkFrame(
                self,
                fg_color=bg_color,
                corner_radius=20,
                border_width=2,
                border_color="#f3f9ff",
            )
            card.grid(row=1, column=idx, padx=12, pady=10, sticky="nsew")

            card.grid_rowconfigure((0, 1, 2, 3), weight=1)
            card.grid_columnconfigure(0, weight=1)

            ct.CTkLabel(
                card,
                text=name,
                font=label_font,
                text_color=self.palette["ink"],
            ).grid(row=0, column=0, pady=(14, 4), padx=10, sticky="n")

            value_label = ct.CTkLabel(
                card,
                text="0",
                font=value_font,
                text_color=self.palette["ink"],
            )
            value_label.grid(row=1, column=0, pady=(0, 6), padx=10, sticky="n")

            meter = ct.CTkProgressBar(
                card,
                progress_color=meter_color,
                fg_color="#bdd6fb",
                height=9,
                corner_radius=100,
            )
            meter.set(1)
            meter.grid(row=2, column=0, padx=22, pady=(2, 8), sticky="ew")

            ct.CTkLabel(
                card,
                text=interval_text,
                font=sub_font,
                text_color=self.palette["ink_sub"],
            ).grid(row=3, column=0, pady=(0, 12), padx=10, sticky="n")

            self.counter_labels[name] = value_label

    def _build_graph_glass(self) -> None:
        self.graph_shell = ct.CTkFrame(
            self,
            fg_color=self.palette["glass_mid"],
            corner_radius=22,
            border_width=2,
            border_color="#eff7ff",
        )
        self.graph_shell.grid(row=2, column=0, columnspan=3, padx=16, pady=(6, 16), sticky="nsew")
        self.graph_shell.grid_rowconfigure(0, weight=1)
        self.graph_shell.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(8.9, 3.9), dpi=100)
        self.x = np.arange(0, 2 * np.pi, 0.01)
        self.phase = 0.0
        self.y = np.sin(self.x)

        (self.wave_line,) = self.ax.plot(
            self.x,
            self.y,
            color=self.palette["graph_line"],
            linewidth=2.8,
        )
        self.wave_fill = self.ax.fill_between(
            self.x,
            self.y,
            0,
            color=self.palette["graph_fill"],
            alpha=0.32,
        )

        self.ax.set_title("Live Process Rhythm", fontsize=13, color="#385c86", pad=10)
        self.ax.set_xlabel("Phase", fontsize=10, color="#385c86")
        self.ax.set_ylabel("Intensity", fontsize=10, color="#385c86")
        self.ax.set_facecolor(self.palette["graph_bg"])
        self.fig.patch.set_facecolor(self.palette["glass_mid"])
        self.ax.grid(True, linestyle="--", linewidth=0.7, color=self.palette["graph_grid"], alpha=1.0)

        for spine in self.ax.spines.values():
            spine.set_color(self.palette["graph_spine"])
        self.ax.tick_params(colors=self.palette["graph_tick"])

        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_shell)
        graph_widget = self.canvas.get_tk_widget()
        graph_widget.configure(bg=self.palette["glass_mid"], highlightthickness=0)
        graph_widget.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        self.canvas.draw()

    def _load_icon(self) -> None:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Halwa.ico")
        try:
            self.iconbitmap(default=icon_path)
        except Exception:
            pass

    def _start_timers(self) -> None:
        self.after(500, self._tick_cleaning)
        self.after(1000, self._tick_cutting)
        self.after(2000, self._tick_cooking)
        self.after(420, self._animate_graph)
        self.after(100, self.lift)

    def _increment(self, key: str) -> None:
        self.counter_data[key] += 1
        self.counter_labels[key].configure(text=str(self.counter_data[key]))

    def _tick_cleaning(self) -> None:
        self._increment("Cleaning")
        self.after(500, self._tick_cleaning)

    def _tick_cutting(self) -> None:
        self._increment("Cutting")
        self.after(1000, self._tick_cutting)

    def _tick_cooking(self) -> None:
        self._increment("Cooking")
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
            color=self.palette["graph_fill"],
            alpha=0.32,
        )

        self.canvas.draw_idle()
        self.after(420, self._animate_graph)


if __name__ == "__main__":
    app = GlassLabDashboard()
    app.mainloop()
