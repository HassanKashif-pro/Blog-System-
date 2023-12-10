from flask import Flask, send_file, redirect, session, request
from replit import db
import os

app = Flask(__name__, static_url_path="/static")
app.secret_key = os.environ.get('secretKey')


def getBlog():
  entry = ""
  f = open("Form.html", "r")
  entry = f.read()
  f.close()
  keys = db.keys()
  keys = list(keys)
  content = ""
  for key in reversed(keys):
    thisEntry = entry
    if key != "user":
        thisEntry = thisEntry.replace("{title}", db[key]["title"])
        thisEntry = thisEntry.replace("{date}", db[key]["date"])
        thisEntry = thisEntry.replace("{body}", db[key]["body"])

        content += thisEntry
    return content




@app.route('/')
def index():
  if session.get('user'):
      return redirect("/EditForm")
  else:
    page = ""
    f  = open("edit.html", "r")
    page = f.read()
    f.close()
    page = page.replace("{content}", getBlog())
    return page


@app.route('/BlogForm', methods=["GET", "POST"])
def blog_form():
  if request.method == 'GET':
      return redirect("/EditForm")
      # Handle GET request
  elif request.method == 'POST':
      return send_file("edit.html")
      # Handle POST request


@app.route('/EditForm', methods=["GET", "POST"])
def Edit():
  if session.get("user"):
      return redirect("/LoginForm")
  else:  
    page = ""
    f  = open("edit.html", "r")
    page = f.read()
    page = page.replace("{content}",getBlog())
    f.close()
    return page


@app.route('/add', methods=["POST"])
def add():
  form = request.form
  entry = {
      "title": form["title"],
      "date": form["date"],
      "body": form["body"]
  }
  db[form["date"]] = entry
  return redirect("/EditForm")

@app.route('/logout')
def logout():
  session.clear()
  return redirect("/")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)