from functools import wraps
from config import connectDB
from flask import jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def db_connect_cmd(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        cursor = None
        try:
            conn = connectDB()
            if conn is None:
                logging.error("Failed to establish database connection.")
                return jsonify({'error': 'Database connection failed'}), 500
            cursor = conn.cursor()
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}")
            if conn:
                conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    return wrapper
