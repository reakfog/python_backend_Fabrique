from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

# -- Survey table ------------------------------------------------------------
def in_duration_day():
    return now() + timedelta(days=settings.DEFAULT_SURVEY_PUBLISHING_DURATION)


class Survey(models.Model):
    title = models.CharField(
        _('Title'), max_length = 300)
    description = models.TextField(
        _('Description'))
    start_date = models.DateField(
        _('Publication date'),
        blank=True,
        null=False,
        default=now)
    end_date = models.DateField(
        _('Expiration date'),
        blank=True,
        null=False,
        default=in_duration_day)
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='surveys')
    
    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')
        ordering = ('-start_date',)


# -- Question table ----------------------------------------------------------
CHOICES_HELP_TEXT = _(
    'The choices field is only used if the question type '
    'is "select-single" or "select multiple" provide a '
    'comma-separated list of options for this question.')


def validate_choices(choices):
    values = choices.split(settings.CHOICES_SEPARATOR)
    empty = 0
    for value in values:
        if value.replace(' ', '') == '':
            empty += 1
    if len(values) < 2 + empty:
        msg = (
            'The selected field requires an associated list of choices. '
            'Choices must contain more than one item.')
        raise ValidationError(msg)


class Question(models.Model):

    TEXT = 'text'
    SELECT_SINGLE = 'select-single'
    SELECT_MULTIPLE = 'select-multiple'

    ANSWERS_TYPES = (
        (TEXT, _('text')),
        (SELECT_SINGLE, _('select single')),
        (SELECT_MULTIPLE, _('select multiple')),
    )

    text = models.TextField()
    answer_type = models.CharField(
        _('Type'),
        max_length=200,
        choices=ANSWERS_TYPES,
        default=TEXT)
    answer_choices = models.TextField(
        _('Choices'),
        blank=True,
        null=True,
        help_text=CHOICES_HELP_TEXT)
    survey = models.ForeignKey(
        Survey,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_('Survey'),
        related_name='questions')
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.SET(get_sentinel_user),
        verbose_name=_('User'),
        related_name='questions')

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ('-survey',)

    def save(self, *args, **kwargs):
        if self.answer_type in [
                Question.SELECT_SINGLE,
                Question.SELECT_MULTIPLE
            ]:
            validate_choices(self.answer_choices)
        super(Question, self).save(*args, **kwargs)


# -- Answers table -------------------------------------------------------
class Answer(models.Model):
    text = models.TextField()
    anonimously = models.BooleanField(
        blank=False,
        default=False)
    question = models.ForeignKey(
        'Question',
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_('Question'),
        related_name='answers')
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='answers')

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
        ordering = ('-question',)
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'author'],
                name='unique_author_answer_key')
        ]
