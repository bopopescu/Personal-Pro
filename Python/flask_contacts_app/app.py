from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL connection
app.config['MYSQL_HOST'] = 'be6v5hba1kumyfvusyeb-mysql.services.clever-cloud.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'ucv6dyydm7ziyttq'
app.config['MYSQL_PASSWORD'] = 'VDnUMuRPNYN1GqzQYxPT'
app.config['MYSQL_DB'] = 'be6v5hba1kumyfvusyeb'
mysql = MySQL(app)

#Setting

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data) 

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
        return redirect(url_for('index'))

@app.route('/edit/<string:contact_id>')
def get_contact(contact_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE contact_id LIKE %s" , [contact_id])
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<contact_id>', methods = ['POST'])
def update_contact(contact_id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE contact_id = %s
        """, (fullname, email, phone, contact_id ))
        mysql.connection.commit()
        flash('Contact Updated  Successfully')
        return redirect(url_for('index'))

@app.route('/delete/<string:contact_id>')
def delete_contact(contact_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE contact_id = {0}'.format(contact_id))
    mysql.connection.commit()
    flash('Contact Removed Succesfully')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port = 3000, debug = True)