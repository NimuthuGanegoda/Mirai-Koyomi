
# 🇱🇰 Sri Lanka Holidays - API & Master Data

<div align="center">

![License](https://img.shields.io/github/license/NimuthuGanegoda/srilanka-holidays-master?style=for-the-badge&color=blue)
![Last Commit](https://img.shields.io/github/last-commit/NimuthuGanegoda/srilanka-holidays-master?style=for-the-badge&color=green)
![API Status](https://img.shields.io/uptimerobot/status/m801863984-21c7b9399c6e347151e59c53?style=for-the-badge&label=API%20STATUS)

---

### 🚀 **High-Performance API & Validated Holiday Datasets**
*Providing a standardized, enterprise-ready source for Sri Lankan holiday data.*

[Explore Documentation](https://srilanka-holidays.vercel.app/docs) • [Request API Key](https://srilanka-holidays.vercel.app) • [Download Data](data/holidays/)

</div>

---

## 📖 **Description**

An open-source ecosystem delivering high-accuracy Sri Lankan holiday data. This repository serves as the **unified master source**, offering validated datasets in multiple formats optimized for enterprise integration and individual scheduling.

---

## ✨ **Core Features**

*   📅 **Extended Coverage**: Verified holiday data for **2021 through 2028**.
*   🏷️ **Visual Markers**: Instant identification via standard indicators: `*` (Public), `†` (Bank), and `‡` (Mercantile).
*   🍎 **Apple & Google Ready**: Strict **CRLF** compliance and **VTIMEZONE** support for flawless calendar sync.
*   🔔 **Smart Alarms**: Integrated `VALARM` notifications at 09:00 AM on the day preceding each holiday.
*   🔄 **CI/CD Automation**: Real-time synchronization and multi-format conversion (JSON, CSV, XML, ICS).

---

## 📂 **Project Structure**

A clean, modular architecture designed for scalability and maintainability:

```bash
.
├── 📁 data/               # 📊 Standardized holiday datasets
│   └── 📁 holidays/       # 🏝️ Validated holiday collections
│       ├── ics/           # 🗓️ iCalendar files (Apple/Google optimized)
│       ├── json/          # 🏗️ Structured JSON for developers
│       ├── csv/           # 📑 Spreadsheet-ready formats
│       └── xml/           # 🧬 Legacy integration support
├── 📁 src/                # 💻 Core application source code
│   ├── api/               # 🌐 FastAPI implementation
│   └── converters/        # 🛠️ Data processing & sync scripts
├── 📁 requirements/       # 📋 Dependency management
│   ├── base.txt           # 📦 Core production dependencies
│   └── github.txt         # 🤖 CI/CD specific requirements
└── 📁 public/             # 🎨 API frontend & static assets
```

---

## 🛠️ **Developer Integration**

### **Public API Usage**
```bash
# Get holidays for a specific year
curl -H "X-API-Key: your-key" "https://srilanka-holidays.vercel.app/api/v1/holidays?year=2025"
```

### **Local Setup**
1.  **Clone**: `git clone https://github.com/NimuthuGanegoda/srilanka-holidays-master.git`
2.  **Install**: `pip install -r requirements/base.txt`
3.  **Run**: `fastapi dev src/api/app.py`

---

## 🛡️ **Data Integrity**

Every holiday entry is manually cross-referenced with the **Official Government Gazette** of Sri Lanka. We prioritize data accuracy over automated heuristics to ensure 100% reliability for production environments.

---

<div align="center">
Developed with 💎 for the Sri Lankan Developer Community.
</div>
