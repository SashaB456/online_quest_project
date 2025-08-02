from django.urls import include, path
from .views import QuizList, QuizCreate, QuizDelete, Challenge, play_quiz, results, QuizEdit, GetUserProfile
urlpatterns = [
    path('quiz_list/', QuizList.as_view(), name='quiz-list'),
    path('quiz_create/', QuizCreate.as_view(), name='quiz-create'),
    path('quiz_edit/<int:pk>/', QuizEdit.as_view(), name='quiz-edit'),
    path('quiz_delete/<int:pk>/', QuizDelete.as_view(), name='quiz-delete'),
    path('challenge/<int:quiz_id>/', Challenge, name='challenge'),
    path('play_quiz/<int:quiz_id>/<int:question_number>', play_quiz, name='play-quiz'),
    path('results/<int:quiz_id>/', results, name='results'),
    path('user_profile/<int:pk>/', GetUserProfile.as_view(), name='user-profile'),
]