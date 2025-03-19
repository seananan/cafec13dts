from flask import Flask, render_template, redirect, request, session
import sqlite3
from sqlite3 import Error

DATABASE = "C:/Users/21236/PycharmProjects/cafec13dts/DB_FILE"

app = Flask(__name__)

def connect_database(db_file):
    """
    creates a connection to the database
    :param db_file:
    :return: conn
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return

app.secret_key = 'secrets'

@app.route('/')
def render_homepage():  # put application's code here
    return render_template('home.html')



@app.route('/login',methods=['POST', 'GET'])
def render_login_page():  # put application's code here\
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('user_password1')
        con = connect_database(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT email, password  FROM user")
        all_emails = cur.fetchall()
        print(f"DEBUG: All emails in database: {all_emails}")
        query = "SELECT password, user_id, email FROM user WHERE email = ?"
        cur.execute(query,(email,))
        user_info = cur.fetchone()
        con.close()
        session["logged_in"] = True
        print(f"DEBUG: Entered email: {email}")  # Debugging email input
        print(f"DEBUG: Retrieved user_info: {user_info}")  # Debugging database result
        if user_info:
            stored_password = user_info[0]
            print(stored_password)
            print(user_info[0])
            print(password)
            if stored_password == password:
                session['user_id'] = user_info[1]
                session['email'] = user_info[2]
                return redirect("/")
            else:
                return redirect("/login?error=Incorrect+password")
        else:
            return redirect("/login?error=Account+not+found")
    return render_template('login.html')

@app.route('/menu/<cat_id>')
def render_menu(cat_id):
    con = connect_database(DATABASE)
    print("hello")
    query = "SELECT name, description, volume, image, price FROM product WHERE fk_cat_id = ?"
    query_cat_list = "SELECT * FROM category"
    cur = con.cursor()
    cur.execute(query, (cat_id,))
    product_list = cur.fetchall()
    cur.execute(query_cat_list)
    cat_list = cur.fetchall()
    print(product_list)
    print(cat_list)
    con.close()
    return render_template('menu.html', list_of_coffee=product_list, list_of_categories=cat_list)



@app.route('/signup',methods=['POST', 'GET'])
def render_signup_page():  # put application's code here
    if request.method =='POST':
        fname = request.form.get('user_fname').title().strip()
        lname = request.form.get('user_lname').title().strip()
        email = request.form.get('user_email').lower().strip()
        password1 = request.form.get('user_password1')
        password2 = request.form.get('user_password2')
        if password1 != password2:
            return redirect("\signup?error=passwords+do+not+match")
        if len(password1) < 8:
            return redirect("\signup?error=password+must+be+over+8+characters")
        else:
            session['logged_in = True']=True
            redirect('/')
        con = connect_database(DATABASE)
        querysean = "SELECT email FROM user"
        cur = con.cursor()
        cur.execute(querysean)
        all_emails = cur.fetchall()
        if (email,) in all_emails:
            return redirect("\signup?error=email+already+in+use")
        query_insert = "INSERT INTO user (first_name, surname, email, password) VALUES (?, ?, ?, ?)"
        cur.execute(query_insert, (fname, lname, email, password1))
        con.commit()
        con.close()
        session["logged_in"] = True
        return redirect("/home")
    return render_template('signup.html')




if __name__ == '__main__':
    app.run()
