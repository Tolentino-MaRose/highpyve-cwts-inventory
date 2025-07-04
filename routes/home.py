from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return jsonify(
    {
        "title": "CWTS Inventory System API",
        "description": "A REST API to manage inventory items used for "
                            "CWTS activities.",
        "URL":
        {
            "empty" : "empty"
        },
        "endpoints": 
        {
            "items" :
            {
                "/items": "GET all inventory items",
                "/items/<id>": "GET, PUT, DELETE item by ID",
            },
            "logs":
            {
                "/logs": "GET all inventory items",
                "/logs/<id>": "GET, PUT, DELETE item by ID",
            }
        },
        "example_item_response": 
        {
            "id": 1,
            "name": "Broom",
            "category": "Cleaning Supplies",
            "quantity": 10,
        },
        "example_log_response": 
        {
            "date": "2025-07-03",
            "log_id": 1,
            "name": "Dust Pan (Pangdakot)",
            "qty": 5,
            "type": "OUT"
        }
    })