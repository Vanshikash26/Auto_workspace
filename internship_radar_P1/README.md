# 🎯 InternShip Radar

A Python automation tool that discovers remote internships and jobs, matches them against your skills, and notifies you only about NEW opportunities.

## 🔗 Live Demo:
      https://autoworkspace-a3gguarfpakad4lhopyehu.streamlit.app/

## ✨ Features

- 🌐 **Real Data Integration** — Fetches live remote jobs from the Remotive API
- 🧠 **Smart Skill Matching** — Weighted scoring based on core and known skills
- 📍 **Location Filtering** — Work-from-home or specific target cities
- 🔔 **New Job Detection** — Shows only unseen jobs using state management
- 📧 **Email Alerts** — Sends Gmail notifications when new jobs are found
- 📊 **Excel Reports** — Generates a styled dashboard of all matched jobs

## 🛠️ Tech Stack

`Python` · `Requests` · `Pandas` · `Openpyxl` · `smtplib`

## 📁 Project Structure

```
internship_radar/
├── config.py      # Skills, cities, and email settings
├── fetcher.py     # Fetches data from the API
├── state.py       # Tracks seen jobs to avoid duplicates
├── notifier.py    # Sends email alerts
├── reporter.py    # Generates Excel reports
└── main.py        # Main application logic
```

## ▶️ How to Run

1. Configure your skills, target cities, and email settings in `config.py`
2. Install the dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`
4. View the generated report: `internship_report.xlsx`

## 📋 How It Works

1. **Fetch** — Pulls live remote jobs from the Remotive API
2. **Filter** — Keeps only jobs open to your location preference (WFH / target cities)
3. **Match** — Scores each job against your core and known skills
4. **Detect** — Compares with previously seen jobs to find NEW ones
5. **Notify** — Displays results, sends an email alert, and saves an Excel report

## 🔮 Future Enhancements

- [ ] Integration with Internshala and LinkedIn
- [ ] Telegram notifications
- [ ] Web-based dashboard
- [ ] Daily automated scheduling

---

Built with ❤️ by Vanshika
