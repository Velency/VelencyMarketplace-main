from .models import Trigger
import random

class ChatBot:
    @staticmethod
    def generate_response(user_input):
        trigger = Trigger.objects.filter(keywords__icontains=user_input).first()

        if trigger:
            return trigger.get_random_response()

        # Ваша текущая логика генерации ответа
        return "На Ваш запрос: {}, пока не могу ничего ответить, но я учусь!".format(user_input)