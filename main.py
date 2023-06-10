from flask import Flask, render_template, session, redirect, url_for, request

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
    if 'logged_in' in session:
        return render_template('appointment_booking.html')
    else:
        return redirect(url_for('login'))

@app.route('/medical')
def medical():
    if 'logged_in' in session:
        return render_template('medical_records.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'logged_in' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # your registration logic here
        pass
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # your authentication logic here
        session['logged_in'] = True
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
