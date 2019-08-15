# -*- coding: utf-8 -*-
from txt_imports import TITLE_VOCAB, RANDOM_WORD_LIST
from feature_imports import TITLE_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS

import random

import numpy as np

import tensorflow as tf
tf.compat.v1.enable_eager_execution()

# ------------------------------- FNS BELOW WILL BE USED WITHIN IMPORTED FNs ------------------------------------


def mapping_creation(vocab):
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}

    # Creating a mapping from indices to unique characters
    idx2char = np.array(vocab)

    return char2idx, idx2char


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):

    if tf.test.is_gpu_available():
        rnn = tf.compat.v1.keras.layers.CuDNNGRU
    else:
        import functools
        rnn = functools.partial(tf.keras.layers.GRU, recurrent_activation='sigmoid')

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]))
    model.add(rnn(rnn_units, return_sequences=True, recurrent_initializer='glorot_uniform', stateful=True))
    model.add(tf.keras.layers.Dropout(0.075))
    model.add(rnn(rnn_units, return_sequences=True, recurrent_initializer='glorot_uniform', stateful=True))
    model.add(tf.keras.layers.Dense(vocab_size))

    return model


# ----------------------------------------------------------------------------------------------------------------

# ------------------------------------ FNS BELOW WILL BE IMPORTED INTO APP -------------------------------------------


def prediction_engine():
    weights = tf.train.latest_checkpoint('./engine/ckpts/')
    engine = build_model(TITLE_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)
    engine.load_weights(weights)
    engine.build(tf.TensorShape([1, None]))
    return engine


# Used to generate text
title_char2idx, title_idx2char = mapping_creation(TITLE_VOCAB)


def generate_text(engine, start_string="", temp=0.75, num_generate=400, random_word_list=RANDOM_WORD_LIST):
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

    # Empty list to store our titles once split
    output_titles = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = temp

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a multinomial distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        # We pass the predicted word as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx2char[predicted_id])
        output_string = start_string + ''.join(text_generated)
        output_titles = [x.strip() for x in output_string.split("~")]
    return output_titles


def get_args_from_post(data_in):
    if data_in.get('batchSize') is not None:
        num_of_chars = int(data_in.get('batchSize'))
    else:
        num_of_chars = 50

    if data_in.get('startString') is not None:
        start_string = data_in.get('startString')
    else:
        start_string = ""

    if data_in.get('randomness') is not None:
        temp = float(data_in.get('randomness'))
    else:
        temp = 0.75

    return num_of_chars, start_string, temp


def parse_anigen_and_dropped_titles(titles, real_titles, num_of_chars):
    anigen_titles = titles[1:]

    dropped_titles = [x for x in titles if x in real_titles]
    dropped_list_dict = [{"dropped_title": dropped_title} for dropped_title in dropped_titles]

    anigen_titles = [x for x in anigen_titles if x not in real_titles]

    if int(num_of_chars) == 50:
        anigen_list_dict = [{"anigen_title": anigen_titles[0]}]
    else:
        anigen_list_dict = [{"anigen_title": title} for title in anigen_titles if len(title) >= 4]


    return anigen_list_dict, dropped_list_dict
# ----------------------------------------------------------------------------------------------------------------
