from flask import Flask, render_template, session, redirect, url_for, request

from database.db_handler import get_appointments_for_user, get_patient_details, register_user, login_user, create_connection, main,add_appointment, get_all_doctors

from flask_mail import Mail, Message
import random
import string



app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # replace with your actual secret key
#mail server config

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'emailsender039@gmail.com'  # your email
app.config['MAIL_PASSWORD'] = 'bfkmsxirmpmonzim'  # your email password
mail = Mail(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if 'user' in session:
        conn = create_connection()
        doctors = get_all_doctors()
        message = ""
        if request.method == 'POST':
            doctor_id = request.form.get('doctor')
            date_time = request.form.get('datetime')

            if not doctor_id or not date_time:
                message = "Please fill in all fields."
            else:
                added = add_appointment(conn, (doctor_id, session['user'], date_time))
                if added:
                    return redirect(url_for('home'))
                else:
                    message = "Failed to book appointment. Please try again."

        return render_template('appointment_booking.html', doctors=doctors, message=message)
    else:
        return redirect(url_for('login'))

@app.route('/medical', methods=['GET'])
def medical():
    if 'user' in session:
        conn = create_connection()
        print(session['user'])
        appointments = get_appointments_for_user(conn, session['user'])
        return render_template('medical_records.html', appointments=appointments)
    else:
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET'])
def profile():
    if 'user' in session:
        conn = create_connection()
        user_details = get_patient_details(conn, session['user'])
        return render_template('profile.html', user=user_details)
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
        if register_user(conn, (email, name, gender, address, phone, password)) != None:
            
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message="User already exits!!")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pwd')
        conn = create_connection()
        user = login_user(conn, email, password)
        if user:
            # generate a random string
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            session['code'] = code
            session['user-temp'] = email

            # send the code to the user's email
            msg = Message('Your verification code', sender='emailsender039@gmail.com', recipients=[email])
            msg.body = f'Your verification code is {code}'
            mail.send(msg)

            return render_template('verify.html')
        else:
            return render_template('login.html', message="* Invalid email or password")

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_code = request.form.get('code')
        print("User entered ",user_code)
        print("Code in session ",session['code'])
        if 'code' in session and user_code == session['code']:
            session['user'] = session['user-temp'] 
            return redirect(url_for('home'))
        else:
            return render_template('verify.html', message='* Invalid code')
    return render_template('verify.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    #main()  #uncomment only first time
    app.run(debug=True)
