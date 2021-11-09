from flask import Flask
from flask import render_template
from flask import request
import class_game
app = Flask(__name__)

app.r = 0
app.g = 0
app.b = 0
app.y = 0
INCREMENT=9.7
MAXIMUM=3484.86

SERVER="http://127.0.0.1:5000/"
# SERVER="https://smidra.pythonanywhere.com/"

this_game = class_game.Game("Supertajná tajenka.")

@app.route("/red_dashboard")
def red_dashboard():
    partial_secret = this_game.get_partial_secret(1)
    return "<p>Red partial secret is:" + partial_secret + "</p>"

@app.route("/blue_dashboard")
def blue_dashboard():
    partial_secret = this_game.get_partial_secret(2)
    return "<p>Blue partial secret is:" + partial_secret + "</p>"

# Administrace
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    # Change points
    if request.method == 'POST':

        if request.form['points'] == "r+" :
            this_game.red_points += 1
        elif request.form['points'] == "r-" :
            this_game.red_points -= 1
        elif request.form['points'] == "b+" :
            this_game.blue_points += 1
        elif request.form['points'] == "b-" :
            this_game.blue_points -= 1
        else:
            print("Unknown form submission.")

    return render_template('administrace.html',
    r=this_game.red_points, b=this_game.blue_points,
    server=SERVER)


def htmlify(cislo):
    return "width: "+ str(cislo/(MAXIMUM/100)) + "%"

@app.route("/")
def index():
    return render_template('index.html',
    r=app.r, b=app.b, g=app.g, y=app.y,
    maximum=MAXIMUM,
    prog_r=htmlify(app.r),
    prog_b=htmlify(app.b),
    prog_g=htmlify(app.g),
    prog_y=htmlify(app.y))

@app.route("/klikadlo")
def klikadlo():
    return render_template('klikadlo.html',
    progress=htmlify(app.r+app.b+app.g+app.y),
    maximum=MAXIMUM, 
    server=SERVER)

# Pridavani prichozich hodnot
@app.route("/r")
def addR():
    app.r += INCREMENT
    return True

@app.route("/b")
def addM():
    app.b += INCREMENT
    return True

@app.route("/g")
def addG():
    app.g += INCREMENT
    return True

@app.route("/y")
def addY():
    app.y += INCREMENT
    return True

@app.route("/wait")
def waitSite():
    return render_template('wait.html', server=SERVER)

# Administrace
@app.route("/jenomrada")
def admin():
    return render_template('administrace.html',
    r=app.r, b=app.b, g=app.g, y=app.y,
    maximum=MAXIMUM,
    prog_r=htmlify(app.r),
    prog_b=htmlify(app.b),
    prog_g=htmlify(app.g),
    prog_y=htmlify(app.y),
    server=SERVER)

