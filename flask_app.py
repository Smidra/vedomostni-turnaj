from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

app.r = 0
app.g = 0
app.b = 0
app.y = 0
INCREMENT=9.7
MAXIMUM=3484.86
# SERVER="http://127.0.0.1:5000/"
SERVER="https://everesttest03.azurewebsites.net/"

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

@app.route("/setpoints")
def setPoints():    
    pocet = request.args.get('body', '')
    barva = request.args.get('barva', '')
    if barva=="r":
        app.r += int(pocet)
    elif barva=="b":
        app.b += int(pocet)
    elif barva=="g":
        app.g += int(pocet)
    elif barva=="y":
        app.y += int(pocet)
    
    return "Nastaveno " + pocet + " pro " + barva
