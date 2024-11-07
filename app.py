from app import create_app
from datetime import datetime

app = create_app()

def my_custom_filter(value):
    return value  

@app.template_filter()
def to_datetime(timestamp):
    """Convert Unix timestamp to a readable date format."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

if __name__ == '__main__':
    app.run(debug=True)







     