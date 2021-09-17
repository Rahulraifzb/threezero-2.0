from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        "setter",
        "title",
        "status",
        "date_added"
    ]

class MultipleChoiceAnswerInlineModel(admin.TabularInline):
    model = MultipleChoiceAnswer
    fields = ["answer"]


@admin.register(MultipleChoice)
class MultipleChoiceAdmin(admin.ModelAdmin):
    fields = [
        "question"
    ]

    

admin.site.register(QuizInstance)
admin.site.register(UserResponse)

