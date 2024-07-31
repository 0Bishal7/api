from flask import Flask, jsonify
from flask_cors import CORS
# If create_app is in a different file or module, adjust the import statement
# from some_module import create_app

app = Flask(__name__)
CORS(app)
# from your_module import invoices_bp  # Ensure correct import

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(invoices_bp, url_prefix='/api')  # Register blueprint with a prefix
#     return app


def create_app():
    app = Flask(__name__)

    @app.route('/api/generate', methods=['POST'])
    def generate_invoice():
        # Your implementation here
        pass

    @app.route('/api/retrieve', methods=['POST'])
    def retrieve_invoices():
        # Your implementation here
        pass

    return app



from invoices import invoices_bp

app.register_blueprint(invoices_bp, url_prefix="/api/invoices")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(invoices_bp, url_prefix='/api')  # Register blueprint with a prefix
    return app















if __name__ == '__main__':
    app.run(port=7452, debug=True)
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# from invoices import invoices_bp

# app.register_blueprint(invoices_bp, url_prefix="/api/invoices")

# if __name__ == '__main__':
#     app.run(port=7452, debug=True)
