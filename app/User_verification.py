from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" methods="POST"><input name="email"><input type="submit">'

    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='CatchUp.notes@gmail.com', recipients=[email])

    link = url_for('confirm_email', token = token, _external=True)
    
    msg.body = 'your link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The Token is {}</h1>'.format(email)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt = 'email-confirm', max_age=60)
    except SignatureExpired: 
        return 'The token is expired'
    except SyntaxError:
        return 'Wrong token value'
    return 'the token works '

if __name__ == "__main__":
    app.run(debug=True)