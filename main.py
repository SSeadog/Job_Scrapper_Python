from flask import Flask, render_template, request, redirect, send_file
from indeed import get_jobs as get_indeed_jobs
from jk import get_jobs as get_jk_jobs
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("seadog.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jk_jobs(word)
            db[word] = jobs
            if jobs[0].get("link") is None:
                return render_template("report.html", searchingBy=word, resultsNumber=0, jobs={})
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


app.run(host="0.0.0.0")
