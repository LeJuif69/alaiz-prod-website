from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Load environment variables
load_dotenv()

# Initialize Sentry if DSN is provided
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/alaiz_prod.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('A Laiz Prod startup')

@app.route('/')
def index():
    # Pass all environment variables to template
    context = {
        'director_phone': os.getenv('DIRECTOR_PHONE', '+237682180266'),
        'director_email': os.getenv('DIRECTOR_EMAIL', 'herve@alaizprod.com'),
        'contact_email': os.getenv('CONTACT_EMAIL', 'contact@alaizprod.com'),
        'booking_email': os.getenv('BOOKING_EMAIL', 'booking@alaizprod.com'),
        'facebook_url': os.getenv('FACEBOOK_URL', 'https://facebook.com/alaizprod'),
        'instagram_url': os.getenv('INSTAGRAM_URL', 'https://instagram.com/alaizprod'),
        'youtube_url': os.getenv('YOUTUBE_URL', 'https://youtube.com/alaizprodlabel'),
        'linkedin_url': os.getenv('LINKEDIN_URL', 'https://linkedin.com/in/hervenanfang'),
        'whatsapp_url': os.getenv('WHATSAPP_URL', 'https://wa.me/237694723492'),
        'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', ''),
        'facebook_pixel_id': os.getenv('FACEBOOK_PIXEL_ID', ''),
    }
    return render_template('index.html', **context)

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
            
            # Send email
            send_contact_email(name, email, message)
            
            # Log the contact form submission
            app.logger.info(f'Nouveau message de {name} ({email})')
            
            return jsonify({'success': True, 'message': 'Merci pour votre message! Nous vous contacterons bientôt.'})
        
        except Exception as e:
            app.logger.error(f'Erreur lors de l\'envoi du message: {str(e)}')
            return jsonify({'success': False, 'message': 'Une erreur s\'est produite. Veuillez réessayer.'})

def send_contact_email(name, email, message):
    """Send contact form submission via email"""
    # Use environment variables for email configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME', os.getenv('EMAIL_USER', ''))
    smtp_password = os.getenv('SMTP_PASSWORD', os.getenv('EMAIL_PASS', ''))
    
    # Get recipient email from environment or use default
    recipient_email = os.getenv('CONTACT_EMAIL', 'contact@alaizprod.com')
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Reply-To'] = email
    msg['Subject'] = f'Nouveau message de {name} - Site A Laiz Prod'
    
    body = f"""
    Nouveau message depuis le site A Laiz Prod:
    
    Nom: {name}
    Email: {email}
    
    Message:
    {message}
    
    ---
    Cet email a été envoyé automatiquement depuis le formulaire de contact du site.
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=port)
