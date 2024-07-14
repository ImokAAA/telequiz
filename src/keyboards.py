from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.quizes.crud import get_user_quizes_name, get_quiz_by_name
from src.questions.crud import get_quiz_questions, get_question_by_id
from src.answers.crud import get_question_answers_name, get_answer_by_id
from src.play.crud import get_answers_by_question_id, get_question_by_quiz_name_and_index

from models import get_db

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои квизы', callback_data='quizes')],
    [InlineKeyboardButton(text='Мои данные', callback_data='personal')],
    [InlineKeyboardButton(text='Играть', callback_data='play')]
    ]
)

async def inline_quizes(telegram_id:int):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        quizes = await get_user_quizes_name(session=sess, telegram_id=telegram_id)
    keyboard.add(InlineKeyboardButton(text="Назад", \
                                        callback_data=f'main')
                )
    for quiz in quizes:
        keyboard.add(InlineKeyboardButton(text=quiz, \
                                          callback_data=f'quiz_info_{quiz}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play(telegram_id:int):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        quizes = await get_user_quizes_name(session=sess, telegram_id=telegram_id)
    keyboard.add(InlineKeyboardButton(text="Назад", \
                                        callback_data=f'main')
                )
    for quiz in quizes:
        keyboard.add(InlineKeyboardButton(text=quiz, \
                                          callback_data=f'quiz_play_{quiz}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play_question(question_id:int):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        answers = await get_answers_by_question_id(session= sess, question_id=question_id)
    keyboard.add(InlineKeyboardButton(text="Выйти", \
                                        callback_data=f'main')
                )
    for answer in answers:
        keyboard.add(InlineKeyboardButton(text=answer.name, \
                                          callback_data=f'answer_check_{answer.id}_{question_id}')
                     )
    return keyboard.adjust(2).as_markup()

async def inline_quizes_play_question_result(question_id:int, answer_id:int):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        answers = await get_answers_by_question_id(session= sess, question_id=question_id)
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

async def inline_quiz_menu(quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        quiz = await get_quiz_by_name(session=sess, name=quiz_name)
    
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

async def inline_questions(quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        questions = await get_quiz_questions(session=sess, quiz_name=quiz_name)
    
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

async def inline_question_menu(question_id:int, quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        question = await get_question_by_id(session=sess, id=question_id)
    
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

async def inline_answers(question_id:int, quiz_name:str):
    keyboard = InlineKeyboardBuilder()
    async for sess in get_db():
        answers = await get_question_answers_name(session=sess, question_id=question_id)
    
    keyboard.add(InlineKeyboardButton(text="Добавить ответ", \
                                          callback_data=f'answer_add_{question_id}_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="Выбрать правильный ответ", \
                                          callback_data=f'answer_correct_{question_id}_{quiz_name}')
                )
    keyboard.add(InlineKeyboardButton(text="<Назад", \
                                          callback_data=f'question_info_{question_id}_{quiz_name}')
                )
    for answer in answers:
        keyboard.add(InlineKeyboardButton(text=answer, \
                                          callback_data=f'answer_info_{answer}')
                     )
    return keyboard.adjust(2).as_markup()