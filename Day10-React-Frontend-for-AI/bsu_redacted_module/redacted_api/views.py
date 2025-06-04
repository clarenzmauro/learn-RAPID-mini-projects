import joblib
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt # For simplicity in testing POST
import json # To parse JSON from request body

from .models import Question, Submission

# load the model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'difficulty_prediction_pipeline.joblib')

DIFFICULTY_MODEL_PIPELINE = None
try:
    DIFFICULTY_MODEL_PIPELINE = joblib.load(MODEL_PATH)
    print(f"Successfully loaded difficulty prediction model from {MODEL_PATH}")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_PATH}. Ensure it's copied into the Docker image.")
    DIFFICULTY_MODEL_PIPELINE = None # Explicitly set to None
except Exception as e:
    print(f"Error loading model: {e}")
    DIFFICULTY_MODEL_PIPELINE = None # Explicitly set to None

@csrf_exempt # Only for testing with tools like curl/Postman easily.
             # In a real React app, Django's CSRF protection would be handled.
def question_list_create_api(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        data = []
        for question in questions:
            data.append({
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'difficulty_level': question.difficulty_level,
                'created_at': question.created_at.isoformat(), # Format datetime
            })
        return JsonResponse(data, safe=False) # safe=False for list responses

    elif request.method == 'POST':
        # This is a placeholder if you wanted to create questions via API
        # For today, we're focusing on GET questions and POST submissions
        try:
            body = json.loads(request.body)
            question_text = body.get('question_text')
            question_type = body.get('question_type')
            difficulty_level = body.get('difficulty_level', 1)

            if not question_text or not question_type:
                return HttpResponseBadRequest("Missing question_text or question_type")

            question = Question.objects.create(
                question_text=question_text,
                question_type=question_type,
                difficulty_level=difficulty_level
            )
            return JsonResponse({
                'id': question.id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'difficulty_level': question.difficulty_level
            }, status=201) # 201 Created
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt # Again, for easier testing of POST requests.
def submit_answer_api(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8')) # Decode body then parse
            question_id = body.get('question_id')
            student_identifier = body.get('student_identifier')
            answer_text = body.get('answer_text')

            if not all([question_id, student_identifier, answer_text]):
                return HttpResponseBadRequest("Missing question_id, student_identifier, or answer_text")

            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'error': 'Question not found'}, status=404)

            submission = Submission.objects.create(
                question=question,
                student_identifier=student_identifier,
                answer_text=answer_text
                # Score will be null by default
            )
            return JsonResponse({
                'id': submission.id,
                'question_id': submission.question.id,
                'student_identifier': submission.student_identifier,
                'answer_text': submission.answer_text,
                'submitted_at': submission.submitted_at.isoformat()
            }, status=201) # 201 Created

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data in request body.")
        except Exception as e:
            # Log the exception e for debugging
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is allowed for this endpoint.'}, status=405)

@csrf_exempt # For easier testing
def predict_difficulty_api(request):
    if request.method == 'POST':
        if DIFFICULTY_MODEL_PIPELINE is None:
            return JsonResponse({'error': 'Model not loaded. Check server logs.'}, status=500)

        try:
            body = json.loads(request.body.decode('utf-8'))
            question_text = body.get('question_text')

            if not question_text:
                return JsonResponse({'error': 'Missing question_text in request body.'}, status=400)

            # The model pipeline expects a list or iterable of texts
            # Even if it's just one, pass it as a list-like structure
            prediction = DIFFICULTY_MODEL_PIPELINE.predict([question_text])

            # prediction will be an array (e.g., numpy array), get the first element
            predicted_difficulty = int(prediction[0]) # Convert to standard Python int

            return JsonResponse({
                'question_text': question_text,
                'predicted_difficulty': predicted_difficulty
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in request body.'}, status=400)
        except Exception as e:
            # Log the exception e for debugging
            print(f"Error during prediction: {e}")
            return JsonResponse({'error': f'An error occurred during prediction: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)