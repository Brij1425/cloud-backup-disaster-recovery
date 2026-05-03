# cloud-backup-disaster-recovery
Cloud-Based Automated Backup and Disaster Recovery System

# Cloud-Based Backup & Disaster Recovery System

## 📌 Overview
This project is a cloud-based backup and disaster recovery system developed using Flask and Supabase. It ensures secure data storage and recovery in case of failure.

It combines:
- 🌐 Cloud database (Supabase)
- 💻 Local backup storage
- 🔐 Secure authentication

## 🚀 Features
- 🔐 User Registration & Login (Password Hashing)
- ☁️ Cloud Database Integration (Supabase)
- 📤 File Upload & Backup
- 🔄 File Restore & Recovery
- 🗑️ File Delete Functionality
- 👨‍💻 Admin Panel (User & File Control)
- 🔍 Search & Organized Dashboard


## 🏗️ Architecture
User → Flask App → Supabase (Cloud DB)
                 → Local Storage (Files)

## 🛠️ Tech Stack
- Python (Flask)
- HTML, CSS
- Supabase (Cloud DB)
- REST API

---
## 📁 Project Structure
cloud-backup-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── admin.html

## ▶️ How to Run
```bash/ CMD
git clone https://github.com/YOUR_USERNAME/cloud-backup-disaster-recovery.git
cd cloud-backup-disaster-recovery
pip install -r requirements.txt
python app.py

👨‍💻 Author
Brijnath Mandal
