from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.TextField()
    # example: 'multiple choice', 'fill in the blank', 'short answer', 'essay'
    question_type = models.CharField(max_length=50)
    # example: 1 easy, 2 medium, 3 hard
    difficulty_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text[:50] # shows first 50 chars in admin
    
class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='submissions')
    student_identifier = models.CharField(max_length=100)
    answer_text = models.TextField()
    score = models.FloatField(null=True, blank=True) 
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student_identifier} for Q: {self.question.id}"
    
# this defines two models: question and submission.