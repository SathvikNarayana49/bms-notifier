# 🎬 BookMyShow Ticket Notifier

## 📌 Overview

In cities like Hyderabad, movie enthusiasts often rush to book **First Day First Show (FDFS)** tickets at popular theatres. Since ticket availability on BookMyShow is unpredictable, users spend hours repeatedly refreshing the website.

This project automates that process by continuously monitoring ticket availability and instantly notifying users via email when tickets are released.

---

## 🚀 Features

* 🔔 Real-time ticket availability monitoring
* 🎥 Filter alerts by specific movie
* 🏢 Optional filtering by theatre
* 📧 Instant email notifications
* 🌐 Simple web interface for user input
* ⚙️ Background monitoring using multithreading

---

## 🛠️ Tech Stack

* Python
* Flask (Backend Web Server)
* Selenium (Web Automation)
* SMTP (Email Notifications)
* HTML, CSS, JavaScript (Frontend)
* Threading

---

## ⚙️ How It Works

1. User enters details (email, city, movie, theatre) via web UI
2. Backend starts a monitoring process in the background
3. Selenium checks BookMyShow periodically
4. When tickets become available:

   * An email notification is sent instantly
5. Monitoring stops after notification

---

## ▶️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bms-notifier.git
cd bms-notifier
```

### 2. Install dependencies

```bash
pip install flask flask-cors selenium webdriver-manager python-dotenv
```

### 3. Create `.env` file

Create a file named `.env` in the root directory and add:

```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

⚠️ Do NOT upload this file to GitHub

---

### 4. Run the application

```bash
python app.py
```

---

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## 💡 Example Use Case

Instead of manually refreshing BookMyShow for hours, this tool automatically monitors ticket availability and sends an email the moment bookings open—helping users grab tickets instantly.

---

## 🔮 Future Improvements

* 📱 SMS / WhatsApp notifications
* 🎯 More accurate ticket detection
* 🌍 Multi-city support
* 🖥️ Dashboard to manage active monitors
* ⏱️ Customizable check intervals

---

## ⚠️ Disclaimer

This project uses web automation for monitoring ticket availability and is intended for educational purposes only.

---

## 👨‍💻 Author

**Sathvik Narayana**
