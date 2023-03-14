import spacy
from sklearn.datasets import fetch_20newsgroups
import tensorflow as tf

from nltk.corpus import stopwords

from collections import Counter


def get_word_2_index(vocab):
    word2index = {}
    for i,word in enumerate(vocab):
        word2index[word] = i

    return word2index


def preproc_text(text_series, stop_words):
    new_texts = {}
    for idx, text in text_series:
        for lemmatized_text in spacy.load('ru_core_news_sm').pipe(text):
            new_texts[idx] = ' '.join(
                [tok.lemma_.lower() for tok in lemmatized_text
                 if tok.lemma_.lower() not in stop_words
                 and len(tok.lemma_) > 2]
            )

    return new_texts


def get_all_vocab(texts):
    vocab = Counter()
    for text in texts:
        for word in text.split(' '):
            vocab[word] += 1

    return vocab


def train_nn():
    input_tensor = tf.placeholder(tf.float32,[None, n_input], name="input")
    output_tensor = tf.placeholder(tf.float32,[None, n_classes], name="output")

    training_epochs = 10
    batch_size = 30
    # Запуск графа
    with tf.Session() as sess:
        sess.run()  # инициализация нормальным распределением

        # Тренировочный цикл
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(len(newsgroups_train.data) / batch_size)
            # Цикл по всем блокам
            for i in range(total_batch):
                batch_x, batch_y = get_batch(newsgroups_train, i, batch_size)
                # Запустим оптимизацию
                c, _ = sess.run([loss, optimizer],
                                feed_dict={input_tensor: batch_x,
                                           output_tensor: batch_y})


if __name__ == '__main__':
    newsgroups_train = fetch_20newsgroups(subset='train')
    newsgroups_test = fetch_20newsgroups(subset='test')
    stop_words = set(stopwords.words('russian'))

    # TODO перевести датасет новостной на рус. яз

    lemmatized_train = preproc_text(newsgroups_train, stop_words)
    vocab = get_all_vocab(lemmatized_train)

    # Параметры сети
    n_hidden_1 = 10  # количество признаков первого слоя
    n_hidden_2 = 5  # количество признаков второго слоя
    n_input = len(vocab)  # Слова в словаре
    n_classes = 20  # Категории


