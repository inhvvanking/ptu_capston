
from flask import Flask, render_template, request
from analysis.analysis import analyze, simulate, analyze_filtered

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    action = request.args.get("action")
    grade = request.args.get("grade")
    major = request.args.get("major")

    if grade or major:
        data = analyze_filtered(grade, major)
    else:
        data = analyze()

    if action:
        data = simulate(action)

    data["current_grade"] = grade
    data["current_major"] = major

    return render_template("result.html", **data)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

