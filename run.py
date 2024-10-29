from app import create_app
from datetime import datetime

app = create_app()

def my_custom_filter(value):
    return value  # Modifica la lógica según sea necesario

@app.add_template_filter
def to_datetime(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d')

if __name__ == '__main__':
    app.run(debug=True)







     