# Family Budget App — Usage Guide

**言語 / Language / Lingua:**
**English** | [日本語](USAGE_GUIDE.ja.md) | [Italiano](USAGE_GUIDE.it.md)

## Table of Contents

1. [First-Time Setup](#first-time-setup)
2. [Recording Transactions](#recording-transactions)
3. [Budget Management](#budget-management)
4. [Savings](#savings)
5. [Recurring Transactions](#recurring-transactions)
6. [AI Spending Analysis](#ai-spending-analysis)
7. [Future Forecast](#future-forecast)
8. [Family Members & Invites](#family-members--invites)
9. [Currency Settings](#currency-settings)
10. [Language Switching](#language-switching)
11. [Email Notifications](#email-notifications)
12. [Data Export](#data-export)
13. [Categories & Payment Methods](#categories--payment-methods)
14. [FAQ](#faq)

---

## First-Time Setup

### 1. Create an account
1. Open the app and tap **Get Started** (or **Register**)
2. Enter a username (letters and numbers)
3. Enter a password (minimum 8 characters)
4. Tap **Create Account**

### 2. Set up your family
- **Family name** — e.g. "Smith Family"
- **Your nickname** — e.g. "Dad", "Mom", "Taro"

### 3. Categories
Tap **Use default categories** to automatically create:
- **Expenses:** Food, Dining Out, Household, Transport, Utilities, Telecommunications, Medical, Entertainment, Clothing, Insurance (Savings), Other
- **Income:** Salary, Bonus, Side Income, Other Income

You can add, edit, or delete categories any time in **Settings → Categories**.

### 4. Payment methods
Tap **Next** to create defaults:
- Cash, Credit Card, IC Card, PayPay, Bank Transfer

### 5. Done!
The dashboard opens. You're ready to start recording. 🎉

---

## Recording Transactions

### Record an expense
1. Tap the **+** button (bottom right) or **Record Expense**
2. Enter the amount (or use the quick-amount buttons)
3. Select a category
4. Select a payment method
5. Add a memo or date if needed
6. Tap **Save**

### Record income
Same as above, but switch the type to **Income** at the top of the form.

### Attach a receipt photo
On the transaction entry screen, tap **Receipt (optional)** and take a photo or choose from your gallery.

### View and delete transactions
Go to **Menu → Transaction History**, tap a transaction, then tap **Delete**.

---

## Budget Management

### Set a budget
1. **Menu → Budget Management**
2. Select a category (e.g. Food)
3. Enter the monthly amount (e.g. 50000)
4. Tap **Add Budget**

### Monitor usage
Budgets are shown with colour-coded progress bars:
- 🟢 **Green** — below 80 %
- 🟡 **Yellow** — 80 % or above
- 🔴 **Red** — over budget

The dashboard **Budget Status** section shows a quick overview.

### Edit or delete a budget
**Menu → Budget Management** → tap **Edit** or **Delete** next to the budget.

---

## Savings

The app tracks two kinds of savings:

### Cash savings (direct deposits)
For transfers directly into a savings account, bonus savings, etc.

1. **Menu → Register Savings**
2. Enter the amount and an optional memo
3. Tap **Save**

**Effect:** Reduces spendable money; appears in the long-term savings total and the future forecast.

### Insurance savings (insurance-type expenses)
For life insurance, education insurance, pension, etc. that are simultaneously a monthly expense *and* a long-term saving.

1. **Record Expense** → category **Insurance (Savings)**
2. Enter the premium amount
3. Tap **Save**

**Effect:** Added to monthly expenses *and* to the long-term savings total.

### View savings summary
**Menu → Savings Summary** shows:
- Total savings (cash + insurance)
- Cash savings history
- Insurance savings history

---

## Recurring Transactions

Use recurring transactions for fixed costs like rent, salary, or subscriptions.

### Create a template
1. **Menu → Recurring Transactions**
2. Tap **➕ Add**
3. Fill in: type, category, amount, payment method
4. Set **Frequency**: daily / weekly / monthly / yearly
5. Set **Start Date** and, optionally, an **End Date**
6. For monthly frequency, set the **Day of Month** (e.g. 25)
7. Tap **Add**

### Bulk recording (⚡ one click)
1. **Menu → Recurring Transactions**
2. Tap **⚡ Record All Recurring Transactions**
3. Review the list of due transactions
4. Tap **Record**

Transactions already recorded today are skipped automatically.

### Enable / Disable
Toggle the **Active** switch on any template to pause it temporarily.

---

## AI Spending Analysis

Gemini AI reads your transaction history and gives personalised advice.

### How to use it
1. **Menu → AI Analysis**
2. Choose the **analysis period** (1, 3, 6, or 12 months — 3 is recommended)
3. Choose the **analysis type**:
   - **General Spending Analysis** — current status, improvement suggestions, savings targets
   - **Savings Optimisation** — savings rate, methods to improve, future outlook
   - **Budget Planning** — ideal budget allocation, concrete monthly proposals
   - **Category Deep-dive** — detailed analysis of one specific category
   - **Custom Question** — ask the AI anything about your finances
4. Tap **Start AI Analysis**

Results appear as a formatted report with summary cards (income, expenses, balance, savings rate) and the AI's full advice.

### Use your own API key
Each user can set a personal Gemini API key:

1. **Menu → Settings → AI API Key**
2. Paste your key (starts with `AIzaSy…`)
3. Tap **Save**

Your personal key is used instead of the shared app key. Tap **Delete** to remove it.

> Get a free API key at [Google AI Studio](https://aistudio.google.com/).

---

## Future Forecast

Project your savings up to 60 years into the future based on the last 12 months of data.

1. **Menu → Future Forecast**
2. Adjust the forecast period with the spinner (scroll or swipe, 1–60 years)
3. The chart updates automatically

The graph shows separate lines for cash savings, insurance savings, and the combined total.

---

## Family Members & Invites

### Invite a new member
1. **Menu → Settings → Family Information → Member Management**
2. Tap **Create New**
3. Copy the invite link
4. Send it via LINE, WhatsApp, email, etc.

The link is valid for **7 days** and can only be used once.

### Joining via invite link
1. Tap the invite link
2. You'll see "You've been invited to [Family Name]"
3. Register a username and password
4. Enter your nickname
5. Tap **Join**

### Remove a member
**Settings → Member Management** → tap **Delete** next to the member.

---

## Currency Settings

1. **Menu → Settings → Currency Settings** (or tap 💱 in Settings)
2. Select a currency from the dropdown:
   - ¥ Japanese Yen (JPY)
   - $ US Dollar (USD)
   - € Euro (EUR)
   - £ British Pound (GBP)
   - ¥ Chinese Yuan (CNY)
   - ₩ Korean Won (KRW)
   - S$ Singapore Dollar (SGD)
   - A$ Australian Dollar (AUD)
3. Tap **Change**

The selected currency's symbol is used throughout the app. Exchange rates are indicative.

---

## Language Switching

A language selector is always visible in the **bottom-left corner** of the screen.

| Option | Language |
|---|---|
| 🇯🇵 日本語 | Japanese |
| 🇬🇧 English | English |
| 🇮🇹 Italiano | Italian |

Select a language and the page reloads in that language. The preference is saved in a cookie for one year.

---

## Email Notifications

Get a reminder email if no transaction has been recorded for N consecutive days.

### Configure
1. **Menu → Email Notifications**
2. Enable notifications
3. Set **Days without log** (e.g. 3)
4. Enter one or more **notification email addresses** (one per line):
   ```
   dad@example.com
   mom@example.com
   ```
5. Tap **Save**

### How it works
- The `send_log_reminders` management command checks the last recorded transaction date
- If the gap exceeds the configured days, it sends an email to all configured addresses
- At most one email is sent per day per family

### Server setup (admin)
Add a cron job to run the command daily:

```bash
# /etc/cron.d/budget-reminders — runs at 9 AM daily
0 9 * * * youruser /path/to/venv/bin/python /path/to/manage.py send_log_reminders
```

---

## Data Export

Export all transactions for a given month as CSV.

1. **Menu → Settings → Data Export**
2. Select year and month
3. Tap **Download CSV**

The CSV includes: date, type, category, amount, payment method, memo, and recorder.

Open the file in Excel or Google Sheets for further analysis, or keep it as a backup.

---

## Categories & Payment Methods

### Add a category
1. **Settings → Categories → Manage**
2. Tap **➕ Add**
3. Fill in: name, type (expense / income), icon (emoji), and whether it's an insurance savings category
4. Tap **Add**

### Edit or delete a category
Tap **Edit** or **Delete** on the category. Note: categories used by existing transactions cannot be deleted — reassign or delete those transactions first.

### Add a payment method
1. **Settings → Payment Methods → Manage**
2. Tap **➕ Add**
3. Enter the name and type (cash, credit, IC card, QR, bank transfer, other)
4. Tap **Add**

---

## FAQ

**How many family members can I add?**
There is no limit. Create invite links as needed.

**Can I edit a transaction after saving it?**
Currently only deletion is supported. Delete the incorrect entry and re-enter it.

**What if a recurring transaction was already recorded today?**
The bulk-recording button skips it automatically. No duplicates.

**How accurate is the future forecast?**
It extrapolates from the 12-month average. Treat it as an estimate — actual results will vary.

**What if the email notification doesn't arrive?**
Check your SMTP settings. For Gmail, enable 2-factor authentication and generate an App Password.

**Is my data safe?**
Data is stored on the server. For extra security, export a CSV backup regularly.

**Can I use the app offline?**
An internet connection is currently required. The app is PWA-ready for future offline support.

**How far back can I look at transactions?**
All recorded transactions are stored indefinitely — there is no history limit.

**Can I belong to more than one family group?**
One account belongs to one family group. Create a separate account to join another group.

**Does it work on desktop?**
Yes. The app is mobile-first but fully usable in a desktop browser.

**Budget colour thresholds?**
Green < 80 %, Yellow ≥ 80 %, Red > 100 %.

---

**Happy Budgeting! 💰✨**
