from django.urls import path
from . import views

app_name = 'assessment_api' # Optional: for namespacing URLs

urlpatterns = [
    path('questions/', views.question_list_create_api, name='question-list-create'),
    path('submit_answer/', views.submit_answer_api, name='submit-answer'),
    path('predict_difficulty/', views.predict_difficulty_api, name='predict-difficulty'),
]