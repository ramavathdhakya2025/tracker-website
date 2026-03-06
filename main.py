import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQL_ALCHEMY_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Tracker(db.Model):
    __tablename__ = "daily_tracker"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    task: Mapped[str] = mapped_column(String, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=db.func.now())

with app.app_context():
    db.create_all()

TASKS = [
    "WakeUP at 4AM",
    "Read Book 5pages",
    "Meditation for 20 mins",
    "Manifest 4 times a day"
]
DAYS = [d for d in range(1, 22)]

@app.route('/')
def home():
    # Load saved progress
    progress = {}
    for entry in Tracker.query.all():
        progress[(entry.day, entry.task)] = entry.completed
    return render_template('app.html', tasks=TASKS, days=DAYS, progress=progress)

@app.route('/save', methods=['POST'])
def save():
    # Clear old entries
    Tracker.query.delete()

    for day in DAYS:
        for task in TASKS:
            field_name = f"day{day}_{task}"
            completed = field_name in request.form
            tracker_entry = Tracker(day=day, task=task, completed=completed)
            db.session.add(tracker_entry)

    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
