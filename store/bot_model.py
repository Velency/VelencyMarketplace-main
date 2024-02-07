# В файле bot_model.py
from .data import tokenizer, load_dialogue_database_from_json
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
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

def create_model(vocab_size, max_sequence_length, embedding_dim, lstm_units):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length))
    model.add(LSTM(units=lstm_units))
    model.add(Dense(vocab_size, activation='softmax'))
    return model

def pad_or_trim_sequence(sequence, max_length):
    if len(sequence) < max_length:
        # Если длина последовательности меньше максимальной, дополняем нулями
        padded_sequence = sequence + [0] * (max_length - len(sequence))
    else:
        # Если длина последовательности больше или равна максимальной, обрезаем до максимальной длины
        padded_sequence = sequence[:max_length]
    return padded_sequence

def generate_response(model, tokenizer, user_input, max_sequence_length, dialogue_database):
    # Отладочный вывод для проверки аргументов
    print("user_input:", user_input)

    # Проверяем, начинается ли входное сообщение с ключевого слова "запомни"
    if user_input.startswith("запомни"):
        # Извлекаем вопрос и ответ из сообщения
        question_answer = user_input.split("запомни", 1)[1].strip()
        # Проверяем, присутствует ли фраза "тебя спросят" во входной строке
        if "тебя спросят" in question_answer:
            question, answer = question_answer.split("тебя спросят", 1)
            # Отладочный вывод для проверки извлеченных вопроса и ответа
            print("question:", question.strip())
            print("answer:", answer.strip())

            # Вызываем функцию remember_dialogue
            remember_dialogue(question.strip(), answer.strip(), dialogue_database)
            return "Я запомнил этот диалог."
        else:
            return "Фраза 'тебя спросят' отсутствует в вашем запросе."
    
    # Проверяем, есть ли вопрос в базе данных
    if user_input in dialogue_database:
        # Если есть несколько ответов на вопрос, выбираем один случайным образом
        return np.random.choice(dialogue_database[user_input])
    print("Входной текст:", user_input)
    # Преобразование входного текста в последовательность чисел с помощью токенизатора
    input_sequence = tokenizer.texts_to_sequences([user_input])
    print("Числовая последовательность:", input_sequence)
    # Дополнение последовательности нулями или обрезка, чтобы достичь максимальной длины
    input_sequence = pad_or_trim_sequence(input_sequence[0], max_sequence_length)
    
    # Получение предсказания от модели
    predicted_id = np.argmax(model.predict(np.array([input_sequence])), axis=-1)[0]
    print("Предсказанный ID:", predicted_id)
    # Преобразование числа обратно в текст с помощью токенизатора
    bot_response = tokenizer.index_word.get(predicted_id, "Простите, я вас не понимаю или пока нет ответа на данное предложение.")
    print("Ответ бота:", bot_response)
    return bot_response


def recognize_question(user_input, dialogue_database):
    for question in dialogue_database:
        if question in user_input:
            return question
    return None

def remember_dialogue(question, answer, dialogue_database):
    print("Запомнил вопрос:", question)
    print("Запомнил ответ:", answer)
    if question in dialogue_database:
        # Если вопрос уже существует в базе данных, добавляем новый ответ к списку существующих ответов
        dialogue_database[question].append(answer)
    else:
        # Если вопроса нет в базе данных, создаем новую запись
        dialogue_database[question] = [answer]
    save_dialogue_database(dialogue_database, 'dialogue_database.json')



# Параметры модели
vocab_size = 10000  # Размер словаря
max_sequence_length = 20  # Максимальная длина последовательности вопроса
embedding_dim = 100  # Размерность векторов вложений
lstm_units = 256  # Количество нейронов в слое LSTM

# Создание модели
model = create_model(vocab_size, max_sequence_length, embedding_dim, lstm_units)

# Компиляция модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Вывод информации о модели
model.summary()
