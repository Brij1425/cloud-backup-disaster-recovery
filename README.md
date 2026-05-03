# cloud-backup-disaster-recovery
Cloud-Based Automated Backup and Disaster Recovery System

# Cloud-Based Backup & Disaster Recovery System

## 📌 Overview
This project is a cloud-based backup and disaster recovery system developed using Flask and Supabase. It ensures secure data storage and recovery in case of failure.

## 🚀 Features
- User Registration & Login
- Secure Password Hashing
- File Upload & Backup
- File Restore & Delete
- Admin Panel for Monitoring
- Cloud Database Integration (Supabase)

## 🏗️ Architecture
User → Flask App → Supabase (Cloud DB)
                 → Local Storage (Files)

## 🛠️ Tech Stack
- Python (Flask)
- HTML, CSS
- Supabase (Cloud DB)
- REST API

## ▶️ How to Run
```bash
pip install flask requests
python app.py

---
cloud-backup-project/
│
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
