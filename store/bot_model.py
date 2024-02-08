from .data import load_dialogue_database_from_json
from gensim.models import Word2Vec
import numpy as np
import json



def load_dialogue_database(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            dialogue_database = json.load(file)
    except FileNotFoundError:
        dialogue_database = {}
    return dialogue_database

def save_dialogue_database(dialogue_database, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dialogue_database, file, ensure_ascii=False, indent=4)



def generate_response(word2vec_model, user_input, dialogue_database):
    # Разбиваем вход пользователя на слова
    user_input_tokens = user_input.lower().split()
    
    # Проверяем, начинается ли входное сообщение с ключевого слова "запомни"
    if user_input.startswith("Запомни"):
        # Извлекаем вопрос и ответ из сообщения
        question_answer = user_input.split("Запомни", 1)[1].strip()
        # Проверяем, присутствует ли фраза "тебя спросят" во входной строке
        if "тебя спросят" in question_answer:
            question, answer = question_answer.split("тебя спросят", 1)
            # Вызываем функцию remember_dialogue
            remember_dialogue(question.strip(), answer.strip(), dialogue_database)
            return "Я запомнил этот диалог."
        else:
            return "Фраза 'тебя спросят' отсутствует в вашем запросе."
    
    # Проверяем, есть ли вопрос в базе данных
    if user_input in dialogue_database:
        # Если есть несколько ответов на вопрос, выбираем один случайным образом
        return np.random.choice(dialogue_database[user_input])
    
    # Ищем наиболее похожие слова в модели Word2Vec
    similar_words = []
    for word in user_input_tokens:
        if word in word2vec_model.wv.key_to_index:
            similar_words.extend(word2vec_model.wv.most_similar(word, topn=3))  # Поиск 3 наиболее похожих слов
    # Выбираем ответ из базы данных, если найдены похожие слова
    responses = []
    for word, similarity in similar_words:
        if word in dialogue_database:
            responses.extend(dialogue_database[word])
    if responses:
        return np.random.choice(responses)
    else:
        return "Простите, я не могу понять ваш запрос или у меня нет ответа на него."


def recognize_question(user_input, dialogue_database):
    # Эта функция остается без изменений, так как она не зависит от выбранной модели
    for question in dialogue_database:
        if question in user_input:
            return question
    return None

def remember_dialogue(question, answer, dialogue_database):
    # Эта функция остается без изменений, так как она не зависит от выбранной модели
    print("Запомнил вопрос:", question)
    print("Запомнил ответ:", answer)
    if question in dialogue_database:
        # Если вопрос уже существует в базе данных, добавляем новый ответ к списку существующих ответов
        dialogue_database[question].append(answer)
    else:
        # Если вопроса нет в базе данных, создаем новую запись
        dialogue_database[question] = [answer]
    save_dialogue_database(dialogue_database, 'dialogue_database.json')

# Загрузка модели Word2Vec
word2vec_model = Word2Vec.load('word2vec.bin')

# Загрузка базы данных из JSON файла
dialogue_database = load_dialogue_database('dialogue_database.json')

# Остальные параметры модели LSTM (не нужны для Word2Vec)
vocab_size = None
max_sequence_length = None
embedding_dim = None
lstm_units = None

# Необходимо также создать заглушку для компиляции модели, так как она не требуется для Word2Vec
def compile_model(model):
    pass

