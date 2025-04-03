from app import run_app

app = run_app()

if __name__ == "__main__":
    app.run_server(debug=True, port=5000)