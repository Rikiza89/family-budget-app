# App per la Gestione del Budget Familiare

Un sistema di gestione del budget familiare mobile-first costruito con Django. Registra entrate, spese e risparmi, e ricevi consigli finanziari basati su AI — condivisi con tutta la famiglia.

**言語 / Language / Lingua:**
[English](README.md) | [日本語](README.ja.md) | **Italiano**

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Funzionalità

### Funzioni principali
- **Dashboard** — riepilogo mensile di entrate/uscite con grafici
- **Inserimento rapido** — registra una transazione in 2 tocchi (ottimizzato per mobile)
- **Due tipi di risparmio**
  - *Risparmio in contanti* — depositi e prelievi diretti
  - *Risparmio assicurativo* — conteggiato sia come spesa che come risparmio a lungo termine
- **Foto ricevute** — allega un'immagine a qualsiasi transazione
- **Gestione budget** — imposta e monitora budget mensili per categoria con barre colorate (verde / giallo / rosso)
- **Grafici delle spese** — andamento entrate/uscite negli ultimi 6 mesi
- **Analisi AI** — Gemini AI analizza i tuoi dati finanziari e fornisce consigli pratici

### Transazioni ricorrenti
- Crea template per affitto, stipendio, assicurazioni, abbonamenti, ecc.
- Frequenza: giornaliera / settimanale / mensile / annuale
- Registrazione massiva con un clic di tutte le transazioni in scadenza
- Attiva/disattiva i singoli template

### Notifiche email
- Email di promemoria se non viene registrata alcuna transazione per N giorni
- Configurazione per nucleo familiare
- Supporto per più indirizzi email destinatari

### Previsione futura
- Proietta i risparmi fino a 60 anni nel futuro
- Basata sugli ultimi 12 mesi di dati reali
- Proiezioni separate per risparmio in contanti e risparmio assicurativo
- Spinner interattivo (rotella del mouse / swipe) per cambiare il periodo di previsione

### Condivisione familiare
- Più membri condividono lo stesso budget familiare
- Aggiungi nuovi membri tramite link d'invito a tempo limitato (scadenza 7 giorni)
- Ogni transazione mostra chi l'ha registrata

### Altro
- **Metodi di pagamento** — contanti, carta di credito, pagamento QR, bonifico bancario, carta IC, ecc.
- **Categorie personalizzate** — aggiungi, modifica ed elimina liberamente
- **Esportazione dati** — scarica le transazioni in formato CSV
- **Multi-valuta** — JPY, USD, EUR, GBP, CNY, KRW, SGD, AUD (modificabile per nucleo familiare)
- **Multi-lingua** — Giapponese / Inglese / Italiano (basato su cookie, modificabile in qualsiasi momento)
- **Chiave API AI personale** — ogni utente può impostare la propria chiave Gemini API nelle Impostazioni
- **PWA-ready** — installabile come app sulla schermata iniziale del mobile

---

## Avvio rapido

### Requisiti
- Python 3.11+
- pip

### Installazione

```bash
# 1. Clona il repository
git clone https://github.com/Rikiza89/family-budget-app.git
cd family-budget-app

# 2. Crea e attiva un ambiente virtuale
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Esegui le migrazioni (crea le tabelle e inserisce i dati delle valute)
python manage.py migrate

# 5. Crea un superutente (opzionale, per l'accesso a /admin)
python manage.py createsuperuser

# 6. Avvia il server di sviluppo
python manage.py runserver
```

Apri `http://localhost:8000` nel browser.

> **Database esistente (senza storico migrazioni)?**
> Se hai già un database creato prima che esistessero i file di migrazione, esegui:
> ```bash
> python manage.py migrate --fake 0001
> python manage.py migrate
> ```

---

## Struttura del progetto

