from typing import Iterable

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.models import Quiz, Answer, Question, User

from models import get_db

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои квизы', callback_data='quizes')],
    [InlineKeyboardButton(text='Мои данные', callback_data='personal')],
    [InlineKeyboardButton(text='Играть', callback_data='play')]
    ]
)

async def inline_quizes(quiz_names: Iterable[str]):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Назад", \
                                        callback_data=f'main')
                )
    for quiz in quiz_names:
        keyboard.add(InlineKeyboardButton(text=quiz, \
                                          callback_data=f'quiz_info_{quiz}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play(quiz_names: Iterable[str]):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Назад", \
                                        callback_data=f'main')
                )
    for quiz in quiz_names:
        keyboard.add(InlineKeyboardButton(text=quiz, \
                                          callback_data=f'quiz_play_{quiz}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play_question(answers:Iterable[Answer]):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Выйти", \
                                        callback_data=f'main')
                )
    for answer in answers:
        keyboard.add(InlineKeyboardButton(text=answer.name, \
                                          callback_data=f'answer_check_{answer.id}_{answer.question_id}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play_question_result(answers:Iterable[Answer], answer_id:int, question_id:int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Выйти", \
                                        callback_data=f'main')
                )
    keyboard.add(InlineKeyboardButton(text="Продолжить", \
                                        callback_data=f'answer_play_{answer_id}_{question_id}')
                )
    for answer in answers:
        keyboard.add(InlineKeyboardButton(text=f"{answer.name} {answer.correct_answer}", \
                                          callback_data='qotaq')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quiz_menu(quiz:Quiz):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.add(InlineKeyboardButton(text="Вопросы", \
                                          callback_data=f'questions_{quiz.name}')
                )
    keyboard.add(InlineKeyboardButton(text="Поменять название", \
                                          callback_data=f'change_name_quiz_{quiz.name}')
                )
    keyboard.add(InlineKeyboardButton(text="Удалить", \
                                          callback_data=f'delete__quiz_{quiz.name}')
                )
    keyboard.add(InlineKeyboardButton(text="<Назад", \
                                          callback_data='quizes')
                )
    return keyboard.adjust(2).as_markup()

async def inline_questions(questions: Iterable[Question], quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Добавить вопрос", \
                                          callback_data=f'question_add_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="<Назад", \
                                          callback_data=f'quiz_info_{quiz_name}')
                )
    for question in questions:
        keyboard.add(InlineKeyboardButton(text=question.name, \
                                          callback_data=f'question_info_{question.id}_{quiz_name}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_question_menu(question:Question, quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Ответы", \
                                          callback_data=f'answers_{question.id}_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="Поменять название", \
                                          callback_data=f'change_name__question{question.id}')
                )
    keyboard.add(InlineKeyboardButton(text="Удалить", \
                                          callback_data=f'delete_question_{question.id}')
                )
    keyboard.add(InlineKeyboardButton(text="<Назад", \
                                          callback_data=f'questions_{quiz_name}')
                )
    return keyboard.adjust(2).as_markup()

async def inline_answers(answer_names:Iterable[str], question_id:int, quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Добавить ответ", \
                                          callback_data=f'answer_add_{question_id}_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="Выбрать правильный ответ", \
                                          callback_data=f'answer_correct_{question_id}_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="<Назад", \
                                          callback_data=f'question_info_{question_id}_{quiz_name}')
                )
    for answer in answer_names:
        keyboard.add(InlineKeyboardButton(text=answer, \
                                          callback_data=f'answer_info_{answer}')
                     )
    return keyboard.adjust(2).as_markup()