# Invoice API

A RESTful API built with Flask for managing invoices. This API allows you to generate and retrieve invoices. It includes endpoints for creating new invoices and retrieving existing ones by their IDs.

## Features

- **Generate Invoice**: Create new invoices with product details and automatically calculate totals, GST, and discounts.
- **Retrieve Invoices**: Retrieve details of invoices by their IDs.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/invoice-api.git
    cd invoice-api
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Configure Database**: Update `dbconfig.py` with your database connection details.

6. **Set Up Environment Variables**: Ensure any necessary environment variables are set. You can use a `.env` file for this.

## Usage

1. **Run the Application**:
    ```bash
    python main.py
    ```

   The application will start on `http://localhost:7452`.

## API Endpoints

### Generate Invoice

- **URL**: `/api/invoices/generate`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "product_code": "XYZ789",
        "rate": 200.0,
        "quantity": 5
    }
    ```
- **Response**:
    ```json
    {
        "invoice_id": 1,
        "product_code": "XYZ789",
        "rate": 200.0,
        "quantity": 5,
        "subtotal": 1000.0,
        "discount": 100.0,
        "gst": 162.0,
        "total": 1062.0
    }
    ```
- **Status Codes**:
  - `201 Created`: Invoice successfully created.
  - `400 Bad Request`: Invalid input data.
  - `500 Internal Server Error`: Database error.

### Retrieve Invoices

- **URL**: `/api/invoices/retrieve`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "invoice_ids": [1]
    }
    ```
- **Response**:
    ```json
    [
        {
            "invoice_id": 1,
            "product_code": "XYZ789",
            "rate": 200.0,
            "quantity": 5,
            "subtotal": 1000.0,
            "discount": 100.0,
            "gst": 162.0,
            "total": 1062.0
        }
    ]
    ```
- **Status Codes**:
  - `200 OK`: Successfully retrieved invoices.
  - `400 Bad Request`: Invalid input data.

## Testing

1. **Run Tests**:
    ```bash
    pytest
    ```

   Ensure that all tests pass before deploying.

## Security

- **SQL Injection Protection**: Parameterized queries are used to prevent SQL injection.
- **Data Validation**: Inputs are validated and sanitized to prevent vulnerabilities.
- **Authentication & Authorization**: Consider implementing authentication (e.g., API keys, OAuth) and authorization mechanisms as needed.

## Compliance

- **Data Privacy**: Ensure compliance with data protection regulations such as GDPR or CCPA.
- **Standards**: Follow industry standards for API design and implementation, including RESTful principles.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

