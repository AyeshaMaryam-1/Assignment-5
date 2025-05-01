# 🔐 Secure Data Encryption System

[![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)

A simple but effective Streamlit app for **securely encrypting and retrieving sensitive data** using custom passkeys and session-based brute-force protection.

---

## 🚀 Features

- 🔒 **Secure Encryption** with user-defined passkeys (Fernet/AES-based)
- 🧠 **Session Memory** to manage data and failed login attempts
- 🧪 **Decryption Attempts Limit** with lockout and reauthorization
- 🆔 **Unique Data ID** for referencing and retrieval
- 👤 **Master Admin Login** to reset after 3 failed attempts
- 🎨 **Minimal, Emoji-Powered UI** for a smooth user experience

---

## 📸 Demo Preview

> Coming Soon: Hosted version on Streamlit Community Cloud (optional)

---

## 🛠️ Technologies Used

| Tool           | Role                            |
|----------------|---------------------------------|
| [Streamlit](https://streamlit.io/) | Frontend UI Framework          |
| `cryptography` | Symmetric Encryption (`Fernet`) |
| `hashlib`      | Passkey hashing (`SHA-256`)     |
| `uuid`         | Unique ID generation            |
| `time`         | Lockout timing mechanism        |

---

## 🔐 Usage Guide

### ➕ Store Data
- Navigate to **Store Data**.
- Enter your data and create a secure passkey.
- Receive a unique **Data ID** – save this to retrieve your data later.

### 🔍 Retrieve Data
- Navigate to **Retrieve Data**.
- Enter your saved **Data ID** and passkey.
- If both are correct, your data will be decrypted and shown.

### ⛔ Brute Force Protection
- After **3 failed decryption attempts**, the system locks access.
- User is automatically redirected to the **Login** page.

### 🔑 Admin Reauthorization
- To regain access, enter the **master password** (`admin123`) on the Login page.
- This resets the failed attempt count and restores functionality.

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes only.
It is not secure for storing sensitive personal data in production.

- No persistent storage (data is lost on refresh)

- Master password is hardcoded (admin123)

- No multi-user or database support

## ✍️ Author

Developed by **Ayesha Maryam**
