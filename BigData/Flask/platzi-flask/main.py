from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    #Obtiene la ip del usuario
    user_ip = request.remote_addr
    return 'Hello World Flask, tu IP es {}'.format(user_ip)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)