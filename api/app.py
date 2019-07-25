# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import tensorflow as tf
from flask_cors import CORS
import time, random, json

tf.enable_eager_execution()

# Create application
app = Flask(__name__)
CORS(app)

LEADER_BOARD = []
VOTES = [1, 2, 3, 4, 5, 65, 4, 3, 2, 1, 1]
WEIRDER_BOARD = []

# global TITLE_VOCAB, random_word_list, real_titles

with open("engine/txt_files/title_vocab.txt", encoding="utf-8") as file:
    content = file.readlines()
    TITLE_VOCAB = [x.strip() for x in content]
    TITLE_VOCAB[0] = ' '

with open("engine/txt_files/random_word_list.txt") as file:
    content = file.readlines()
    random_word_list = [x.strip().capitalize() for x in content]

with open("./engine/txt_files/real_titles.txt", encoding="utf-8") as f:
    real_titles = f.readlines()
    real_titles = [x.strip().title() for x in real_titles]

# Constants for the model
PATH_TO_MODEL_FILE = "./engine/model_file"
TITLE_VOCAB_SIZE = len(TITLE_VOCAB)
EMBEDDING_DIM = 512
RNN_UNITS = 1024


def mapping_creation(vocab):
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}

    # Creating a mapping from indices to unique characters
    idx2char = np.array(vocab)

    return char2idx, idx2char


title_char2idx, title_idx2char = mapping_creation(TITLE_VOCAB)


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([

        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        tf.keras.layers.Dropout(0.25),

        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.2),

        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.05),

        tf.keras.layers.Dense(vocab_size)
    ])

    return model


def prediction_engine():
    weights = tf.train.latest_checkpoint('./engine/ckpts/')
    engine = build_model(TITLE_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)
    engine.load_weights(weights)
    engine.build(tf.TensorShape([1, None]))
    return engine


title_engine = prediction_engine()


def generate_text(engine, start_string="", temp=0.75, num_generate=400, random_word_list=random_word_list):
    if start_string == "":
        start_string = random_word_list[int(random.random() * len(random_word_list) - 1)]

    start_string = " ~ " + start_string

    char2idx = title_char2idx
    idx2char = title_idx2char

    model = engine

    # Evaluation step (generating text using the learned model)

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = temp
    output_titles = []

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a multinomial distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.multinomial(predictions, num_samples=1)[-1, 0].numpy()

        # We pass the predicted word as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
        output_string = start_string + ''.join(text_generated)
        output_titles = [x.strip() for x in output_string.split("~")]
    return output_titles


# request model prediction
@app.route('/predict/<batch_size>', methods=['GET'])
def predict(batch_size):
    anigen_titles = generate_text(engine=title_engine,
                                  start_string="",
                                  temp=0.75,
                                  num_generate=int(batch_size),
                                  random_word_list=random_word_list)

    anigen_titles = anigen_titles[1:]

    original_length = len(anigen_titles)
    anigen_titles = [x for x in anigen_titles if x not in real_titles]
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
@app.route('/leaderboard/', methods=['GET'])
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
@app.route('/weirderboard/', methods=['GET'])
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
