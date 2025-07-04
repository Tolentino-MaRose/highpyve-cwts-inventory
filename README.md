# CWTS Inventory Management System

A lightweight, RESTful web application built using **Python**, **Flask**, and **SQLite** to manage inventory and track item logs for a CWTS (Civic Welfare Training Service) program. This project supports real-time API interactions and is deployed for web access.

---

## Live Demo

🔗 [Deployed Web App]: https://cwtsinventory.onrender.com 

---

## Features

- **Item Management**: Track inventory items with CRUD operations
- **Transaction Logs**: Record IN/OUT transactions with automatic inventory updates
- **RESTful Endpoints**: JSON-based API following REST conventions
- **Data Integrity**: Ensures inventory quantities are always consistent with transaction logs

---

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML
- **API**: Flask RESTful, JSON
- **Database**: SQLite 
- **Deployment**: Render

---

## API Endpoints

### Items
- `GET /items` - List all inventory items
- `POST /items` - Create a new item
- `PUT /items/<int:item_id>` - Fully update an item
- `PATCH /items/<int:item_id>` - Partially update an item
- `DELETE /items/<int:item_id>` - Delete an item

### Logs
- `GET /logs` - Get all transaction logs with item details
- `POST /logs` - Add a new transaction log (adjusts inventory automatically)
- `PUT /logs/<int:log_id>` - Fully update a log (adjusts inventory accordingly)
- `PATCH /logs/<int:log_id>` - Partially update a log (adjusts inventory)
- `DELETE /logs/<int:log_id>` - Delete a log (reverts inventory changes)

---

## Database Schema
The system uses SQLite with the following tables:

### Item
- `item_id` 
- `name`
- `description` 
- `quantity`

### Log
- `log_id` 
- `item_id` 
- `type` 
- `qty` 
- `date` 

## Project Structure:

```
cwts-inventory/
├── routes/
│   ├── __init__.py
│   ├── items.py
│   └── logs.py
├── templates/
│   ├── home.html
├── .gitignore
├── cwts_inventory.db
├── database.py
├── view_db.py
├── schema.sql
├── requirements.txt
├── Procfile
└── README.md
```

## Getting Started:

### 1. Clone the repository
```bash
git clone git@github.com:Tolentino-MaRose/highpyve-cwts-inventory.git
cd cwts-inventory
```
### 2. Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Run the app locally
```bash
python app.py
```