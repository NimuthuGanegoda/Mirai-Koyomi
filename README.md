# 🇱🇰 Sri Lanka Holidays API

<div align="center">

![License](https://img.shields.io/github/license/NimuthuGanegoda/srilanka-holidays-master?style=for-the-badge&color=blue)
![Data Integrity](https://img.shields.io/badge/Data-Verified-success?style=for-the-badge)

</div>

---

## 📖 **Description**

Sri Lanka Holidays API is an asynchronous FastAPI application that provides accurate and highly reliable data about Sri Lankan holidays. The API leverages Redis for caching with a robust fallback to local JSON file reads, ensuring high availability and seamless data delivery.

It serves data for the years **2021 to 2028**, covering Public, Bank, and Mercantile holidays. The project includes endpoints for checking specific holidays, retrieving detailed holiday information, fetching coverage status, and even combining personal calendars with Sri Lanka public holidays.

---

## ✨ **Core Features**

*   🚀 **FastAPI Backend**: Built with Python's FastAPI for high performance and asynchronous request handling.
*   📅 **Extended Coverage**: Verified holiday data spanning from **2021 through 2028**.
*   🔒 **Secure Access**: Authenticated endpoints utilizing API key validation (via `X-API-Key` header or `api_key` query parameter).
*   ⚡ **Redis Caching & Fallback**: Fast lookups via Redis for API keys and holiday data. Automatically falls back to local JSON data files and environment variables if Redis is unavailable.
*   🔄 **Combined Calendar Integration**: Create an aggregated `.ics` calendar from your personal ICS feed alongside Sri Lankan public holidays.

---

## ⚙️ **Configuration & Environment Variables**

The application uses a `.env` file or standard environment variables for configuration. Below is a list of supported variables:

| Variable | Description |
|----------|-------------|
| `API_KEYS` | Comma-separated list of fallback API keys used when Redis is unavailable. |
| `REDIS_HOST` | Hostname of the Redis server. |
| `REDIS_PORT` | Port number of the Redis server. |
| `REDIS_USERNAME` | Username for Redis authentication (optional). |
| `REDIS_PASSWORD` | Password for Redis authentication (optional). |
| `ENV` | Set to `DEV` to mount static files under `/public` for development. |
| `VERCEL` | Set to `1` when deploying on Vercel to route the root URL to `/index.html`. |

---

## 🛣️ **API Endpoints**

### Public & Documentation
*   `GET /public` - Serves the home page (only when `ENV=DEV`).
*   `GET /docs` - Swagger UI documentation.
*   `GET /redoc` - ReDoc API documentation.

### Unauthenticated APIs
*   `HEAD /api/v1/health` - Simple health check.

### Authenticated APIs
*(Require a valid API key passed via the `X-API-Key` header or `api_key` query parameter)*

*   `GET /api/v1/status` - Returns the operational status of the API, database connectivity, and version info.
*   `GET /api/v1/version` - Returns the current API version and data store limits.
*   `GET /api/v1/coverage` - Checks the availability of data coverage for a specified year.
*   `GET /api/v1/check_holiday` - Checks whether a specific date (year/month/day) is a holiday.
*   `GET /api/v1/holiday_info` - Retrieves detailed information about a holiday on a given date.
*   `GET /api/v1/holidays` - Returns a list of holidays for a specific year and optional month, format, and type filtering.
*   `GET /api/v1/combined_calendar` - Merges a user-provided ICS calendar feed URL with the Sri Lanka Holidays Master ICS and returns a combined calendar.

---

## 📂 **Project Structure**

```bash
.
├── 📁 data/               # Standardized holiday datasets
├── 📁 json/               # Fallback structured JSON holiday data (2021-2028)
├── 📁 public/             # Project assets & documentation frontend files
├── 📁 requirements/       # Dependency management files (base.txt, etc.)
├── 📄 app.py              # Main FastAPI application
├── 📄 vercel.json         # Deployment configuration for Vercel
├── 📄 .env                # Environment configuration file (ignored in git)
└── 📄 README.md           # This file
```

---

## 🛠️ **Local Development**

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements/base.txt
   ```
3. **Set up your `.env` file** matching the configuration section above.
4. **Run the development server:**
   ```bash
   uvicorn app:app --reload
   ```

---

<div align="center">
Developed for the Sri Lankan Developer Community.
</div>
