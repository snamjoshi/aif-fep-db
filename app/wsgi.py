import os

from app import run_app

db_path = os.environ.get("DB_PATH")
app = run_app(db_path)

if __name__ == "__main__":
    app.run_server(debug=True, port=5000)
