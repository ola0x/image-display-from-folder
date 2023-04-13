from waitress import serve
from app import app

host = '0.0.0.0'
port = 8000

print(f"Starting server on http://{host}:{port}")
serve(app, host=host, port=port)
