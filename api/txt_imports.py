# -*- coding: utf-8 -*-

# Retrieve the list of characters from the title_vocab.txt file --> TITLE_VOCAB
with open("engine/txt_files/title_vocab.txt", encoding="utf-8") as file:
    content = file.readlines()
    TITLE_VOCAB = [x.strip() for x in content]
    TITLE_VOCAB[0] = ' '

# Retrieve the list of random words from the random_word_list.txt file --> RANDOM_WORD_LIST
with open("engine/txt_files/random_word_list.txt") as file:
    content = file.readlines()
    RANDOM_WORD_LIST = [x.strip().capitalize() for x in content]

# Retrieve the list of real anime titles from the real_titles.txt file --> REAL_TITLES
with open("./engine/txt_files/real_titles.txt", encoding="utf-8") as f:
    content = f.readlines()
    REAL_TITLES = [x.strip().title() for x in content]
