from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY']='SUPER SECRETO'
bootstrap=Bootstrap(app)

todos = ['Comprar café', 'Enviar solicitud de compra', 'Entregar video a producto']

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

@app.route('/hello')
def hello():
    #Obtiene la ip del usuario desde la cookie
    user_ip = session.get('user_ip')
    context = {
        'user_ip' : user_ip, 
        'todos' : todos
    }
    return render_template('hello.html', **context)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)