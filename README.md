# 🚀 FREE FIRE LIKE API

<p align="center">
  <img src="./logo.png" width="140" alt="SAITO AX Logo">
</p>

<h1 align="center">SAITO FREE FIRE LIKE API</h1>

<p align="center">
  ⚡ ULTRA FAST ASYNC LIKE API USING FLASK + AES + PROTOBUF
</p>

<p align="center">
  <a href="https://t.me/SAITO_LORD">
    <img src="https://img.shields.io/badge/Telegram-SAITO_LORD-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>

  <a href="https://saito_ax">
    <img src="https://img.shields.io/badge/Website-saitoxakane.ea-black?style=for-the-badge&logo=google-chrome&logoColor=white">
  </a>
</p>

---

# ✨ FEATURES

- ⚡ ULTRA FAST ASYNC REQUEST SYSTEM
- 🔐 AES CBC ENCRYPTION
- 📦 PROTOBUF SERIALIZATION
- 🌍 MULTI REGION SUPPORT
- 🧠 SMART TOKEN LOADER
- 🚀 FLASK REST API
- 📊 REAL LIKE COUNT RESPONSE
- 🔥 OB53 SUPPORTED
- 🛡 FULL ERROR HANDLING
- ⚙️ VPS OPTIMIZED

---

# 🌍 SUPPORTED REGIONS

| REGION | CODE |
|--------|------|
| BANGLADESH | BD |
| INDIA | IND |
| BRAZIL | BR |
| UNITED STATES | US |
| NORTH AMERICA | NA |
| SAC | SAC |

---

# 📂 PROJECT STRUCTURE

```bash
project/
│
├── app.py
│
├── like_pb2.py
├── like_count_pb2.py
├── uid_generator_pb2.py
│
├── token_bd.json
├── token_br.json
├── token_ind.json
│
├── requirements.txt
│
└── README.md
```

---

# 📦 REQUIREMENTS

## INSTALL PACKAGES

```bash
pip install -r requirements.txt
```

## requirements.txt

```txt
flask
aiohttp
requests
pycryptodome
protobuf
```

---

# 📁 TOKEN FILES

## token_bd.json

```json
[
  {
    "token": "YOUR_JWT_TOKEN"
  },
  {
    "token": "YOUR_JWT_TOKEN_2"
  }
]
```

## token_br.json

```json
[
  {
    "token": "YOUR_JWT_TOKEN"
  }
]
```

## token_ind.json

```json
[
  {
    "token": "YOUR_JWT_TOKEN"
  }
]
```

---

# ▶️ RUN SERVER

```bash
python app.py
```

Server Running On:

```bash
http://127.0.0.1:5000
```

---

# ⚙️ PRODUCTION DEPLOYMENT

# GUNICORN

```bash
gunicorn -w 4 -k gthread -b 0.0.0.0:5000 app:app
```

# PM2

```bash
pm2 start app.py --interpreter python3 --name ff-like-api
```

# SUPERVISOR

```bash
sudo nano /etc/supervisor/conf.d/fflike.conf
```

## CONFIG

```ini
[program:fflike]
directory=/root/project
command=python3 app.py
autostart=true
autorestart=true
stderr_logfile=/var/log/fflike.err.log
stdout_logfile=/var/log/fflike.out.log
```

## RESTART SUPERVISOR

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart fflike
```

---

# 📌 API ENDPOINT

```bash
GET /like?uid={uid}&server_name={region}
```

---

# ✅ EXAMPLE REQUEST

```bash
https://your-domain.com/like?uid=1727611045&server_name=IND
```

---

# ✅ EXAMPLE RESPONSE

```json
{
  "LikesGivenByAPI": 100,
  "LikesafterCommand": 14700,
  "LikesbeforeCommand": 160,
  "PlayerNickname": "SAITO AE",
  "UID": 123456789,
  "status": 1
}
```

---

# 📊 RESPONSE EXPLANATION

|KEY | DESCRIPTION |
|-----|-------------|
| LIKESGIVENBYAPI | TOTAL LIKES ADDED |
| LIKESAFTERCOMMAND | LIKES AFTER REQUEST |
| LIKESBEFORECOMMAND | LIKES BEFORE REQUEST |
| PLAYERNICKNAME | PLAYER NAME |
| UID | PLAYER UID |
| STATUS | 1 = SUCCESS |
| STATUS | 2 = FAILED |
---

# 🔥 PERFORMANCE

- 250 ASYNC REQUESTS PER COMMAND
- MULTI TOKEN ROTATION
- LOW RAM USAGE
- HIGH SPEED RESPONSE
- VPS OPTIMIZED
- FAST LIKE DELIVERY
---

# 🛠 BUILT WITH

- PYTHON
- FLASK
- ASYNCIO
- AIOHTTP
- REQUESTS
- PYCRYPTODOME
- PROTOBUF

---

# 🧠 ENCRYPTION

THIS API USES:

- AES CBC ENCRYPTION
- PROTOBUF ENCODED BINARY REQUESTS
- BEARER TOKEN AUTHENTICATION

---

# 👨‍💻 DEVELOPER

## 📢 TELEGRAM

<p align="left">
  <a href="https://t.me/saito_ae">
    <img src="https://img.shields.io/badge/Telegram-SAITO_LORD-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white">
  </a>
</p>

## 🌐 WEBSITE

<p align="left">
  <a href="https://saito_like_ea">
    <img src="https://img.shields.io/badge/Website-saitoxakane.ea-black?style=for-the-badge&logo=google-chrome&logoColor=white">
  </a>
</p>

---

# 🌐 OFFICIAL WEBSITE

https://saitolike.lovable.app/

---

# ⚠ DISCLAIMER

THIS PROJECT IS MADE FOR EDUCATIONAL PURPOSES ONLY.

THE DEVELOPER IS NOT RESPONSIBLE FOR ANY MISUSE OF THIS PROJECT.

USE AT YOUR OWN RISK.

---

# ⭐ SUPPORT

IF YOU LIKE THIS PROJECT:

```bash
⭐ STAR THIS REPOSITORY
🍴 FORK THE REPOSITORY
📢 SHARE WITH FRIENDS
```

---

# ❤️ THANKS FOR USING

<p align="center">
  MADE WITH ❤️ BY SAITO
</p>