```
family-budget-app/
├── budget/
│   ├── models.py                  # Modelli dati
│   ├── views.py                   # Dashboard, analisi AI, esportazione
│   ├── setup_views.py             # Impostazioni, categorie, valute, inviti
│   ├── auth_views.py              # Login, registrazione, configurazione profilo
│   ├── forms.py                   # Form Django
│   ├── urls.py                    # Routing URL
│   ├── admin.py                   # Registrazione pannello admin Django
│   ├── migrations/                # Migrazioni del database (incl. seed valute)
│   ├── management/commands/
│   │   └── send_log_reminders.py  # Comando cron per notifiche email
│   ├── templatetags/
│   │   └── translation_tags.py    # Filtro |translate per stringhe dinamiche
│   └── templates/budget/          # Template HTML
├── family_budget/
│   ├── settings.py
│   └── urls.py
├── locale/
│   ├── en/LC_MESSAGES/            # Traduzioni inglesi (.po + .mo compilato)
│   └── it/LC_MESSAGES/            # Traduzioni italiane (.po + .mo compilato)
├── requirements.txt
└── manage.py
```

---

## Stack tecnologico

| Livello | Tecnologia |
|---|---|
| Backend | Django 5.2+ |
| Frontend | HTML5, Tailwind CSS (CDN), Vanilla JS |
| Database | SQLite (predefinito) / compatibile con PostgreSQL |
| Grafici | Chart.js |
| AI | Google Gemini API (`google-generativeai`) |
| Elaborazione immagini | Pillow |
| Utilità date | python-dateutil |
| Internazionalizzazione | Django i18n (JA / EN / IT) |

---

## Modelli dati

| Modello | Scopo |
|---|---|
| `Family` | Gruppo familiare; contiene la preferenza di valuta |
| `FamilyMember` | Collega un `User` Django a una `Family`; memorizza la chiave Gemini personale |
| `Transaction` | Registrazione di entrata o uscita |
| `CashSaving` | Deposito diretto di risparmio |
| `Category` | Categoria definita dall'utente; `is_insurance_saving=True` indica tipo assicurativo |
| `PaymentMethod` | Contanti, carta, QR, ecc. |
| `Budget` | Limite di spesa mensile per categoria |
| `RecurringTemplate` | Template per transazioni periodiche |
| `Currency` | Codice valuta, simbolo e tasso di cambio in JPY |
| `EmailNotificationSettings` | Configurazione promemoria email per nucleo familiare |

### Logica dei risparmi

**Risparmio in contanti (`CashSaving`):** Riduce il denaro disponibile; conteggiato solo come risparmio a lungo termine.

**Risparmio assicurativo (`Transaction` con `is_insurance_saving=True`):** Conteggiato come spesa mensile *e* come risparmio a lungo termine contemporaneamente.

---

## Configurazione

### AI (Gemini)

Imposta la chiave API condivisa in `.env` o `settings.py`:

```python
GEMINI_API_KEY = 'AIzaSy...'
```

Ogni utente può anche impostare una chiave personale in **Impostazioni → Chiave API AI**. La chiave personale ha la priorità.

### Notifiche email

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Password app Gmail
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

Esegui il comando di promemoria ogni giorno con cron:

```bash
# /etc/cron.d/budget-reminders — eseguito alle 9:00 ogni giorno
0 9 * * * youruser /path/to/venv/bin/python /path/to/manage.py send_log_reminders
```

### Checklist produzione

```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```

---

## Traduzioni

I file sorgente delle traduzioni si trovano in `locale/<lang>/LC_MESSAGES/django.po`.
Dopo aver modificato un file `.po`, ricompila:

```bash
python manage.py compilemessages
```

I file `.mo` compilati sono già inclusi nel repository e pronti all'uso senza eseguire il comando sopra.

---

## Risoluzione problemi

| Problema | Soluzione |
|---|---|
| Errore di migrazione | `python manage.py migrate --fake 0001 && python manage.py migrate` |
| Menu a tendina valute vuoto | Esegui `python manage.py migrate` — la migrazione 0003 inserisce le valute automaticamente |
| Errore upload immagini | `pip install pillow && mkdir -p media/receipts` |
| Traduzioni non applicate | `python manage.py compilemessages` |
| Email non ricevute | Controlla le impostazioni SMTP; per Gmail abilita la verifica in 2 passaggi e usa una Password app |

---

## Licenza

MIT — vedi [LICENSE](LICENSE) per i dettagli.

## Segnalazione bug e richieste di funzionalità

Apri una segnalazione su [GitHub Issues](https://github.com/Rikiza89/family-budget-app/issues).

---

Fatto con ❤️ per le famiglie che gestiscono il budget insieme.
