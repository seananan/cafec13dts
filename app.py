from flask import Flask, render_template
import sqlite3
from sqlite3 import ERROR

DATABASE = "DB_FILE"

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



@app.route('/')
def render_homepage():  # put application's code here
    return render_template('home.html')


@app.route('/menu')
def render_menu():
    con = create_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products"
    cur = con.cursor()
    cur.execute(query)
    product_list = cur.fetchall()
    print(product_list)
    con.close()
    return render_template('menu.html', list_of_coffee=product_list)


if __name__ == '__main__':
    app.run()
