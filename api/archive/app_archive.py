# -*- coding: utf-8 -*-

from random_word import RandomWords
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import tensorflow as tf

tf.enable_eager_execution()

# Create application
app = Flask(__name__)

# Create a random word generator to be used later
word_generator = RandomWords()

with open("engine/txt_files/title_vocab.txt", encoding="utf-8") as file:
    content = file.readlines()
    TITLE_VOCAB = [x.strip() for x in content]
    TITLE_VOCAB[0] = ' '

with open("engine/txt_files/synopsis_vocab.txt", encoding="utf-8") as file:
    content = file.readlines()
    SYNOPSIS_VOCAB = [x.strip() for x in content]
    SYNOPSIS_VOCAB[0] = ' '
    SYNOPSIS_VOCAB[94] = '\xa0'
    SYNOPSIS_VOCAB[168] = '\u2028'
    SYNOPSIS_VOCAB[169] = '\u202f'
    SYNOPSIS_VOCAB[198] = '\u3000'

with open("engine/txt_files/title_and_synopsis_vocab.txt", encoding="utf-8") as file:
    content = file.readlines()
    TITLE_AND_SYNOPSIS_VOCAB = [x.strip() for x in content]
    TITLE_AND_SYNOPSIS_VOCAB[0] = " "
    TITLE_AND_SYNOPSIS_VOCAB[95] = '\xa0'
    TITLE_AND_SYNOPSIS_VOCAB[174] = '\u2028'
    TITLE_AND_SYNOPSIS_VOCAB[175] = '\u202f'
    TITLE_AND_SYNOPSIS_VOCAB[210] = '\u3000'

