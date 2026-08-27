import json
import os
import threading
import time
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import win32gui
import win32process
import psutil


class TimeTrackerApp:
    # Keywords to detect websites inside browsers
    SITE_KEYWORDS = {
        "youtube": "YouTube",
        "netflix": "Netflix",
        "twitch": "Twitch",
        "spotify": "Spotify",
        "github": "GitHub",
        "stackoverflow": "Stack Overflow",
        "gmail": "Gmail",
        "outlook": "Outlook",
        "chatgpt": "ChatGPT",
        "reddit": "Reddit",
        "twitter": "Twitter",
        "instagram": "Instagram",
        "linkedin": "LinkedIn",
        "facebook": "Facebook",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("📊 What did I actually do on the computer today?")
        self.root.geometry("750x620")
        self.root.configure(bg="#f0f4f8")

        # Data storage: key = app name, value = seconds
        self.times = {}
        self.lock = threading.Lock()

        # Control flags
        self.running = False
        self.current_app = None

        # Load today's data
        self.load_today_data()

        # Build GUI
        self.create_widgets()

        # Start periodic UI refresh
        self.update_display()

    def get_active_window_info(self):
        """Return (window_title, process_name) or (None, None)."""
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None, None
            title = win32gui.GetWindowText(hwnd)
            if not title:
                return None, None
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            process_name = process.name()
            return title, process_name
        except Exception:
            return None, None

    def get_app_name(self, title, process_name):
        """
        Determine a clean display name for the current window.
        Priority: 1) site keyword in title, 2) clean process name.
        """
        if not title and not process_name:
            return None

        # 1. Check title for site keywords
        if title:
            title_lower = title.lower()
            for keyword, display in self.SITE_KEYWORDS.items():
                if keyword in title_lower:
                    return display

        # 2. Use process name (remove .exe, capitalize nicely)
        if process_name:
            base = process_name.replace(".exe", "").replace(".EXE", "")
            # Capitalize first letter, keep rest as is (e.g., "Code" for "code.exe")
            if base:
                # Special case: if it's all caps, make it title case
                if base.isupper():
                    base = base.capitalize()
                else:
                    # Some names are like "chrome" -> "Chrome"
                    base = base[0].upper() + base[1:] if len(base) > 1 else base.upper()
                return base

        return "Unknown"

    def track_loop(self):
        """Background thread: every second, record the active app."""
        while self.running:
            title, process_name = self.get_active_window_info()
            if title and process_name:
                app_name = self.get_app_name(title, process_name)
                if app_name:
                    with self.lock:
                        if app_name not in self.times:
                            self.times[app_name] = 0
                        self.times[app_name] += 1
                        self.current_app = app_name
            # If no window is active, we do nothing (no time counted)
            time.sleep(1)

    # ---------- GUI Creation ----------
    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#f0f4f8")
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = tk.Button(btn_frame, text="▶ Start Tracking", bg="#4CAF50", fg="white",
                                   font=("Segoe UI", 10, "bold"), command=self.start_tracking)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop", bg="#f44336", fg="white",
                                  font=("Segoe UI", 10, "bold"), command=self.stop_tracking, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        chart_btn = tk.Button(btn_frame, text="📈 Show Chart", bg="#2196F3", fg="white",
                              font=("Segoe UI", 10, "bold"), command=self.show_chart)
        chart_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(btn_frame, text="🔄 Reset Today", bg="#FF9800", fg="white",
                              font=("Segoe UI", 10, "bold"), command=self.reset_today)
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Status
        self.status_label = tk.Label(main_frame, text="Status: Stopped", font=("Segoe UI", 10),
                                     fg="#777", bg="#f0f4f8")
        self.status_label.pack(anchor=tk.W, pady=(0, 5))

        # Table
        columns = ("App", "Time")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        self.tree.heading("App", text="Application")
        self.tree.heading("Time", text="Time Spent")
        self.tree.column("App", width=300, anchor=tk.W)
        self.tree.column("Time", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Total
        self.total_label = tk.Label(main_frame, text="Total: 0h 0m", font=("Segoe UI", 12, "bold"),
                                    bg="#f0f4f8", fg="#333")
        self.total_label.pack(anchor=tk.E, pady=5)

    # ---------- Control Methods ----------
    def start_tracking(self):
        if not self.running:
            self.running = True
            self.start_btn.config(state=tk.DISABLED, bg="#a5d6a7")
            self.stop_btn.config(state=tk.NORMAL, bg="#f44336")
            self.status_label.config(text="Status: Tracking...", fg="#4CAF50")
            threading.Thread(target=self.track_loop, daemon=True).start()

    def stop_tracking(self):
        if self.running:
            self.running = False
            self.start_btn.config(state=tk.NORMAL, bg="#4CAF50")
            self.stop_btn.config(state=tk.DISABLED, bg="#d3d3d3")
            self.status_label.config(text="Status: Stopped", fg="#777")
            self.save_today_data()

    def refresh_table(self):
        """Update the table with current data, sorted by time descending."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        total_seconds = 0
        with self.lock:
            sorted_items = sorted(self.times.items(), key=lambda x: x[1], reverse=True)
            for app, seconds in sorted_items:
                if seconds > 0:
                    time_str = self.format_time_short(seconds)
                    self.tree.insert("", tk.END, values=(app, time_str))
                    total_seconds += seconds

        self.total_label.config(text=f"Total: {self.format_time_short(total_seconds)}")

    def update_display(self):
        if self.running:
            self.refresh_table()
        self.root.after(1000, self.update_display)

    def format_time_short(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        parts = []
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs and not hours:
            parts.append(f"{secs}s")
        return " ".join(parts) if parts else "0s"

    # ---------- Chart ----------
    def show_chart(self):
        with self.lock:
            data = {k: v for k, v in self.times.items() if v > 0}
        if not data:
            messagebox.showinfo("Info", "No data to display yet.")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Application Usage Chart")
        chart_window.geometry("750x500")
        chart_window.configure(bg="#f0f4f8")

        fig, ax = plt.subplots(figsize=(7.5, 5))
        apps = list(data.keys())
        times_hours = [t / 3600.0 for t in data.values()]

        colors = plt.cm.Set3(range(len(apps)))
        bars = ax.bar(apps, times_hours, color=colors)
        ax.set_ylabel("Hours", fontsize=12)
        ax.set_title("Time Spent on Applications Today", fontsize=14)
        ax.tick_params(axis='x', rotation=40, labelsize=9)

        for bar, val in zip(bars, times_hours):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f"{val:.2f}h", ha='center', va='bottom', fontsize=9)

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ---------- Persistence ----------
    def load_today_data(self):
        filename = f"tracker_{date.today().isoformat()}.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    with self.lock:
                        for k, v in data.items():
                            self.times[k] = v
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_today_data(self):
        filename = f"tracker_{date.today().isoformat()}.json"
        try:
            with self.lock:
                with open(filename, 'w') as f:
                    json.dump(self.times, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def reset_today(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to reset today's data?"):
            with self.lock:
                self.times.clear()
            self.refresh_table()
            self.save_today_data()

    def on_closing(self):
        if self.running:
            self.stop_tracking()
        self.save_today_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()