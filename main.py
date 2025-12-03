from app import create_app
from app.data_loader import load_type_chart

if __name__ == '__main__':
    load_type_chart()

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)