# Vocabs
# TITLE_VOCAB = [' ', '!', '"', '#', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '|', '~', '¥', '«', '°', '²', '³', '´', '»', '½', 'À', 'Ä', 'É', 'Î', '×', 'Ø', 'à', 'ä', 'ç', 'è', 'é', 'ê', 'í', 'ô', 'ö', 'ù', 'ú', 'ü', 'Ā', 'Ō', 'ō', 'ū', 'Ω', 'α', 'μ', 'ḥ', '\u200b', '–', '’', '“', '”', '†', '₩', '℃', '↑', '→', '∀', '−', '√', '∞', '○', '★', '☆', '♡', '♥', '♪', '♯', '✡', '✿', '⤴', '。', '〜', 'い', 'か', 'が', 'き', 'こ', 'さ', 'し', 'じ', 'た', 'ち', 'つ', 'て', 'で', 'と', 'な', 'に', 'の', 'ば', 'ま', 'み', 'め', 'る', 'ろ', 'わ', 'ん', 'イ', 'ダ', 'マ', 'リ', 'ワ', 'ン', '・', 'ー', '人', '回', '官', '復', '心', '恋', '抱', '明', '星', '束', '板', '棲', '甘', '神', '私', '縁', '縛', '能', '裏', '覧', '～']
# SYNOPSIS_VOCAB = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '}', '~', '\xa0', '©', '«', '\xad', '°', '±', '²', '³', '´', 'µ', '·', '»', '½', 'Á', 'È', 'É', 'Ö', '×', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'ç', 'è', 'é', 'ê', 'ë', 'í', 'î', "ï", 'ñ', 'ó', 'ô', 'ö', '÷', 'ù', 'ú', 'û', 'ü', 'Ā', 'ā', 'ē', 'ī', 'Ō', 'ō', 'š', 'ū', 'ǒ', 'ǔ', '˚', 'Α', 'Δ', 'Ψ', 'Ω', 'α', 'β', 'γ', 'μ', 'π', 'е', 'ḥ', '\u200b', '–', '—', '―', '‘', '’', '“', '”', '†', '•', '…', '\u2028', '\u202f', '‹', '※', '€', '℃', '™', '↑', '→', '⇎', '√', '≒', '≪', '≫', '─', '△', '○', '●', '◯', '★', '☆', '♀', '♂', '♡', '♥', '♪', '♭', '♯', '❤', '⤴', '\u3000', '、', '。', '〇', '〈', '〉', '《', '》', '「', '」', '『', '』', 'あ', 'い', 'う', 'え', 'ぉ', 'お', 'か', 'が', 'き', 'ぎ', 'く', 'け', 'げ', 'こ', 'ご', 'さ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'た', 'だ', 'ち', 'ぢ', 'っ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ば', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ま', 'み', 'む', 'め', 'も', 'ゃ', 'や', 'ゅ', 'ゆ', 'ょ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん', 'ァ', 'ア', 'ィ', 'イ', 'ウ', 'ェ', 'エ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ', 'コ', 'サ', 'シ', 'ジ', 'ス', 'ズ', 'セ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ッ', 'ツ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ャ', 'ュ', 'ユ', 'ョ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ン', 'ヴ', '・', 'ー', 'ㅡ', '一', '丁', '三', '上', '世', '中', '丸', '主', '乙', '乳', '事', '二', '京', '人', '介', '仕', '他', '付', '代', '仰', '仲', '任', '会', '伝', '似', '体', '何', '佗', '作', '侠', '係', '俗', '俺', '倒', '側', '偽', '催', '僕', '優', '兄', '先', '光', '入', '八', '共', '内', '冷', '出', '刊', '初', '刺', '刻', '剑', '力', '動', '勝', '募', '勧', '化', '医', '印', '厚', '原', '去', '又', '友', '取', '受', '古', '史', '合', '吉', '同', '向', '君', '吸', '周', '命', '和', '咥', '咬', '唸', '問', '嘘', '器', '図', '国', '園', '城', '堕', '墓', '士', '変', '夏', '外', '夜', '夢', '大', '天', '太', '奇', '奥', '奮', '女', '好', '妄', '娼', '婚', '婦', '嫁', '嫌', '子', '季', '学', '孫', '守', '完', '宝', '実', '客', '室', '宴', '家', '寄', '密', '尊', '小', '少', '尿', '屋', '巨', '巻', '巾', '師', '帰', '干', '年', '幸', '底', '店', '度', '引', '弘', '弟', '張', '形', '彼', '待', '後', '徒', '御', '心', '快', '怒', '思', '急', '恋', '恥', '患', '悪', '情', '惑', '想', '愁', '意', '愛', '態', '憂', '成', '戦', '手', '才', '打', '抱', '押', '拷', '持', '指', '挿', '捨', '授', '損', '摘', '擦', '攻', '放', '教', '散', '敬', '文', '方', '旅', '族', '日', '旺', '昏', '春', '昭', '昼', '時', '暑', '暗', '書', '曹', '替', '最', '月', '有', '期', '木', '未', '本', '来', '東', '果', '枯', '某', '染', '校', '桃', '桜', '森', '極', '楽', '様', '模', '権', '樹', '欲', '正', '歴', '死', '残', '段', '殺', '毒', '比', '氏', '民', '氓', '気', '水', '汁', '決', '治', '注', '泰', '活', '流', '浴', '海', '涙', '淫', '深', '清', '渚', '漂', '演', '漫', '潔', '激', '濁', '濃', '瀬', '火', '灵', '炎', '無', '煉', '熟', '熱', '燦', '爛', '物', '状', '猫', '獄', '獣', '玉', '王', '甘', '生', '田', '男', '界', '番', '疑', '病', '痛', '療', '発', '白', '百', '盛', '目', '真', '眠', '着', '矢', '知', '石', '研', '破', '硬', '祐', '神', '福', '禰', '秋', '科', '秘', '称', '稲', '稿', '穏', '究', '窓', '立', '童', '節', '米', '粋', '純', '紹', '終', '絆', '結', '絡', '綴', '緊', '締', '編', '練', '罪', '美', '羞', '者', '聖', '聞', '聴', '肉', '育', '背', '能', '脅', '腐', '腫', '腰', '自', '舎', '舞', '色', '花', '若', '茎', '草', '華', '落', '著', '薄', '薬', '藍', '虎', '虔', '虫', '蜜', '血', '行', '術', '街', '衝', '裸', '要', '覆', '見', '視', '覚', '触', '言', '記', '試', '詩', '話', '誘', '課', '談', '謎', '貌', '貞', '負', '贈', '贖', '赤', '超', '足', '路', '踏', '身', '車', '軋', '較', '輝', '輩', '農', '辺', '込', '迷', '迸', '追', '送', '逆', '透', '逢', '連', '週', '遊', '過', '道', '違', '遥', '郎', '部', '酒', '酔', '醒', '野', '金', '鉄', '録', '長', '門', '開', '間', '関', '闇', '闘', '门', '陰', '階', '雄', '集', '雪', '電', '霊', '青', '面', '音', '頬', '頭', '顔', '願', '類', '飲', '香', '馬', '駆', '験', '高', '鬱', '鬼', '魂', '鹿', '麻', '黒', '龍', '龙', '박', '사', '카', '프', '︎', '\ufeff', '！', '（', '）', '，', '－', '／', '１', '２', '６', '？', '［', '～', '｢', '｣', '�']
# TITLE_AND_SYNOPSIS_VOCAB = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\xa0', '¥', '©', '«', '\xad', '°', '±', '²', '³', '´', 'µ', '·', '»', '½', 'À', 'Á', 'Ä', 'È', 'É', 'Î', 'Ö', '×', 'Ø', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'ç', 'è', 'é', 'ê', 'ë', 'í', 'î', 'ï', 'ñ', 'ó', 'ô', 'ö', '÷', 'ù', 'ú', 'û', 'ü', 'Ā', 'ā', 'ē', 'ī', 'Ō', 'ō', 'š', 'ū', 'ǒ', 'ǔ', '˚', 'Α', 'Δ', 'Ψ', 'Ω', 'α', 'β', 'γ', 'μ', 'π', 'е', 'ḥ', '\u200b', '–', '—', '―', '‘', '’', '“', '”', '†', '•', '…', '\u2028', '\u202f', '‹', '※', '₩', '€', '℃', '™', '↑', '→', '⇎', '∀', '−', '√', '∞', '≒', '≪', '≫', '─', '△', '○', '●', '◯', '★', '☆', '♀', '♂', '♡', '♥', '♪', '♭', '♯', '✡', '✿', '❤', '⤴', '\u3000', '、', '。', '〇', '〈', '〉', '《', '》', '「', '」', '『', '』', '〜', 'あ', 'い', 'う', 'え', 'ぉ', 'お', 'か', 'が', 'き', 'ぎ', 'く', 'け', 'げ', 'こ', 'ご', 'さ', 'し', 'じ', 'す', 'ず', 'せ', 'ぜ', 'そ', 'ぞ', 'た', 'だ', 'ち', 'ぢ', 'っ', 'つ', 'づ', 'て', 'で', 'と', 'ど', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ば', 'ひ', 'び', 'ぴ', 'ふ', 'ぶ', 'ぷ', 'へ', 'ぺ', 'ほ', 'ぼ', 'ぽ', 'ま', 'み', 'む', 'め', 'も', 'ゃ', 'や', 'ゅ', 'ゆ', 'ょ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん', 'ァ', 'ア', 'ィ', 'イ', 'ウ', 'ェ', 'エ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ', 'ゲ', 'コ', 'サ', 'シ', 'ジ', 'ス', 'ズ', 'セ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ', 'ッ', 'ツ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'バ', 'パ', 'ヒ', 'ビ', 'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ャ', 'ュ', 'ユ', 'ョ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ン', 'ヴ', '・', 'ー', 'ㅡ', '一', '丁', '三', '上', '世', '中', '丸', '主', '乙', '乳', '事', '二', '京', '人', '介', '仕', '他', '付', '代', '仰', '仲', '任', '会', '伝', '似', '体', '何', '佗', '作', '侠', '係', '俗', '俺', '倒', '側', '偽', '催', '僕', '優', '兄', '先', '光', '入', '八', '共', '内', '冷', '出', '刊', '初', '刺', '刻', '剑', '力', '動', '勝', '募', '勧', '化', '医', '印', '厚', '原', '去', '又', '友', '取', '受', '古', '史', '合', '吉', '同', '向', '君', '吸', '周', '命', '和', '咥', '咬', '唸', '問', '嘘', '器', '回', '図', '国', '園', '城', '堕', '墓', '士', '変', '夏', '外', '夜', '夢', '大', '天', '太', '奇', '奥', '奮', '女', '好', '妄', '娼', '婚', '婦', '嫁', '嫌', '子', '季', '学', '孫', '守', '完', '官', '宝', '実', '客', '室', '宴', '家', '寄', '密', '尊', '小', '少', '尿', '屋', '巨', '巻', '巾', '師', '帰', '干', '年', '幸', '底', '店', '度', '引', '弘', '弟', '張', '形', '彼', '待', '後', '徒', '御', '復', '心', '快', '怒', '思', '急', '恋', '恥', '患', '悪', '情', '惑', '想', '愁', '意', '愛', '態', '憂', '成', '戦', '手', '才', '打', '抱', '押', '拷', '持', '指', '挿', '捨', '授', '損', '摘', '擦', '攻', '放', '教', '散', '敬', '文', '方', '旅', '族', '日', '旺', '明', '昏', '星', '春', '昭', '昼', '時', '暑', '暗', '書', '曹', '替', '最', '月', '有', '期', '木', '未', '本', '束', '来', '東', '板', '果', '枯', '某', '染', '校', '桃', '桜', '森', '棲', '極', '楽', '様', '模', '権', '樹', '欲', '正', '歴', '死', '残', '段', '殺', '毒', '比', '氏', '民', '氓', '気', '水', '汁', '決', '治', '注', '泰', '活', '流', '浴', '海', '涙', '淫', '深', '清', '渚', '漂', '演', '漫', '潔', '激', '濁', '濃', '瀬', '火', '灵', '炎', '無', '煉', '熟', '熱', '燦', '爛', '物', '状', '猫', '獄', '獣', '玉', '王', '甘', '生', '田', '男', '界', '番', '疑', '病', '痛', '療', '発', '白', '百', '盛', '目', '真', '眠', '着', '矢', '知', '石', '研', '破', '硬', '祐', '神', '福', '禰', '私', '秋', '科', '秘', '称', '稲', '稿', '穏', '究', '窓', '立', '童', '節', '米', '粋', '純', '紹', '終', '絆', '結', '絡', '綴', '緊', '締', '編', '練', '縁', '縛', '罪', '美', '羞', '者', '聖', '聞', '聴', '肉', '育', '背', '能', '脅', '腐', '腫', '腰', '自', '舎', '舞', '色', '花', '若', '茎', '草', '華', '落', '著', '薄', '薬', '藍', '虎', '虔', '虫', '蜜', '血', '行', '術', '街', '衝', '裏', '裸', '要', '覆', '見', '視', '覚', '覧', '触', '言', '記', '試', '詩', '話', '誘', '課', '談', '謎', '貌', '貞', '負', '贈', '贖', '赤', '超', '足', '路', '踏', '身', '車', '軋', '較', '輝', '輩', '農', '辺', '込', '迷', '迸', '追', '送', '逆', '透', '逢', '連', '週', '遊', '過', '道', '違', '遥', '郎', '部', '酒', '酔', '醒', '野', '金', '鉄', '録', '長', '門', '開', '間', '関', '闇', '闘', '门', '陰', '階', '雄', '集', '雪', '電', '霊', '青', '面', '音', '頬', '頭', '顔', '願', '類', '飲', '香', '馬', '駆', '験', '高', '鬱', '鬼', '魂', '鹿', '麻', '黒', '龍', '龙', '박', '사', '카', '프', '︎', '\ufeff', '！', '（', '）', '，', '－', '／', '１', '２', '６', '？', '［', '～', '｢', '｣', '�']


