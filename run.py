from app import create_app
import requests
from flask import jsonify

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)







     