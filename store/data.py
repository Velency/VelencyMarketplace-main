from gensim.models import Word2Vec
import json
import numpy as np

def load_dialogue_database_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dialogue_database = json.load(file)
    return dialogue_database

# Загрузка базы данных из JSON файла
dialogue_database = load_dialogue_database_from_json('dialogue_database.json')

# Обучение модели Word2Vec на текстовых данных из базы диалогов
sentences = [sentence.split() for answers in dialogue_database.values() for sentence in answers]
word2vec_model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=1)

# Сохранение модели Word2Vec в файл (если нужно)
word2vec_model.save("word2vec_model.bin")



# Загрузка обученной модели Word2Vec (если необходимо)
# word2vec_model = Word2Vec.load("word2vec_model.bin")
