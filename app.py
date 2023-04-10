from flask import Flask, jsonify, render_template, request
from pathlib import Path
import firebase_admin
from firebase_admin import db
import random

cred_object = firebase_admin.credentials.Certificate('thesis-97ea0-firebase-adminsdk-30tt2-ffccac5c02.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': 'https://thesis-97ea0-default-rtdb.firebaseio.com/'
})

SUBSET_SIZE = 20

app = Flask(__name__)


@app.route('/')
def ping_server():
    return render_template("main.html")

@app.route('/survey', methods=['POST'])
def survey():
    fake_audios = list(Path("static/generated").rglob("*fake_*.wav"))
    random.shuffle(fake_audios)
    fake_audios = fake_audios[:SUBSET_SIZE]

    audio_ids = [x.stem.split("_")[1] for x in fake_audios]

    real_audios = [str(x).replace("fake", "noisy") for x in fake_audios]
    fake_audios = [str(x) for x in fake_audios]

    audios = list(zip(real_audios, fake_audios, audio_ids))

    to_swap = [random.random() < 0.5 for _ in audios]
    audios = [(b, a, f"{c}_f") if flag else (a, b, f"{c}_r") for ((a,b,c), flag) in zip(audios, to_swap)]

    return render_template("index.html", audios=audios)

@app.route("/submit", methods=['POST'])
def submit():
    print(request.form)

    collection_ref =  db.reference('survey-answers')

    collection_ref.push().set(request.form)

    return "Thank you for your answer!"
if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
