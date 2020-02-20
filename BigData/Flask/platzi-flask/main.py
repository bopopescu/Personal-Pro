from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY']='SUPER SECRETO'
bootstrap=Bootstrap(app)

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video a producto']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def not_fount(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip']=user_ip
    return response

@app.route('/hello', methods =['GET','POST'])
def hello():
    #Obtiene la ip del usuario desde la cookie
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    
    context = {
        'user_ip' : user_ip, 
        'todos' : todos,
        'login_form' : login_form,
        'username' : username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con éxito!')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)