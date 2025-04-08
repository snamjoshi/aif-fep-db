from app import run_app

# TODO: Import config TOML file with database path
db_path = "/app/data/databases/database__2025-03-21__17:12:35.196730.pkl"
app = run_app(db_path)

if __name__ == "__main__":
    app.run_server(debug=True, port=5000)
