from txt_imports import TITLE_VOCAB, RANDOM_WORD_LIST
from feature_imports import TITLE_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS

import random

import numpy as np

import tensorflow as tf
tf.enable_eager_execution()

# ------------------------------- FNS BELOW WILL BE USED WITHIN IMPORTED FNs ------------------------------------


def mapping_creation(vocab):
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}

    # Creating a mapping from indices to unique characters
    idx2char = np.array(vocab)

    return char2idx, idx2char


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


# ----------------------------------------------------------------------------------------------------------------
