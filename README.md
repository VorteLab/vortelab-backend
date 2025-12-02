# VorteLab Backend (Django + Django REST Framework)

This repository contains the backend API of the **VorteLab** platform.  
It is built using Django, Django REST Framework, JWT authentication and a modular app structure.

The backend provides user authentication, account management, profile data, and a secure internal messaging system between users and administrators.

---

## 🚀 Features

### 🔐 Authentication
- JWT authentication (access + refresh tokens)
- Login, registration, and secure session handling
- Password hashing and Django security middleware enabled

### 👤 User Accounts
- User profile model
- Company field, balance field, avatar, and related profile data
- Django admin panel enabled for full account management

### 💬 Internal Messaging System
- Built-in chat between users and site administrators  
- Messages stored securely in the database  
- Integrated with JWT authentication  
- Designed for an internal support/communication workflow

### 📡 API
- Fully REST-based endpoints (DRF)
- Serializer clean separation
- Modular URLs per app (`accounts/`, `messaging/`, etc.)

---

## 📁 Project Structure

```
/accounts          → User accounts, profiles, auth endpoints
/messaging         → Internal chat system (optional)
/server            → Core Django project (settings, wsgi, urls)
/staticfiles       → Static files collected by Django
manage.py          → Main Django entry point
requirements.txt   → Python dependencies
db.sqlite3         → Development demo database
```

---

## 🛠 Installation

### 1. Clone the repository
```
git clone https://github.com/VorteLab/vortelab-backend.git
cd vortelab-backend
```

### 2. Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run migrations
```
python manage.py migrate
```

### 5. Start the development server
```
python manage.py runserver
```

The backend runs at:
```
http://127.0.0.1:8000
```

---

## 🔧 Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
```

⚠️ Environment files **must NOT be committed**.

---

## 📦 Production Notes

- Use PostgreSQL or MySQL in production
- Configure `STATIC_ROOT` and run:
  ```
  python manage.py collectstatic
  ```
- Configure `DEBUG=False`
- Use a real JWT expiration policy
- Serve with **gunicorn + nginx** or **uvicorn + daphne** for ASGI

---

## 📎 Related Repositories

- **Frontend (Vue 3):** https://github.com/VorteLab/vortelab-frontend  
- **Main website:** https://github.com/VorteLab/vortelab-site  
- **Organization:** https://github.com/VorteLab

---

## ⚠️ Demo Database Notice

This repository includes a **demo `db.sqlite3`**, used for testing and early development.  
It should not contain real user data, real messages, or sensitive credentials.

For production usage:
- Replace with a new database
- Delete the committed sqlite file
- Add `db.sqlite3` to `.gitignore`

---

## 📝 License

This backend is part of the VorteLab platform.  
All rights reserved.

