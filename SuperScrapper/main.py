from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
import requests
from bs4 import BeautifulSoup
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


# @: decorator - looks for a function right under itself.
# Query Arguments


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            so_url = f"https://stackoverflow.com/jobs?q={word}"
            so_result = requests.get(so_url)
            so_soup = BeautifulSoup(so_result.text, "html.parser")
            empty_result = so_soup.find_all("div", {"class": "s-empty-state"})
            if empty_result:
                return render_template("empty_result.html", searchingBy=word)
            else:
                jobs = get_jobs(word)
                db[word] = jobs
        return render_template(
            "report.html",
            searchingBy=word,
            resultsNumber=len(jobs),
            jobs=jobs)
    else:
        return redirect("/")


@app.route("/<username>")
def contact(username):
    return f"Hello {username}, how are you doing?"


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(word, jobs)
        return send_file(f"{word}_jobs.csv", as_attachment=True, )
    except:
        return redirect("/")


app.run(host="0.0.0.0")
