from flask import Flask
from flask import render_template
from flask import request
from class_category import Category
import class_game
import gamefileGenerator.createGamefiles as gamefilesGenerator
from flask import send_file
import time
import os
app = Flask(__name__)

SERVER="http://127.0.0.1:5000/"
# SERVER="https://smidra.pythonanywhere.com/"

this_game = class_game.Game("Deafult secret")
this_game.add_category("Dějepis")
this_game.categories[0].add_question("Kdo je to Václav Havel?", "Bývalý prezident ČR")
this_game.categories[0].add_question("Kdy skončila 2.sv?", "1945")
this_game.add_category("ZSV")
this_game.categories[1].add_question("Co je to inflace?", "Postupné znehodnocování peněz.")
this_game.categories[1].add_question("Zlatá cihlička!", "Bod zdarma.")

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

@app.route("/green_dashboard")
def green_dashboard():
    return render_template('dashboard.html',
    partial_secret = this_game.get_partial_secret(3),
    name = "Green team",
    color="success",
    points=this_game.green_points,
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
        elif request.form['points'] == "g-" :
            this_game.change_score(3,-1)
        elif request.form['points'] == "g+" :
            this_game.change_score(3,1)
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
    g=this_game.green_points,
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
    g=this_game.green_points,
    category_name=this_category.category_text,
    question_text=this_category.questions[selected_question].question_text,
    question_answer=this_category.questions[selected_question].question_answer)

# Administartion
@app.route('/admin_dashboard', defaults={'what_action': "default"}, methods=['GET', 'POST'])
@app.route("/admin_dashboard/<what_action>", methods=['GET', 'POST'])
def admin_dashboard(what_action="default"):
    loaded_game="no loaded game"
    loaded_questionslist="no loaded questionslist" 
    # Cleanup of old export
    try:
        os.remove("/tmp/output.xlsx")
    except:
        pass
    # Manage aministrtor request 
    if request.method == 'POST':
        # Change points
        add_points(request)
        # Do I wish to load something?
        # -- Load gamefile
        if (what_action=="load_gamefile"):
            try:
                f = request.files['file']  
                f.save(f.filename)
                this_game.load(f.filename)
                loaded_game=f.filename  
            except:
                print("No file sent.")
        # -- Load questions list
        elif (what_action=="load_questionslist"):
            try:
                f = request.files['file']
                f.save(f.filename)
                loaded_questionslist=f.filename
                print("Got into Python filename is:", f.filename)
                NUMEBR_OF_GAMEFILES = request.form['NUMEBR_OF_GAMEFILES']
                NUMEBR_OF_SUBJECTS_IN_GAMEFILE = request.form['NUMEBR_OF_SUBJECTS_IN_GAMEFILE']
                NUMBER_OF_QUESTIONS_PER_SUBJECT = request.form['NUMBER_OF_QUESTIONS_PER_SUBJECT']
                gamefilesGenerator.generate_gamefiles( str(f.filename), "/tmp/output.xlsx", int(NUMEBR_OF_GAMEFILES), int(NUMEBR_OF_SUBJECTS_IN_GAMEFILE), int(NUMBER_OF_QUESTIONS_PER_SUBJECT))
                # Cleanup the uploaded file - would cause more security holes that i care to fix. Let the files live 3 months - who cares.
            except:
                print("No file saved.")
            
            time.sleep(5) # There is a second sleep to trigger the spinner in administrace.html. I have shamed the honor of my familly with this code.
            what_action="default"
            return send_file("/tmp/output.xlsx")

    return render_template('administrace.html',
    r=this_game.red_points, b=this_game.blue_points, g=this_game.green_points,
    loaded_game=loaded_game, loaded_questionslist=loaded_questionslist, what_action=what_action)

