# Imports
from flask import Flask, render_template, request, redirect
import traceback
import threading
import hashlib
import os

# Initialize app
app = Flask(__name__)

# Read the password but if the file doesnt exist create a new one
try:
    with open('password.txt', 'r') as f:
        password = f.read()
except FileNotFoundError:
    # Ask, hash, and save password in password.txt
    password = hashlib.sha512(input('Password\n> ').encode()).hexdigest()
    with open('password.txt', 'w') as f:
        f.write(password)

# Session_key handles login.
session_key = hashlib.sha256(os.urandom(32)).hexdigest()

# Ids and console info for the python execution.
current_id = 0
ids = {}


@app.get('/')
def index():
    if request.cookies.get('token') == session_key:
        return render_template('index.html')
    return redirect("/login")


@app.get("/login")
def login():
    if request.cookies.get('token') == session_key:
        return redirect("/")
    return render_template("login.html")


@app.post('/process-login')
def process_login():
    if request.cookies.get('token') == session_key:
        return redirect("/")

    passw = request.form.get("password")
    if hashlib.sha512(passw.encode()).hexdigest() != password or len(passw) > 256:
        return redirect("/login")

    resp = redirect('/')
    resp.set_cookie("token", session_key)

    return resp


@app.post('/process-python')
def process_python():
    global current_id
    if request.cookies.get('token') != session_key:
        return redirect("/")

    current_id += 1
    ids[str(current_id)] = -1
    threading.Thread(target=python_runner, args=(request.form.get('code'), str(current_id),)).start()

    resp = redirect("/code-console")
    resp.set_cookie("id", str(current_id))

    return resp


def python_runner(code, _id):
    # Executes in thread
    try:
        exec(str(code))
    except Exception:
        # traceback.format_exc() formats the exception in the same way as the console.
        ids[_id] = traceback.format_exc().replace("\n", "<br>")
        return

    # If the code passed without any difficulties
    ids[_id] = "Passed without any problem"


@app.get('/code-console')
def code_console():
    if request.cookies.get("id") is None:
        return redirect('/')
    # I was to lazy to make a code-console.html file.
    return '''
<h1 align="center">Code output: </h1>
<h4 align="center" id="output">Output will appear here</h2>
<script>
const Http = new XMLHttpRequest();
const url='/get-python';

while(true){
Http.open("GET", url, false);
Http.send();
let resp = Http.responseText;
if(resp !== "null"){
    document.getElementById("output").innerHTML = resp;
    console.log(resp);
    break;
}
}
</script>
    '''


@app.get("/get-python")
def get_python():
    # Handles giving back the console output
    global ids

    if ids.get(str(request.cookies.get('id'))) is None:
        return "Invalid id!"

    if ids.get(str(request.cookies.get('id'))) == -1:
        return "null"

    out = str(ids[request.cookies.get('id')])
    ids.pop(str(request.cookies.get('id')))
    return out


# All mentioned anchors in the index.html file

# Allows for both get and post requests
@app.get("/set-pass")
@app.post("/set-pass")
def set_pass():
    if request.cookies.get('token') != session_key:
        return redirect("/login")

    if request.method == "POST":
        global password

        # Check if passwords are the same and if the given current password is the current password
        if request.form.get('new1') != request.form.get('new2'):
            return redirect("/set-pass")
        if hashlib.sha512(request.form.get('old').encode()).hexdigest() != password:
            return redirect('/set-pass')

        # Change and save password
        password = hashlib.sha512(request.form.get('new1').encode()).hexdigest()
        with open('password.txt', 'w') as f:
            f.write(password)

        return redirect('/')

    return render_template('setpass.html')


@app.get('/exec-python')
def exec_python():
    if request.cookies.get('token') != session_key:
        return redirect("/login")

    return render_template('/execpython.html')


@app.get('/add-file')
@app.post("/add-file")
def add_file():
    if request.cookies.get('token') != session_key:
        return redirect("/login")

    if request.method == 'POST':
        with open(request.form.get('filename'), 'w') as f:
            f.write(request.form.get('content'))

        return redirect('/')

    return render_template('/addfile.html')

@app.get('/delete-file')
@app.post("/delete-file")
def del_file():
    if request.cookies.get('token') != session_key:
        return redirect("/login")

    if request.method == 'POST':
        if not os.path.exists(request.form.get('filename')):
            return redirect('/delete-file')
        os.remove(request.form.get('filename'))

        return redirect('/')

    return render_template('/delfile.html')


# Run python file
if __name__ == '__main__':
    app.run('0.0.0.0', 80)
