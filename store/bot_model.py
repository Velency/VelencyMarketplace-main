import tensorflow_hub as hub
import numpy as np
import json

# Загрузка базы данных из JSON файла
def load_dialogue_database(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            dialogue_database = json.load(file)
    except FileNotFoundError:
        dialogue_database = {}
    # Приведение ключей к нижнему регистру
    dialogue_database = {question.lower(): answers for question, answers in dialogue_database.items()}
    return dialogue_database

# Загрузка Universal Sentence Encoder
def load_universal_sentence_encoder():
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

# Вычисление сходства между запросом пользователя и базой данных бота
def calculate_similarity(user_input, dialogue_database, use_model):
    user_embeddings = use_model([user_input])
    dialogue_embeddings = use_model(list(dialogue_database.keys()))
    similarities = np.inner(user_embeddings, dialogue_embeddings)
    return similarities.flatten()


# Сохранение базы данных в JSON файле
def save_dialogue_database(dialogue_database, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(dialogue_database, file, ensure_ascii=False, indent=4)

# Генерация ответа на запрос пользователя
def generate_response(user_input, dialogue_database, use_model):

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
        
    similarities = calculate_similarity(user_input, dialogue_database, use_model)
    max_index = np.argmax(similarities)
    max_similarity = similarities[max_index]
    threshold = 0.2  # Порог сходства (можно настраивать)
    if max_similarity >= threshold:
        question = list(dialogue_database.keys())[max_index]
        return np.random.choice(dialogue_database[question])
    else:
        return "Простите, я не могу понять ваш запрос или у меня нет ответа на него."
    
# Запоминание диалога
def remember_dialogue(question, answer, dialogue_database):
    # Приведение ключа (вопроса) к нижнему регистру
    question = question.lower()
    # Если вопрос уже существует в базе данных, добавляем новый ответ к списку существующих ответов
    if question in dialogue_database:
        dialogue_database[question].append(answer)
    else:
        # Если вопроса нет в базе данных, создаем новую запись
        dialogue_database[question] = [answer]
    # Сохраняем обновленную базу данных
    save_dialogue_database(dialogue_database, 'dialogue_database.json')

# Загрузка базы данных
dialogue_database = load_dialogue_database('dialogue_database.json')

# Загрузка Universal Sentence Encoder
use_model = load_universal_sentence_encoder()

# Пример запроса пользователя
user_input = "расскажи про погоду"

# Генерация ответа на запрос пользователя
response = generate_response(user_input, dialogue_database, use_model)
print("Ответ бота:", response)
