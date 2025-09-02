from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-temp')

# Test minimal - juste pour voir si l'app démarre
@app.route('/')
def test_index():
    return "<h1>Test A Laiz Prod</h1><p>Si vous voyez ceci, l'app fonctionne</p>"

@app.route('/debug')
def debug():
    return {
        'status': 'OK',
        'templates_folder': app.template_folder,
        'static_folder': app.static_folder
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
