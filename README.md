# URL Shortener
A lightweight, secure URL shortener built with Python and Flask. It provides both a JSON REST API and a web interface to shorten long URLs, redirect short codes to original destinations, and prevent enumeration attacks and request spam.

---

## Features

* **Dual Interface:** Provides a JSON API (`/shorten`) for scripts/applications and a web form (`/shorten-form`) rendered with Jinja templates.
* **Deterministic & Collision-Free Encoding:** Generates unique short codes by converting auto-incremented database IDs into short strings using Hashids.
* **IDOR & Enumeration Protection:** Obfuscates consecutive database IDs using a salted `Hashids` configuration with a minimum length of 6 characters.
* **Input Validation:** Rejects malformed URLs using `urllib.parse` before performing database operations.
* **SQL Injection Prevention:** Uses parameterized SQLite queries (`?` placeholders) for all database reads and writes.
* **Rate Limiting:** Protects write endpoints against abuse using `Flask-Limiter` (default global limits plus an endpoint-specific 10 requests/minute cap).

---

## Tech Stack

* **Language:** Python 3
* **Framework:** Flask
* **Database:** SQLite3 (standard library)
* **Libraries:** `Flask-Limiter`, `hashids`, `python-dotenv`

---

## Getting Started

### 1. Clone & Set Up Environment

```bash
cd url-shortener
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
