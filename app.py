from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET','POST'])
def home():
    short_url = None

    if request.method == 'POST':
        original_url = request.form['url']
        code = generate_code()

        new_url = URL(original_url=original_url, short_code=code)
        db.session.add(new_url)
        db.session.commit()

        short_url = request.host_url + code

    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first()

    if url:
        return redirect(url.original_url)

    return "URL Not Found"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)