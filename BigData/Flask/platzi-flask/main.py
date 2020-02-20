from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap

import unittest

from app import create_app
from app.forms import LoginForm


import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

app = create_app()

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video a producto']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

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