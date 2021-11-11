from flask import Flask
from flask import render_template
from flask import request
from class_category import Category
import class_game
app = Flask(__name__)

SERVER="http://127.0.0.1:5000/"
# SERVER="https://smidra.pythonanywhere.com/"

this_game = class_game.Game("Deafult secret")
this_game.add_category("Dějepis")
this_game.categories[0].add_question("Kdo je to Václav Havel?", "Bývalý prezident ČR")
this_game.categories[0].add_question("Kdy skončila 2.sv?", "1945")
this_game.add_category("ZSV")
this_game.categories[1].add_question("Co je to inflace?", "Postupné znehodnocování peněz.")

# Team dashboards
@app.route("/red_dashboard")
def red_dashboard():
    return render_template('dashboard.html',
    partial_secret = this_game.get_partial_secret(1),
    name = "Red team",
    color="danger",
    points=this_game.red_points,
    server=SERVER)

@app.route("/blue_dashboard")
def blue_dashboard():
    return render_template('dashboard.html',
    partial_secret = this_game.get_partial_secret(2),
    name = "Blue team",
    color="primary",
    points=this_game.blue_points,
    server=SERVER)

# Global function (eww) to parse reqest to change points
def add_points(recieved_request):
    request=recieved_request
    try:
        if request.form['points'] == "r+" :
            this_game.change_score(1,1)
        elif request.form['points'] == "r-" :
            this_game.change_score(1,-1)
        elif request.form['points'] == "b+" :
            this_game.change_score(2, 1)
        elif request.form['points'] == "b-" :
            this_game.change_score(2,-1)
    except:
        print("No points sent.")
        return False
    return True

# Gameboard
@app.route("/", methods=['GET', 'POST'])
def game_dashboard():
    # Change points if coming from a question.
    if request.method == 'POST':
        add_points(request)
    return render_template('game.html',
    r=this_game.red_points,
    b=this_game.blue_points,
    nr_categories=len(this_game.categories),
    categories=this_game.categories,
    game_name=this_game.game_name)

@app.route("/question", methods=['GET', 'POST'])
def game_question():
    # Parse what is the desired category and question
    selected_category = int(request.form['cat'])
    selected_question = int(request.form['question'])
    this_category = this_game.categories[selected_category]
    this_category.questions[selected_question].make_seen()
    # Render it
    return render_template('question.html',
    r=this_game.red_points,
    b=this_game.blue_points,
    category_name=this_category.category_text,
    question_text=this_category.questions[selected_question].question_text,
    question_answer=this_category.questions[selected_question].question_answer)

# Administartion
@app.route("/admin_dashboard", methods=['GET', 'POST'])
def admin_dashboard():
    loaded_game="none"
    if request.method == 'POST':
        # Change points
        add_points(request)        
        # Load file
        try:
            f = request.files['file']  
            f.save(f.filename)
            this_game.load(f.filename)
            loaded_game=f.filename
        except:
            print("No file sent.")
    return render_template('administrace.html',
    r=this_game.red_points, b=this_game.blue_points,
    loaded_game=loaded_game)

