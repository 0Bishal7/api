import pytest
from flask.testing import FlaskClient
import json

@pytest.fixture
def app():
    from main import create_app  # Adjust import based on your app's structure
    app = create_app()
    yield app

@pytest.fixture
def client(app: FlaskClient):
    return app.test_client()

def test_generate_invoice(client: FlaskClient):
    response = client.post('/api/generate', 
        data=json.dumps({
            'product_code': 'XYZ789',
            'rate': 200.0,
            'quantity': 5
        }), 
        content_type='application/json'
    )
    assert response.status_code == 201
    assert 'invoice_id' in response.json

def test_retrieve_invoices(client: FlaskClient):
    # Generate an invoice first
    generate_response = client.post('/api/generate', 
        data=json.dumps({
            'product_code': 'XYZ789',
            'rate': 200.0,
            'quantity': 5
        }), 
        content_type='application/json'
    )
    invoice_id = generate_response.json.get('invoice_id')

    # Retrieve the invoice
    response = client.post('/api/retrieve',
        data=json.dumps({
            'invoice_ids': [invoice_id]
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['invoice_id'] == invoice_id

def test_generate_invoice_invalid_input(client: FlaskClient):
    response = client.post('/api/generate',
        data=json.dumps({
            'product_code': 'XYZ789',
            'rate': 'invalid_rate',  # Invalid rate type
            'quantity': 5
        }),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_retrieve_invoices_invalid_ids(client: FlaskClient):
    response = client.post('/api/retrieve',
        data=json.dumps({
            'invoice_ids': [9999999]  # ID that does not exist
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert len(response.json) == 0  # No invoice should be retrieved

def test_retrieve_invoices_invalid_input(client: FlaskClient):
    response = client.post('/api/retrieve',
        data=json.dumps({
            'invoice_ids': 'invalid_ids'  # Invalid ids type
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
