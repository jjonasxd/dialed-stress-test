from app import create_app, run_app

if __name__ == '__main__':
    app = create_app(debug=False)
    run_app(app)