# Family Budget App

A mobile-first household budget management system built with Django. Track income, expenses, savings, and get AI-powered financial advice — shared across the whole family.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

### Core
- **Dashboard** — monthly income/expense summary with charts
- **Quick entry** — record a transaction in 2 taps (mobile-optimised)
- **Two types of savings**
  - *Cash savings* — pure deposits/withdrawals
  - *Insurance savings* — counted as both an expense and long-term savings
- **Receipt photos** — attach an image to any transaction
- **Budget management** — set and track per-category monthly budgets with colour-coded alerts (green / yellow / red)
- **Spending charts** — 6-month income/expense trend
- **AI spending analysis** — Gemini AI analyses your data and gives actionable advice

### Recurring Transactions
- Create templates for rent, salary, insurance, subscriptions, etc.
- Frequency: daily / weekly / monthly / yearly
- One-click bulk recording of all due recurring transactions
- Enable/disable individual templates

### Email Notifications
- Reminder email when no transaction has been logged for N days
- Per-family configuration
- Multiple recipient email addresses supported

### Future Forecast
- Predict savings up to 60 years ahead
- Based on the last 12 months of actual data
- Separate projections for cash savings and insurance savings
- Interactive spinner (mouse wheel / swipe) to change the forecast period

### Family Sharing
- Multiple members share one household budget
- Invite new members via a time-limited link (7-day expiry)
- Every transaction shows who recorded it

### Other
- **Payment methods** — cash, credit card, QR payment, bank transfer, IC card, etc.
- **Custom categories** — add, edit, and delete categories freely
- **Data export** — download transactions as CSV
- **Multi-currency** — JPY, USD, EUR, GBP, CNY, KRW, SGD, AUD (switchable per family)
- **Multi-language** — Japanese / Italian / English (cookie-based, switchable at any time)
- **Personal AI API key** — each user can set their own Gemini API key in Settings
- **PWA-ready** — installable on mobile as a home-screen app

---

## Quick Start

### Requirements
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rikiza89/family-budget-app.git
cd family-budget-app

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations (creates tables and seeds currency data)
python manage.py migrate

# 5. Create a superuser (optional, for /admin access)
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open `http://localhost:8000` in your browser.

> **Existing database (no migration history)?**
> If you already have a database created before migration files existed, run:
> ```bash
> python manage.py migrate --fake 0001
> python manage.py migrate
> ```

---

## Project Structure

```
family-budget-app/
├── budget/
│   ├── models.py                  # Data models
│   ├── views.py                   # Dashboard, AI analysis, export
│   ├── setup_views.py             # Settings, categories, currencies, invites
│   ├── auth_views.py              # Login, register, profile setup
│   ├── forms.py                   # Django forms
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Django admin registration
│   ├── migrations/                # Database migrations (incl. currency seed)
│   ├── management/commands/
│   │   └── send_log_reminders.py  # Email notification cron command
│   ├── templatetags/
│   │   └── translation_tags.py    # |translate filter for dynamic strings
│   └── templates/budget/          # HTML templates
├── family_budget/
│   ├── settings.py
│   └── urls.py
├── locale/
│   ├── en/LC_MESSAGES/            # English translations (.po + compiled .mo)
│   └── it/LC_MESSAGES/            # Italian translations (.po + compiled .mo)
├── requirements.txt
└── manage.py
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2+ |
| Frontend | HTML5, Tailwind CSS (CDN), Vanilla JS |
| Database | SQLite (default) / PostgreSQL compatible |
| Charts | Chart.js |
| AI | Google Gemini API (`google-generativeai`) |
| Image processing | Pillow |
| Date utilities | python-dateutil |
| Internationalisation | Django i18n (EN / IT / JA) |

---

## Data Models

### Key Models

| Model | Purpose |
|---|---|
| `Family` | One household group; holds currency preference |
| `FamilyMember` | Links a Django `User` to a `Family`; stores personal Gemini API key |
| `Transaction` | Income or expense record |
| `CashSaving` | Direct savings deposit |
| `Category` | User-defined category; `is_insurance_saving=True` marks insurance-type |
| `PaymentMethod` | Cash, card, QR, etc. |
| `Budget` | Monthly spending limit per category |
| `RecurringTemplate` | Template for periodic transactions |
| `Currency` | Currency code, symbol, and JPY exchange rate |
| `EmailNotificationSettings` | Per-family email reminder configuration |

### Savings Logic

**Cash savings (`CashSaving`):** Reduces available spending money; counted only as long-term savings.

**Insurance savings (`Transaction` with `is_insurance_saving=True`):** Counted as a monthly expense *and* as long-term savings at the same time.

---

## Configuration

### AI (Gemini)

Set the shared API key in `.env` or `settings.py`:

```python
GEMINI_API_KEY = 'AIzaSy...'
```

Each user can also set a personal key in **Settings → AI API Key**. The personal key takes priority.

### Email Notifications

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Gmail app password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

Run the reminder command daily with cron:

```bash
# /etc/cron.d/budget-reminders
0 9 * * * youruser /path/to/venv/bin/python /path/to/manage.py send_log_reminders
```

### Production Checklist

```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```

---

## Translations

Translation source files live in `locale/<lang>/LC_MESSAGES/django.po`.
After editing a `.po` file, recompile:

```bash
python manage.py compilemessages
```

Compiled `.mo` files are already committed and ready to use without running the above command.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Migration error | `python manage.py migrate --fake 0001 && python manage.py migrate` |
| Currency dropdown empty | Run `python manage.py migrate` — the 0003 migration seeds currencies automatically |
| Image upload error | `pip install pillow && mkdir -p media/receipts` |
| Translations not applied | `python manage.py compilemessages` |
| Email not sent | Check SMTP settings; for Gmail enable 2FA and use an App Password |

---

## Demo

A live demo is available at [mydemoapplication.pythonanywhere.com](https://mydemoapplication.pythonanywhere.com).
Data is cleared periodically. For production hosting assistance, feel free to reach out.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.

## Issues & Support

Report bugs or request features at [GitHub Issues](https://github.com/Rikiza89/family-budget-app/issues).

---

Made with ❤️ for families managing their budgets together.
