from django.contrib import admin
from .models import Question, Submission

# Register your models here.
admin.site.register(Question)
admin.site.register(Submission)