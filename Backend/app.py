from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
import logging
import re  # Import regex for URL validation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String, unique=True, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

# Create the database tables within an application context
with app.app_context():
    db.create_all()

@app.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.path}")

@app.route('/')
def home():
    return "Welcome to the URL Shortener Microservice!"

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/shorturls', methods=['POST'])
def create_short_url():
    data = request.json
    original_url = data.get('url')
    
    # Validate URL
    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    validity = data.get('validity', 30)  # Default to 30 minutes
    shortcode = data.get('shortcode', str(uuid.uuid4())[:6])  # Generate a unique shortcode

    # Check for uniqueness of shortcode
    if URLMapping.query.filter_by(short_code=shortcode).first():
        return jsonify({"error": "Shortcode already exists"}), 400

    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=validity)
    new_url = URLMapping(original_url=original_url, short_code=shortcode, expiry=expiry_time)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        "shortLink": f"http://localhost:5000/{shortcode}",
        "expiry": expiry_time.isoformat()
    }), 201

@app.route('/<shortcode>', methods=['GET'])
def redirect_to_url(shortcode):
    url_mapping = URLMapping.query.filter_by(short_code=shortcode).first()
    if url_mapping and url_mapping.expiry > datetime.datetime.utcnow():
        return redirect(url_mapping.original_url)
    return jsonify({"error": "URL not found or expired"}), 404

@app.route('/shorturls/<shortcode>', methods=['GET'])
def get_url_stats(shortcode):
    url_mapping = URLMapping.query.filter_by(short_code=shortcode).first()
    if url_mapping:
        return jsonify({
            "clicks": 0,  # Implement click tracking if needed
            "originalURL": url_mapping.original_url,
            "createdAt": url_mapping.expiry,
            "expiry": url_mapping.expiry.isoformat(),
            "clickDetails": []  # Implement click details if needed
        })
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
