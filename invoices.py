from flask import Blueprint, jsonify, request
from dbconfig import db_connect_cmd
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Blueprint setup
invoices_bp = Blueprint('invoices', __name__)

# Helper functions for validation
def validate_generate_invoice_data(data):
    if not isinstance(data.get('product_code'), str):
        return False
    if not isinstance(data.get('rate'), (int, float)) or data.get('rate') <= 0:
        return False
    if not isinstance(data.get('quantity'), int) or data.get('quantity') <= 0:
        return False
    return True

def validate_retrieve_invoices_data(data):
    if not isinstance(data.get('invoice_ids'), list):
        return False
    return all(isinstance(id, int) for id in data.get('invoice_ids'))

@invoices_bp.route('/generate', methods=['POST'])
@db_connect_cmd
def generate_invoice(cursor):
    data = request.get_json()
    
    # Validate input data
    if not validate_generate_invoice_data(data):
        return jsonify({'error': 'Invalid input'}), 400

    product_code = data['product_code']
    rate = data['rate']
    quantity = data['quantity']
    subtotal = rate * quantity
    gst = subtotal * 0.18
    discount = subtotal * 0.10 if subtotal > 5000 else 0
    total = subtotal - discount + gst

    try:
        # Use parameterized queries to prevent SQL injection
        cursor.execute("""
            INSERT INTO invoices (product_code, rate, quantity, subtotal, discount, gst, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (product_code, rate, quantity, subtotal, discount, gst, total))
        invoice_id = cursor.lastrowid
        response = {
            'invoice_id': invoice_id,
            'product_code': product_code,
            'rate': rate,
            'quantity': quantity,
            'subtotal': subtotal,
            'discount': discount,
            'gst': gst,
            'total': total
        }
        return jsonify(response), 201
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500

@invoices_bp.route('/retrieve', methods=['POST'])
@db_connect_cmd
def retrieve_invoices(cursor):
    data = request.get_json()
    
    # Validate input data
    if not validate_retrieve_invoices_data(data):
        return jsonify({'error': 'Invalid input'}), 400

    invoice_ids = data['invoice_ids']
    results = []
    try:
        for invoice_id in invoice_ids:
            cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
            invoice = cursor.fetchone()
            if invoice:
                results.append({
                    'invoice_id': invoice[0],
                    'product_code': invoice[1],
                    'rate': invoice[2],
                    'quantity': invoice[3],
                    'subtotal': invoice[4],
                    'discount': invoice[5],
                    'gst': invoice[6],
                    'total': invoice[7]
                })
        return jsonify(results), 200
    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500

# from flask import Blueprint, jsonify, request
# from dbconfig import db_connect_cmd
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Blueprint setup
# invoices_bp = Blueprint('invoices', __name__)

# @invoices_bp.route('/generate', methods=['POST'])
# @db_connect_cmd
# def generate_invoice(cursor):
#     data = request.get_json()
#     product_code = data.get('product_code')
#     rate = data.get('rate')
#     quantity = data.get('quantity')

#     # Validate inputs
#     if not product_code or not isinstance(rate, (int, float)) or not isinstance(quantity, int):
#         return jsonify({'error': 'Invalid input'}), 400

#     subtotal = rate * quantity
#     gst = subtotal * 0.18
#     discount = 0

#     if subtotal > 5000:
#         discount = subtotal * 0.10

#     total = subtotal - discount + gst

#     try:
#         # Use parameterized queries to prevent SQL injection
#         cursor.execute("""
#             INSERT INTO invoices (product_code, rate, quantity, subtotal, discount, gst, total)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (product_code, rate, quantity, subtotal, discount, gst, total))
#         invoice_id = cursor.lastrowid
#         response = {
#             'invoice_id': invoice_id,
#             'product_code': product_code,
#             'rate': rate,
#             'quantity': quantity,
#             'subtotal': subtotal,
#             'discount': discount,
#             'gst': gst,
#             'total': total
#         }
#         return jsonify(response), 201
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500

# @invoices_bp.route('/retrieve', methods=['POST'])
# @db_connect_cmd
# def retrieve_invoices(cursor):
#     data = request.get_json()
#     invoice_ids = data.get('invoice_ids')

#     # Validate inputs
#     if not isinstance(invoice_ids, list) or not all(isinstance(id, int) for id in invoice_ids):
#         return jsonify({'error': 'Invalid input'}), 400

#     results = []
#     try:
#         for invoice_id in invoice_ids:
#             cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
#             invoice = cursor.fetchone()
#             if invoice:
#                 results.append({
#                     'invoice_id': invoice[0],
#                     'product_code': invoice[1],
#                     'rate': invoice[2],
#                     'quantity': invoice[3],
#                     'subtotal': invoice[4],
#                     'discount': invoice[5],
#                     'gst': invoice[6],
#                     'total': invoice[7]
#                 })
#         return jsonify(results), 200
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500

# from flask import Blueprint, jsonify, request
# from dbconfig import db_connect_cmd
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Blueprint setup
# invoices_bp = Blueprint('invoices', __name__)

# from flask import Blueprint, jsonify, request
# from dbconfig import db_connect_cmd
# import logging

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Blueprint setup
# invoices_bp = Blueprint('invoices', __name__)

# @invoices_bp.route('/generate', methods=['POST'])
# @db_connect_cmd
# def generate_invoice(cursor):
#     data = request.get_json()
#     product_code = data.get('product_code')
#     rate = data.get('rate')
#     quantity = data.get('quantity')

#     if not product_code or not isinstance(rate, (int, float)) or not isinstance(quantity, int):
#         return jsonify({'error': 'Invalid input'}), 400

#     subtotal = rate * quantity
#     gst = subtotal * 0.18
#     discount = 0

#     if subtotal > 5000:
#         discount = subtotal * 0.10

#     total = subtotal - discount + gst

#     try:
#         cursor.execute("""
#             INSERT INTO invoices (product_code, rate, quantity, subtotal, discount, gst, total)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (product_code, rate, quantity, subtotal, discount, gst, total))
#         invoice_id = cursor.lastrowid
#         response = {
#             'invoice_id': invoice_id,
#             'product_code': product_code,
#             'rate': rate,
#             'quantity': quantity,
#             'subtotal': subtotal,
#             'discount': discount,
#             'gst': gst,
#             'total': total
#         }
#         return jsonify(response), 201
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500

# # @invoices_bp.route('/generate', methods=['POST'])
# # @db_connect_cmd
# # def generate_invoice(cursor):
#     data = request.get_json()
#     product_code = data.get('product_code')
#     rate = data.get('rate')
#     quantity = data.get('quantity')

#     if not product_code or not isinstance(rate, (int, float)) or not isinstance(quantity, (int, float)):
#         return jsonify({'error': 'Invalid input'}), 400

#     subtotal = rate * quantity
#     gst = subtotal * 0.18
#     discount = 0

#     if subtotal > 5000:
#         discount = subtotal * 0.10

#     total = subtotal - discount + gst

#     try:
#         cursor.execute("""
#             INSERT INTO invoices (product_code, rate, quantity, subtotal, discount, gst, total)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (product_code, rate, quantity, subtotal, discount, gst, total))
#         invoice_id = cursor.lastrowid
#         response = {
#             'invoice_id': invoice_id,
#             'product_code': product_code,
#             'rate': rate,
#             'quantity': quantity,
#             'subtotal': subtotal,
#             'discount': discount,
#             'gst': gst,
#             'total': total
#         }
#         return jsonify(response), 201
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500

# # @invoices_bp.route('/retrieve', methods=['POST'])
# # @db_connect_cmd
# # def retrieve_invoices(cursor):
#     data = request.get_json()
#     invoice_ids = data.get('invoice_ids')

#     if not isinstance(invoice_ids, list):
#         return jsonify({'error': 'Invalid input'}), 400

#     results = []
#     try:
#         for invoice_id in invoice_ids:
#             cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
#             invoice = cursor.fetchone()
#             if invoice:
#                 results.append({
#                     'invoice_id': invoice[0],
#                     'product_code': invoice[1],
#                     'rate': invoice[2],
#                     'quantity': invoice[3],
#                     'subtotal': invoice[4],
#                     'discount': invoice[5],
#                     'gst': invoice[6],
#                     'total': invoice[7]
#                 })
#         return jsonify(results), 200
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500


# @invoices_bp.route('/retrieve', methods=['POST'])
# @db_connect_cmd
# def retrieve_invoices(cursor):
#     data = request.get_json()
#     invoice_ids = data.get('invoice_ids')

#     if not isinstance(invoice_ids, list):
#         return jsonify({'error': 'Invalid input'}), 400

#     results = []
#     try:
#         for invoice_id in invoice_ids:
#             cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))
#             invoice = cursor.fetchone()
#             if invoice:
#                 results.append({
#                     'invoice_id': invoice[0],
#                     'product_code': invoice[1],
#                     'rate': invoice[2],
#                     'quantity': invoice[3],
#                     'subtotal': invoice[4],
#                     'discount': invoice[5],
#                     'gst': invoice[6],
#                     'total': invoice[7]
#                 })
#         return jsonify(results), 200
#     except Exception as e:
#         logging.error(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database error occurred'}), 500