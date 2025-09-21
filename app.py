from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # Basic validation
            if not name or not email or not message:
                return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires.'})
            
            # Send email (you'll need to configure your email settings)
            send_contact_email(name, email, message)
            
            return jsonify({'success': True, 'message': 'Merci pour votre message! Nous vous contacterons bientôt.'})
        
        except Exception as e:
            return jsonify({'success': False, 'message': 'Une erreur s\'est produite. Veuillez réessayer.'})

def send_contact_email(name, email, message):
    """Send contact form submission via email"""
    # Configure your email settings here
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = 'contact@alaizprod.com'  # Your receiving email
    msg['Subject'] = f'Nouveau message de {name}'
    
    body = f"""
    Nom: {name}
    Email: {email}
    Message:
    {message}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
