from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from txt_imports import RANDOM_WORD_LIST, REAL_TITLES
from helper_functions import prediction_engine, generate_text, get_args_from_post, parse_anigen_and_dropped_titles
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABSE_URI

# -----------------------------------------------------------------------------------
#                                   IMPORTS ABOVE
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
#                               CREATE FLASK APPLICATION
# -----------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABSE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from models import ExcellentList, WeirdList

db.create_all()
db.session.commit()

# -------------------------------------------
# Make the title prediction model {engine}
# -------------------------------------------
title_engine = prediction_engine()
# -------------------------------------------


# ---------------------------------------------------------------------------------------------------------------
#                                           ENDPOINT DEFINITIONS ARE BELOW
# ---------------------------------------------------------------------------------------------------------------
# request model prediction endpoint
@app.route('/api/predict/', methods=['POST'])
def predict():
    """Handle request and output model generated titles in json format"""

    # Handle empty requests.
    if not request.json:
        return jsonify({'error': 'no request received'})

    num_of_chars, start_string, temp = get_args_from_post(request.get_json())

    anigen_titles = generate_text(engine=title_engine,
                                  start_string=start_string,
                                  temp=temp,
                                  num_generate=num_of_chars,
                                  random_word_list=RANDOM_WORD_LIST)

    anigen_list_dict, dropped_list_dict = parse_anigen_and_dropped_titles(titles=anigen_titles,
                                                                          real_titles=REAL_TITLES,
                                                                          num_of_chars=num_of_chars)

    return jsonify(anigen_list_dict, dropped_list_dict)


# leaderboard endpoint
@app.route('/api/leaderboard/', methods=['GET'])
def leaderboard():

    title = request.args.get('title')
    upvote = request.args.get('upvote')

    if title is not None:

        excellent_title = ExcellentList.query.filter_by(title=title).first()

        if excellent_title is None:

            excellent_title = ExcellentList(title=title, votes=1)
            db.session.add(excellent_title)
            db.session.commit()

        else:

            excellent_title.upvote()

    if upvote is not None:
        title_to_upvote = ExcellentList.query.filter_by(title=upvote).first()
        title_to_upvote.upvote()

    leaderboard_data = ExcellentList.query.all()
    leaderboard_titles = [ld.title for ld in leaderboard_data]
    leaderboard_votes = [ld.votes for ld in leaderboard_data]
    leaderboard_data = [{"votes": v, "anigen_titles": t} for v, t in zip(leaderboard_votes, leaderboard_titles)]

    return jsonify(leaderboard_data)


# weirderboard endpoint
@app.route('/api/weirderboard/', methods=['GET'])
def weirderboard():
    title = request.args.get('title')
    upvote = request.args.get('upvote')

    if title is not None:

        weird_title = WeirdList.query.filter_by(title=title).first()
        if weird_title is None:

            weird_title = WeirdList(title=title, votes=1)
            db.session.add(weird_title)
            db.session.commit()

        else:

            weird_title.upvote()

    if upvote is not None:
        title_to_upvote = WeirdList.query.filter_by(title=upvote).first()
        title_to_upvote.upvote()

    weirderboard_data = WeirdList.query.all()
    weirderboard_titles = [wd.title for wd in weirderboard_data]
    weirderboard_votes = [wd.votes for wd in weirderboard_data]
    weirderboard_data = [{"votes": v, "anigen_titles": t} for v, t in zip(weirderboard_votes, weirderboard_titles)]

    return jsonify(weirderboard_data)
# ---------------------------------------------------------------------------------------------------------------


# api/app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

