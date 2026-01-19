from flask import Blueprint, request, jsonify, render_template
from scheduler.generator_ga import genetic_scheduler
from config import DAYS

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/generate", methods=["POST"])
def generate():

    classes=[c.strip() for c in request.form["classes"].split(",") if c.strip()]

    subjects={}
    for line in request.form["subjects"].splitlines():
        s,c,t=line.split(":")
        subjects[s]={"count":int(c),"type":t}

    teachers={}
    for line in request.form["teachers"].splitlines():
        s,t=line.split(":")
        teachers[s]=[x.strip() for x in t.split(",")]

    timetable=genetic_scheduler(classes,subjects,teachers,DAYS)
    return jsonify(timetable)
