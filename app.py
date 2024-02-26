from flask import Flask, render_template, request, redirect, session
import pandas as pd
from GradeDistribution import GradeDistribution
import os
#import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management
users_data_file = "databases/users.csv"
grades_data_file = "databases/grades.csv"

# Read initial data from CSV
try:
    df = pd.read_csv(users_data_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["First Name", "Last Name", "Email", "Password"]) # , "Courses"
    df.to_csv(users_data_file, index=False)

grade_dist = GradeDistribution(grades_data_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register_user():
    global df
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Check if passwords match
    confirm_password = request.form['confirm_password']
    if password != confirm_password:
        error = "Passwords do not match. Please try again"
        return render_template('register.html', error=error)

    # Check if email already exists
    if email in df['Email'].values:
        error = "This email is already in use"
        return render_template('register.html', error=error)

    new_user = pd.DataFrame({'First Name': [first_name],
                            'Last Name': [last_name],
                            'Email': [email],
                            'Password': [password]})    #'Courses': {}
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(users_data_file, index=False)
    
    # Log the user in
    session['email'] = email
    return redirect('/profile')

@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if email and password match
        user = df[(df['Email'] == email) & (df['Password'] == password)]
        if user.empty:
            error = "Invalid username or password"
            return render_template('login.html', error=error)

        # Log the user in
        session['email'] = email
        return redirect('/profile')
    else:
        return render_template('login.html')

@app.route('/profile')
def profile():
    global df
    if 'email' not in session:
        return redirect('/login')

    email = session['email']
    user = df[df['Email'] == email]
    first_name = user['First Name'].iloc[0]
    last_name = user['Last Name'].iloc[0]

    # Retrieve the user's courses dictionary from DataFrame
    #courses_json_str = user['Courses'].iloc[0]
    #courses_dict = json.loads(courses_json_str) if not pd.isna(courses_json_str) else {}

    return render_template('profile.html', first_name=first_name, last_name=last_name) # , courses=courses_dict

#@app.route('/add_course', methods=['POST'])
#def add_course():
#    global df
#    if 'email' not in session:
#        return redirect('/login')
#
#    email = session['email']
#    course_dept = request.form['course_dept']
#    course_num = request.form['course_num']
#    role = request.form['role']
#    
#    # Construct the course key
#    course_key = f"{course_dept} {course_num}"
#    
#    # Retrieve the user's courses dictionary from DataFrame
#    courses_json_str = df[df['Email'] == email]['Courses'].iloc[0]
#    courses_dict = json.loads(courses_json_str) if not pd.isna(courses_json_str) else {}
#
#    # Add the new course and role to the dictionary
#    courses_dict[course_key] = role
#
#    # Update the DataFrame with the modified courses dictionary
#    df.loc[df['Email'] == email, 'Courses'] = json.dumps(courses_dict)
#    df.to_csv(users_data_file, index=False)
#
#    return redirect('/profile')

@app.route('/prof_search', methods=['GET', 'POST'])
def prof_search():
    return render_template('prof_search.html', ranked_profs=None)
    #if request.method == 'POST':
    #    course_dept = request.form['course_dept']
    #    course_num = request.form['course_num']
    #    course_data = grade_dist.search_class(course_dept, course_num)
    #    
    #    if not course_data.empty:
    #        ranked_profs = grade_dist.rank_profs(course_data)
    #        return render_template('prof_search.html', ranked_profs=ranked_profs)
    #else:
    #    return render_template('prof_search.html', ranked_profs=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
