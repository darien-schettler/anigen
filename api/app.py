from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from txt_imports import RANDOM_WORD_LIST, REAL_TITLES
from helper_functions import prediction_engine, generate_text

# -----------------------------------------------------------------------------------
#                                   IMPORTS ABOVE
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
#                               CREATE FLASK APPLICATION
# -----------------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# ------------------------------------------------------
#               TEMPORARY DUMMY DATA
# ------------------------------------------------------
LEADER_BOARD = []
WEIRDER_BOARD = []
VOTES = [1, 2, 3, 4, 5, 65, 4, 3, 2, 1, 1, 65, 4, 3, 2, 1, 1]
# ------------------------------------------------------


# -------------------------------------------
# Make the title prediction model {engine}
# -------------------------------------------
title_engine = prediction_engine()
# -------------------------------------------


# ---------------------------------------------------------------------------------------------------------------
#                                           ENDPOINT DEFINITIONS ARE BELOW
# ---------------------------------------------------------------------------------------------------------------
# request model prediction endpoint
@app.route('/api/predict/<batch_size>', methods=['GET'])
def predict(batch_size):
    anigen_titles = generate_text(engine=title_engine,
                                  start_string="",
                                  temp=0.75,
                                  num_generate=int(batch_size),
                                  random_word_list=RANDOM_WORD_LIST)

    anigen_titles = anigen_titles[1:]

    original_length = len(anigen_titles)
    anigen_titles = [x for x in anigen_titles if x not in REAL_TITLES]
    dropped_titles = original_length - len(anigen_titles)

    if int(batch_size) == 50:
        anigen_list_dict = [{"anigen_title": anigen_titles[0]}]
    else:
        anigen_list_dict = [{"anigen_title": title.title()} for title in anigen_titles if len(title) >= 4]

    data = {'number_of_dropped_titles': dropped_titles,
            'anigen_title_count': original_length - dropped_titles,
            'anigen_titles': anigen_list_dict}

    return data


# leaderboard endpoint
@app.route('/api/leaderboard/', methods=['GET'])
def leaderboard():

    title = request.args.get('title')
    upvote = request.args.get('upvote')

    if title is not None:
        if title not in LEADER_BOARD:
            LEADER_BOARD.append(title)

        VOTES[LEADER_BOARD.index(title)] += 1
        return jsonify(LEADER_BOARD)

    if upvote is not None:
        VOTES[LEADER_BOARD.index(upvote)] += 1

    leaderboard = [{"votes": v, "anigen_titles": t} for v, t in zip(VOTES, LEADER_BOARD)]
    return jsonify(leaderboard)


# weirderboard endpoint
@app.route('/api/weirderboard/', methods=['GET'])
def weirderboard():

    title = request.args.get('title')
    upvote = request.args.get('upvote')

    if title is not None:
        if title not in WEIRDER_BOARD:
            WEIRDER_BOARD.append(title)

        VOTES[WEIRDER_BOARD.index(title)] += 1
        return jsonify(WEIRDER_BOARD)

    if upvote is not None:
        VOTES[WEIRDER_BOARD.index(upvote)] += 1

    weirderboard = [{"votes": v, "anigen_titles": t} for v, t in zip(VOTES, WEIRDER_BOARD)]
    return jsonify(weirderboard)
# ---------------------------------------------------------------------------------------------------------------
