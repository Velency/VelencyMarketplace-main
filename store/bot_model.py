from .data import load_dialogue_database_from_json
from gensim.models import Word2Vec
import numpy as np
import json
import Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_dialogue_database(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            dialogue_database = json.load(file)
    except FileNotFoundError:
        dialogue_database = {}
    # Приведение ключей к нижнему регистру
    dialogue_database = {question.lower(): answers for question, answers in dialogue_database.items()}
    return dialogue_database


def save_dialogue_database(dialogue_database, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dialogue_database, file, ensure_ascii=False, indent=4)




def generate_response(user_input, dialogue_database):
    # Приводим входной текст к нижнему регистру
    user_input = user_input.lower()  
    
    # Проверяем, начинается ли входное сообщение с ключевого слова "запомни"
    if user_input.startswith("запомни"):
        # Извлекаем вопрос и ответ из сообщения
        question_answer = user_input.split("запомни", 1)[1].strip()
        # Проверяем, присутствует ли фраза "тебя спросят" во входной строке
        if "тебя спросят" in question_answer:
            question, answer = question_answer.split("тебя спросят", 1)
            # Вызываем функцию remember_dialogue
            remember_dialogue(question.strip(), answer.strip(), dialogue_database)
            return "Я запомнил этот диалог."
        else:
            return "Фраза 'тебя спросят' отсутствует в вашем запросе."

    # Собираем все фразы из базы данных
    all_phrases = list(dialogue_database.keys())

    # Добавляем входную фразу в список
    all_phrases.append(user_input)

    # Создаем матрицу TF-IDF для всех фраз
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_phrases)

    # Вычисляем косинусное сходство между входной фразой и всеми фразами из базы данных
    similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])

    # Находим наиболее похожую фразу
    max_similarity_index = np.argmax(similarities)
    max_similarity = similarities[0][max_similarity_index]

    # Если сходство больше некоторого порога, возвращаем ответ из базы данных
    if max_similarity > 0.5:  # Пример порога
        return np.random.choice(dialogue_database[all_phrases[max_similarity_index]])
    else:
        return "Простите, я не могу понять ваш запрос или у меня нет ответа на него."


    # Проверяем, есть ли точное совпадение в базе данных
    if user_input in dialogue_database:
        responses.extend(dialogue_database[user_input])

    # Если нет точного совпадения, попробуем найти наиболее близкие запросы по расстоянию Левенштейна
    if not responses:
        for question, answers in dialogue_database.items():
            if Levenshtein.distance(user_input, question) <= 2:  # Подберите подходящий порог
                responses.extend(answers)

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

