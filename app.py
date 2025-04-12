import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
 
load_dotenv()

# pip install -r requirements.txt :- use this command to install requirements
def create_app():
    app = Flask(__name__) 
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def micro_blog():
        if request.method == "POST":
            entry_content = request.form.get("content")
            date = datetime.datetime.today().strftime("%y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": date})
        
        entries_with_date = [
            {"content": entry["content"], "date": entry["date"]}
            for entry in app.db.entries.find({})
        ]
        return render_template("microblog.html", entries=entries_with_date)

    return app
