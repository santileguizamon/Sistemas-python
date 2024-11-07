from app import create_app
import requests
from flask import jsonify

app = create_app()

def my_custom_filter(value):
    return value  

app.template_filter()(my_custom_filter)

if __name__ == '__main__':
    app.run(debug=True)







     