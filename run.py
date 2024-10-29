from app import create_app

app = create_app()

def my_custom_filter(value):
    return value  # Modifica la lógica según sea necesario


if __name__ == '__main__':
    app.run(debug=True)







     