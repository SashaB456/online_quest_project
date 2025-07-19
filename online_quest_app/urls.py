from django.urls import include, path
from .views import QuizList, QuizDetail, QuizCreate, QuizDelete, Challenge, play_quiz, results
urlpatterns = [
    path('quiz_list/', QuizList.as_view(), name='quiz-list'),
    path('quiz_detail/<int:pk>', QuizDetail.as_view(), name='quiz-detail'),
    path('quiz_create/', QuizCreate.as_view(), name='quiz-create'),
    path('quiz_delete/<int:pk>/', QuizDelete.as_view(), name='quiz-delete'),
    path('challenge/<int:quiz_id>/', Challenge, name='challenge'),
    path('play_quiz/<int:quiz_id>/<int:question_number>', play_quiz, name='play-quiz'),
    path('results/<int:quiz_id>/', results, name='results'),
]