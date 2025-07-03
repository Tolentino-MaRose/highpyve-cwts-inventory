from flask import Blueprint, request, jsonify
from database import query_db

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    required_fields = {'item_id', 'type', 'qty', 'date'}
    if not data or not required_fields.issubset(data):
        return jsonify({'error': 'Invalid input'}), 400
    
    if not isinstance(data['qty'], int):
        return jsonify({'error': 'Quantity must be an integer'}), 400

    item = query_db("SELECT * FROM Item WHERE item_id = ?",
                    (data['item_id'],), one=True)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    current_qty = item['quantity']
    qty = data['qty']

    if data['type'] == 'IN':
        new_qty = current_qty + qty
    elif data['type'] == 'OUT':
        if qty > current_qty:
            return jsonify({"error": "Not enough stock"}), 400
        new_qty = current_qty - qty
    else:
        return jsonify({"error": "Invalid type"}), 400

    query_db("INSERT INTO Log (item_id, type, qty, date) VALUES (?, ?, ?, ?)",
             (data['item_id'], data['type'], qty, data['date']))
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?",
             (new_qty, data['item_id']))

    return jsonify({"message": "Log recorded and inventory updated"}), 201

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = query_db("""
        SELECT Log.log_id, Item.name, Log.type, Log.qty, Log.date
        FROM Log JOIN Item ON Log.item_id = Item.item_id
        ORDER BY Log.date DESC
    """)
    return jsonify([dict(log) for log in logs])

@logs_bp.route('/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    data = request.get_json()
    required = {'item_id', 'type', 'qty', 'date'}
    if not data or not required.issubset(data):
        return jsonify({'error': 'Invalid input'}), 400
    
    if not isinstance(data['qty'], int):
        return jsonify({'error': 'Quantity must be an integer'}), 400

    old_log = query_db("SELECT * FROM Log WHERE log_id = ?", 
                       (log_id,), one=True)
    if not old_log:
        return jsonify({'error': 'Log not found'}), 404

    item = query_db("SELECT * FROM Item WHERE item_id = ?", 
                    (old_log['item_id'],), one=True)
    if not item:
        return jsonify({'error': 'Related item not found'}), 404

    current_qty = item['quantity']

    if old_log['type'] == 'IN':
        current_qty -= old_log['qty']
    elif old_log['type'] == 'OUT':
        current_qty += old_log['qty']

    new_type = data['type']
    new_qty = data['qty']

    if new_type == 'IN':
        current_qty += new_qty
    elif new_type == 'OUT':
        if new_qty > current_qty:
            return jsonify({'error': 'Not enough stock for update'}), 400
        current_qty -= new_qty
    else:
        return jsonify({'error': 'Invalid type'}), 400

    query_db(""" UPDATE Log SET item_id = ?, type = ?, qty = ?, date = ?
        WHERE log_id = ? """, 
        (data['item_id'], new_type, new_qty, data['date'], log_id))

    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?",
             (current_qty, old_log['item_id']))

    return jsonify({'message': 'Log fully updated and inventory adjusted'})

@logs_bp.route('/logs/<int:log_id>', methods=['PATCH'])
def patch_log(log_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    log = query_db("SELECT * FROM Log WHERE log_id = ?", (log_id,), one=True)
    if not log:
        return jsonify({'error': 'Log not found'}), 404

    item = query_db("SELECT * FROM Item WHERE item_id = ?", 
                    (log['item_id'],), one=True)
    if not item:
        return jsonify({'error': 'Related item not found'}), 404

    current_qty = item['quantity']

    if log['type'] == 'IN':
        current_qty -= log['qty']
    elif log['type'] == 'OUT':
        current_qty += log['qty']

    new_type = data.get('type', log['type'])
    new_qty = data.get('qty', log['qty'])
    new_date = data.get('date', log['date'])
    new_item_id = data.get('item_id', log['item_id'])

    if new_item_id != log['item_id']:
        return jsonify({'error': 'Changing item_id is not '
                        'supported in this patch'}), 400
    
    if not isinstance(new_qty, int):
        return jsonify({'error': 'Quantity must be an integer'}), 400

    if new_type == 'IN':
        current_qty += new_qty
    elif new_type == 'OUT':
        if new_qty > current_qty:
            return jsonify({'error': 'Not enough stock to apply update'}), 400
        current_qty -= new_qty
    else:
        return jsonify({'error': 'Invalid type'}), 400

    query_db(""" UPDATE Log SET type = ?, qty = ?, date = ? 
             WHERE log_id = ? """, (new_type, new_qty, new_date, log_id))

    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?",
             (current_qty, log['item_id']))

    return jsonify({'message': 'Log updated and inventory adjusted'})

@logs_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    log = query_db("SELECT * FROM Log WHERE log_id = ?", (log_id,), one=True)
    if not log:
        return jsonify({'error': 'Log not found'}), 404

    item = query_db("SELECT * FROM Item WHERE item_id = ?",
                    (log['item_id'],), one=True)
    if not item:
        return jsonify({'error': 'Related item not found'}), 404

    current_qty = item['quantity']

    if log['type'] == 'IN':
        current_qty -= log['qty']
    elif log['type'] == 'OUT':
        current_qty += log['qty']

    query_db("DELETE FROM Log WHERE log_id = ?", (log_id,))
    query_db("UPDATE Item SET quantity = ? WHERE item_id = ?",
             (current_qty, log['item_id']))

    return jsonify({"message": "Log deleted and inventory reverted"})
