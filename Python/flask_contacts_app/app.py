from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

#Setting

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template('index.html') 

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()

        cur.execute("""
        INSERT INTO contacts(`fullname`, `phone`, `email`)
            VALUES(%s,%s,%s)
        """,(fullname,phone, email))

        mysql.connection.commit()
        flash(f'El contacto {fullname} fue agregado')

        print(f'Nombre: {fullname}\nPhone: {phone}\nEmail: {email}')
        return redirect(url_for('Index'))

@app.route('/edit')
def edit_contact():
    return 'Edit contact'

@app.route('/delete')
def delete_contact():
    return 'Delete Contact'

if __name__ == '__main__':
    app.run(port = 3000, debug = True)