# Constants for the model
TITLE_VOCAB_SIZE = 205
SYNOPSIS_VOCAB_SIZE = 844
TITLE_AND_SYNOPSIS_VOCAB_SIZE = 870
EMBEDDING_DIM = 384
RNN_UNITS = 768


def mapping_creation(vocab):
    # Creating a mapping from unique characters to indices
    char2idx = {u: i for i, u in enumerate(vocab)}

    # Creating a mapping from indices to unique characters
    idx2char = np.array(vocab)

    return char2idx, idx2char


title_char2idx, title_idx2char = mapping_creation(TITLE_VOCAB)
synopsis_char2idx, synopsis_idx2char = mapping_creation(SYNOPSIS_VOCAB)
title_and_synopsis_char2idx, title_and_synopsis_idx2char = mapping_creation(TITLE_AND_SYNOPSIS_VOCAB)


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        tf.keras.layers.Dropout(0.22),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.22),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.22),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dropout(0.18),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model


def prediction_engine(engine_type="Title", version=999):
    if engine_type == "Title":
        if version == 1:
            weights = './engine/ckpts/title-model/v1_ckpt_25'
        elif version == 2:
            weights = './engine/ckpts/title-model/v2_ckpt_5'
        elif version == 3:
            weights = './engine/ckpts/title-model/v3_ckpt_10'
        else:
            weights = tf.train.latest_checkpoint('./engine/ckpts/title-model')

        engine = build_model(TITLE_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)

    elif engine_type == "Synopsis":

        if version == 1:
            weights = './engine/ckpts/synopsis-model/v1_ckpt_10'
        elif version == 2:
            weights = './engine/ckpts/synopsis-model/v2_ckpt_5'
        elif version == 3:
            weights = './engine/ckpts/synopsis-model/v3_ckpt_15'
        else:
            weights = tf.train.latest_checkpoint('./engine/ckpts/synopsis-model')

        engine = build_model(SYNOPSIS_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)

    else:

        if version == 1:
            weights = './engine/ckpts/title-and-synopsis-model/v1_ckpt_10'
        elif version == 2:
            weights = './engine/ckpts/title-and-synopsis-model/v2_ckpt_5'
        elif version == 3:
            weights = './engine/ckpts/title-and-synopsis-model/v3_ckpt_15'
        else:
            weights = tf.train.latest_checkpoint('./engine/ckpts/title-and-synopsis-model')

        engine = build_model(TITLE_AND_SYNOPSIS_VOCAB_SIZE, EMBEDDING_DIM, RNN_UNITS, batch_size=1)

    engine.load_weights(weights)
    engine.build(tf.TensorShape([1, None]))

    return engine_type, engine


