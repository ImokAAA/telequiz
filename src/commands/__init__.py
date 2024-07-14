from .basic_commands import router as start_router
from .quiz_create import router as quiz_create_router
from .questions import router as questions_router
from .answers import router as answers_router
from .play_commands import router as play_router

routers_list = [start_router, quiz_create_router, questions_router, answers_router, play_router]