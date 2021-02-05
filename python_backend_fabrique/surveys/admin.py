from django.contrib import admin
from .models import Survey, Question, Answer


class SurveyAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
        'start_date',
        'end_date',
        'author')
    search_fields = ('title',) 
    list_filter = ('start_date',)
    empty_value_display = '-empty-'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['start_date']
        return self.readonly_fields


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'survey',
        'pk',
        'text',
        'answer_type',
        'answer_choices',) 
    search_fields = ('title',) 
    list_filter = ('survey',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'anonimously',
        'question',
        'pk',
        'author',) 
    search_fields = ('text',) 
    list_filter = ('question','author',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)