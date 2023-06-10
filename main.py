from flask import Flask, render_template, session, redirect, url_for, request

from database.db_handler import register_user, login_user, create_connection, main

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # replace with your actual secret key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/appointment')
def appointment():
    if 'user' in session:
        return render_template('appointment_booking.html')
    else:
        return redirect(url_for('login'))

@app.route('/medical')
def medical():
    if 'user' in session:
        return render_template('medical_records.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        gender = request.form.get('gender')
        address = request.form.get('address')
        phone = request.form.get('phone')
        password = request.form.get('pwd')
        print(name,email,gender,address,phone,password)
        conn = create_connection()
        register_user(conn, (email, name, gender, address, phone, password))
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        conn = create_connection()
        user = login_user(conn, email, password)
        if user:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="* Invalid email or password")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    #main()  #uncomment only first time
    app.run(debug=True)
