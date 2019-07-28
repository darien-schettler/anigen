from flask import Flask, request, jsonify
from flask_cors import CORS
from txt_imports import RANDOM_WORD_LIST, REAL_TITLES
from helper_functions import prediction_engine, generate_text, get_args_from_post, parse_anigen_and_dropped_titles

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


# api/app.py
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)

