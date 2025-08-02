# Car Zone — Used Car Selling Website

**Course:** Project Work II
**Semester:** 6th (Spring 2023)
**Session:** Spring 2025

---

## **Group Members**

* **Rayhan Aziz Chowdhury Shafi** — *0562310005101007*
* **Fatematuj Johura Mim** — *0562310005101032*

---

## **Project Overview**

Car Zone is a web-based platform for buying and selling used cars. Sellers can register, list cars with details and images, and manage their listings. Buyers can browse available cars, filter results, view details, and contact sellers. An admin panel provides basic user and listing management.

---

## **Monorepo Structure**

This repository contains both **frontend** and **backend** projects in one place:

```
car-zone/
├── frontend/
├── backend/
```

---

## **Technology Stack**

* **Frontend:** React.js, Tailwind CSS
* **Backend:** Python, Django
* **Database:** SQLite (for development)

---

## **Getting Started**

### **1. Clone the Repository**

```bash
git clone https://github.com/r-shafi/car-zone.git
cd car-zone
```

---

### **2. Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

* Runs the React development server.
* Accessible at `http://localhost:8080`.

---

### **3. Backend Setup**

```bash
cd backend
python -m venv env
source env/bin/activate  # For Linux/macOS
# OR
env\Scripts\activate     # For Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

* Runs Django backend server.
* Accessible at `http://localhost:8000`.

---

## **Key Features**

* User Registration & Login
* Add/Edit/Delete Car Listings
* Search & Filter Cars
* Contact Seller Form
* Admin Panel for user & listing management

---

## **Development Notes**

* The project uses a simple SQLite database for easy setup.
* Image uploads are stored locally during development.
