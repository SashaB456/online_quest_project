from django.urls import include, path
from .views import QuizList, QuizCreate, QuestionCreate, UserProfileList, QuizDelete, QuestionDelete, QuestionEdit, Challenge, play_quiz, results, QuizEdit, GetUserProfile, UpdateUserProfile, QuestionList
urlpatterns = [
    path('', QuizList.as_view()),
    path('quiz_list/', QuizList.as_view(), name='quiz-list'),
    path('question_list/', QuestionList, name='question-list'),
    path('question_edit/<int:pk>', QuestionEdit.as_view(), name='question-edit'),
    path('question_delete/<int:pk>', QuestionDelete.as_view(), name='question-delete'),
    path('quiz_create/', QuizCreate.as_view(), name='quiz-create'),
    path('question_create/', QuestionCreate.as_view(), name='question-create'),
    path('quiz_edit/<int:pk>/', QuizEdit.as_view(), name='quiz-edit'),
    path('quiz_delete/<int:pk>/', QuizDelete.as_view(), name='quiz-delete'),
    path('challenge/<int:quiz_id>/', Challenge, name='challenge'),
    path('play_quiz/<int:quiz_id>/<int:question_number>', play_quiz, name='play-quiz'),
    path('results/<int:quiz_id>/', results, name='results'),
    path('user_profile/<int:pk>/', GetUserProfile.as_view(), name='user-profile'),
    path('profile_list/', UserProfileList.as_view(), name='profile-list'),
    path('user_profile/update/<int:pk>/', UpdateUserProfile.as_view(), name='user-profile-update'),
]