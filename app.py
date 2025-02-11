from flask import Flask, jsonify, request, render_template
from flask import request
import json
import sqlite3
app = Flask(__name__)


@app.route('/', methods=['POST'])
def post():
    if request.form['button']=="CONTINUE":  
        username = request.form['username']
        password = request.form['password']
        if username.lower()=="log":
            print(users)
        LoggedIn = False
        for x in users:
            if x['Username'].lower()==username.lower():
                if x['Password']==password:
                    print(f"User logged in as {username}")
                    return(render_template('index.html', name=username))
        if LoggedIn==False:
            return render_template("login.html")
    elif request.form['button']=="CREATE ACCOUNT":
        username = request.form['username']
        password = request.form['password']
        invalid = False
        for i in users:
            if i['Username'].lower()==username.lower():
                invalid=True
        if invalid==False:
            users.append({"Username": username, "Password": password, "ID": 0})
            json.dump(users, open("Users.json", "w"), indent=2)
            return "Account created, Username: " + username +" Password: " + password
        else:
            return render_template('signup.html')

#handling GET requests to pages
@app.route('/login.html', methods=['GET'])
def showlogin():
    return render_template('login.html')
@app.route('/signup.html', methods=['GET'])
def showsignup():
    return render_template('signup.html')
@app.route('/about.html', methods=['GET'])
def showabout():
    return render_template('about.html')


#temporary page to upload data to data.db
@app.route('/postplace.html', methods=['GET'])
def showpostscreen():
    return render_template('postplace.html')
@app.route('/postplace.html', methods=['POST'])
def postdata():
    place_id = int(request.form['place_id'])
    name = request.form['name']
    category = request.form['category']
    coordx = float(request.form['coordx'])
    coordy = float(request.form['coordy'])
    about = request.form['about']
    address = request.form['address']
    open_hours = request.form['open_hours']
    website = request.form['website']
    phone_number = request.form['phone_number']
    con = sqlite3.connect('database/data.db')
    cur = con.cursor()
    cur.execute("INSERT INTO catalogue(place_id, name, category, coordx, coordy, about, address, open_hours, website, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (place_id, name, category, coordx, coordy, about, address, open_hours, website, phone_number))
    con.commit()
    return render_template("postplace.html")

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
