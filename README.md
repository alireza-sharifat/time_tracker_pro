# 🖥️ TimeTracker – What Did I Actually Do on the Computer Today?

Stop guessing – start knowing. TimeTracker is a smart Windows application that automatically logs your time across all applications and websites. Whether you're a developer, designer, student, or just curious about your digital habits, this tool gives you clear, visual insights into how you actually spend your day.

With a single click, you can see exactly how many hours went into VS Code, Chrome, YouTube, Slack, and even hidden gems like ChatGPT or GitHub. No manual timers, no spreadsheets – just pure data.

---

## ✨ Features

- 🔍 **Universal App Detection** – No whitelist needed. Every running process is automatically recognised and named.
- 🌐 **Smart Website Detection** – Identifies YouTube, Netflix, Twitch, GitHub, Gmail, ChatGPT, Reddit, and many more – even inside browsers.
- ⏱️ **Boot‑Time History** – The moment you open the app, it pulls usage data from system startup, so you never lose track of your morning workflow.
- 📈 **Live Tracking** – Updates every second while the app is running. Watch your stats grow in real time.
- 💾 **Daily Persistence** – Data is automatically saved per day in a clean JSON file. Restart the app, and it picks up right where you left off.
- 📊 **Interactive Bar Chart** – One click shows a beautiful graph of your day, with hour labels on each bar.
- 🎨 **Modern, Clean UI** – A clutter‑free interface with a sortable table, total time summary, and clear status indicators.
- 🚀 **Standalone Executable** – Package the app as a single `.exe` file – no Python installation required on the target machine.

---

## 📦 Requirements

- Windows 10 / 11 (the app uses Windows‑specific APIs)
- Python 3.7 or higher (if running from source)
- Dependencies: `pywin32`, `psutil`, `matplotlib`

---

## 🔧 Installation & Running

### Option 1 – Run from source

1. Clone the repository  
   ```bash
   git clone https://github.com/alireza-sharifat/time-tracker.git
   cd time-tracker
   ```

2. Create a virtual environment (recommended)  
   ```bash
   python -m venv venv
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the app  
   ```bash
   python time_tracker_pro.py
   ```

### Option 2 – Use the pre‑built executable

Download the latest `TimeTracker.exe` from the [Releases](https://github.com/alireza-sharifat/time-tracker/releases) section, double‑click, and you're ready to go.

---

## 🚀 How to Use

1. **Start the app** – you'll see an empty table and a **Start Tracking** button.  
2. **Click Start** – the app begins monitoring your active window. The table updates every second.  
3. **View your stats** – applications are listed in descending order of usage. The total time is shown at the bottom.  
4. **Show chart** – click the **Show Chart** button to open a separate window with a bar chart of your day.  
5. **Stop tracking** – click **Stop** to pause recording. Your data is automatically saved.  
6. **Reset today** – if you want to start fresh, use the **Reset Today** button (confirmation required).

> **Pro tip:** The app automatically loads historical data from system boot every time it starts. That means even if you open the app at lunchtime, you'll already see your morning activity!

---

## 🧪 Building a Standalone .exe

If you want to share the app or use it without Python, package it with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="TimeTracker" time_tracker_pro.py
```

The executable will be created in the `dist/` folder. You can rename it and move it anywhere.

---

## 📂 File Structure

```
time-tracker/
├── time_tracker_pro.py      # Main application
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
└── tracker_YYYY-MM-DD.json  # Daily data files (auto‑generated)
```

---

## ⚙️ Customisation

- **Add or remove website keywords** – edit the `SITE_KEYWORDS` dictionary in `time_tracker_pro.py`.  
- **Change the update frequency** – modify `time.sleep(1)` inside the `track_loop` method (be careful – lower values increase CPU usage).  
- **Change the data file location** – update the filename logic in `load_today_data()` and `save_today_data()`.

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named 'win32gui'` | Make sure you have `pywin32` installed: `pip install pywin32` |
| The chart window is blank | Check that `matplotlib` is installed and that there is data to display. |
| Tracking doesn't start | Ensure you are running Windows and have granted any necessary permissions. |
| Data not saving | Verify that the application has write permissions in its directory (run as administrator if needed). |

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are always welcome!  
Here's how you can help:

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/your-feature`).  
3. Commit your changes (`git commit -m 'Add some feature'`).  
4. Push to the branch (`git push origin feature/your-feature`).  
5. Open a Pull Request – describe your changes clearly.

Please follow the existing code style and include tests where applicable.

---

## 💖 Support the Project

If you find TimeTracker useful and want to support its continued development, consider:

- Starring the repository on GitHub – it helps others discover the project.  
- Reporting bugs or suggesting features via [Issues](https://github.com/alireza-sharifat/time-tracker/issues).  
- Buying me a coffee – every little bit keeps me motivated!

Thank you for using and supporting TimeTracker! 🙏

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [psutil](https://github.com/giampaolo/psutil) – cross‑platform process and system utilities  
- [pywin32](https://github.com/mhammond/pywin32) – Windows API bindings  
- [matplotlib](https://matplotlib.org/) – powerful plotting library  
- All contributors and users who have provided feedback and inspiration

---

Made with ❤️ for everyone who wants to understand their digital life better.

Happy tracking! 📊

---

⭐ If you like this project, please give it a star on GitHub! It really helps and motivates me to keep improving it.
