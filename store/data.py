import json
from keras.preprocessing.text import Tokenizer
import numpy as np

def load_dialogue_database_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    dialogue_database = {}
    for question, answers in data.items():
        dialogue_database[question] = answers
    return dialogue_database

# Загрузка базы данных из JSON файла
dialogue_database = load_dialogue_database_from_json('dialogue_database.json')

# Токенизация текста
tokenizer = Tokenizer()
tokenizer.fit_on_texts(dialogue_database)
texts = [item for sublist in dialogue_database.values() for item in sublist]

# Преобразование текста в числовые последовательности
sequences = tokenizer.texts_to_sequences(dialogue_database)

# Преобразование последовательностей в массивы numpy
X = []
y = []
for seq in sequences:
    X.append(seq[:-1])
    y.append(seq[-1])
X = np.array(X)
y = np.array(y)

# Разделение на обучающий и тестовый наборы
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Определение переменных
vocab_size = len(tokenizer.word_index) + 1  # Размер словаря
max_sequence_length = max([len(seq) for seq in X_train])  # Максимальная длина последовательности вопроса
embedding_dim = 100  # Размерность векторов вложений
lstm_units = 256  # Количество нейронов в слое LSTM
