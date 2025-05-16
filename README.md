# FastAPI Auth Middleware

A lightweight authentication and authorization middleware built using FastAPI and Docker.  
It provides user login, token-based authentication, and secure access to protected endpoints.

## 🔧 Features

- ✅ FastAPI-based backend
- 🔐 User authentication via `/login`
- 🔑 JWT token generation
- 🛡️ Protected middleware with token validation
- 🗂️ User database using SQLite and SQLModel
- 🐳 Dockerized for consistent deployment

## 📦 Usage

1. Build the Docker image:

```bash
docker build -t fastapi-auth .
docker run -d -p 8000:8000 fastapi-auth
Open your browser at http://localhost:8000/docs to test the API.

🧪 Test Credentials
Username: admin

Password: admin123

📁 Endpoints
POST /login — Authenticate user and receive JWT token

GET /protected — Sample protected endpoint

GET /users — Return list of users (if authorized)

🚀 Technologies
FastAPI

Python 3.10

SQLModel

SQLite

Docker

📂 Project Structure
project/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── auth.py
│   └── database.py
├── Dockerfile
├── requirements.txt
└── README.md
