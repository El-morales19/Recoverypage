import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template_string(open('index.html').read())

# Ruta para recibir el formulario y enviar el correo
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']

    # Obtener la API key desde las variables de entorno
    api_key = os.getenv('API_KEY')  # La variable de entorno debe llamarse 'API_KEY'
    
    if not api_key:
        return "Error: API key is not set in environment variables", 500

    # Enviar correo usando la API de Mailgun
    try:
        send_simple_message(name, email, api_key)
        return "Correo enviado correctamente"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}", 500

def send_simple_message(name, email, api_key):
    domain = 'sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org'
    url = f"https://api.mailgun.net/v3/{domain}/messages"

    data = {
        "from": "Mailgun Sandbox <postmaster@sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org>",
        "to": f"{name} <{email}>",
        "subject": f"Hello {name}",
        "template": "you've been compromised",  # Aquí usamos la plantilla "you've been compromised"
        "h:X-Mailgun-Variables": f'{{"name": "{name}", "email": "{email}"}}'
    }

    response = requests.post(
        url,
        auth=("api", api_key),
        data=data
    )

    if response.status_code != 200:
        raise Exception(f"Mailgun API error: {response.text}")
    
    print(response.text)  # Puedes imprimir la respuesta para depuración

if __name__ == '__main__':
    app.run(debug=True)