def generate_text(engine, start_string="", temp=0.7, num_generate=400):
    if start_string == "":
        start_string = word_generator.get_random_word().capitalize()

    start_string = " ~ " + start_string

    if engine[0] == "Title":
        char2idx = title_char2idx
        idx2char = title_idx2char
    elif engine[0] == "Synopsis":
        char2idx = synopsis_char2idx
        idx2char = synopsis_idx2char
    elif engine[0] == "Title_and_Synopsis":
        char2idx = title_and_synopsis_char2idx
        idx2char = title_and_synopsis_idx2char
    else:
        return

    model = engine[1]

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
        output = [x.strip() for x in output_string.split("~")]
    return output


def init():
    global title_engine, synopsis_engine, title_and_synopsis_engine, real_titles

    title_engine = prediction_engine(engine_type="Title", version=3)
    synopsis_engine = prediction_engine(engine_type="Synopsis", version=3)
    title_and_synopsis_engine = prediction_engine(engine_type="Title_and_Synopsis", version=3)

    with open("./engine/txt_files/real_titles.txt", encoding="utf-8") as f:
        real_titles = f.readlines()
        real_titles = [x.strip() for x in real_titles]


# request model prediction
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    init()

    anigen_titles = generate_text(engine=title_engine, start_string="", temp=0.75, num_generate=1000)
    anigen_titles = anigen_titles[1:]

    original_length = len(anigen_titles)
    anigen_titles = [x for x in anigen_titles if x not in real_titles]
    dropped_titles = original_length - len(anigen_titles)

    anigen_title_dict = dict(zip(range(1, len(anigen_titles)), anigen_titles))
    data = {'number_of_dropped_titles': dropped_titles,
            'anigen_title_count': original_length-dropped_titles,
            'anigen_titles': anigen_title_dict}

    return data
