import os
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/change_password', methods=['POST'])
def change_password():
    name = request.form['name']
    email = request.form['email']
    new_password = request.form['new-password']
    confirm_password = request.form['confirm-password']

    if new_password != confirm_password:
        return "Error: Passwords do not match", 400

    # Obtener la API key de Mailgun desde las variables de entorno
    api_key = os.getenv('API_KEY')
    if not api_key:
        return "Error: Mailgun API key is not set", 500

    try:
        send_mailgun_email(name, email, api_key)
        return "Password change request submitted successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}", 500

def send_mailgun_email(name, email, api_key):
    domain = "sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org"
    url = f"https://api.mailgun.net/v3/{domain}/messages"

    data = {
        "from": "Mailgun Sandbox <postmaster@sandbox4d2c52cdc8d14e8d926da2f43fac381f.mailgun.org>",
        "to": f"{name} <{email}>",
        "subject": "Password Change Request",
        "template": "you've been compromised",
        "h:X-Mailgun-Variables": f'{{"name": "{name}", "email": "{email}"}}'
    }

    response = requests.post(
        url,
        auth=("api", api_key),
        data=data
    )

    if response.status_code != 200:
        raise Exception(f"Mailgun API error: {response.text}")

if __name__ == '__main__':
    app.run(debug=True)
