from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_homepage():  # put application's code here
    return render_template('home.html'








if __name__ == '__main__':
    app.run()
