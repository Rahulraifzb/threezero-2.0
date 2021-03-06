'''
1.Add subjective and true or false questions
2.time per question and time for overall quiz
3.quiz settings
4.change order
5.reproduce a quiz already taken
6.garble from hidden values
7.change correct answer selection for a question
8.business rules - no of takes per quiz per user per month,no of instances a user can set per month,no of quizzes a user can set per month
9.quiz status
10.question explanation
11.should we checkin migrations folder??
12.user django polymorphic for question answer models
'''


from django.db import models
from django.template.defaultfilters import default, random, truncatewords_html
from taggit.managers import TaggableManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from dateutil.relativedelta import relativedelta
from datetime import date
from core.backend.quiz.exceptions import ScoreTamperedException

# Create your models here.


class MultipleChoiceAnswer(models.Model):
    '''A multichoice answer.'''
    answer = models.CharField(_('answer'),max_length=100)

    def __unicode__(self):
        return u"%s" %truncatewords_html(self.answer,10)

    def __str__(self):
        return f'{self.answer}'

class MultipleChoice(models.Model):
    '''multiple choice question with answer choices.'''
    question = models.CharField(_("question"),max_length=100)
    slug = models.SlugField(_("slug"))
    choices = models.ManyToManyField(MultipleChoiceAnswer)
    correct_answer = models.ManyToManyField(MultipleChoiceAnswer, related_name="correct", blank=True)
    categories = TaggableManager(blank=False)
    explanation = models.TextField(_('Explain your answer'),blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __unicode__(self):
        return u"%s" % truncatewords_html(self.question,10)


    def get_absolute_url(self):
        return ('quiz.views.question',[self.pk,self.slug])

class Quiz(models.Model):
    '''A quiz template.'''
    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Public")),
        (3,_("Close"))
    )

    FEEDBACK_CHOICES = (
        (1,_("At the end of the quiz")),
        (2,_("After each question")),
        (3,_("Don\'t disclose"))
    )

    TYPE_CHOICES = (
        (1,_("After Lecture")),
        (2,_("Assessment")),
        (3,_("Exam"))
    )

    NO_OF_TAKES_PER_MONTH_PER_USER = 3
    NO_OF_INSTANCES_PER_MONTH_PER_SETTER = 20
    setter = models.ForeignKey(User,related_name="setter",on_delete=models.CASCADE)
    title = models.CharField(_("title"),max_length=100)
    slug = models.SlugField(_("slug"))
    description = RichTextField(blank=True, null=True)
    status = models.IntegerField(_("status"),choices=STATUS_CHOICES,default=1)
    type = models.IntegerField(_("quiz type"),choices=TYPE_CHOICES,default=2)
    questions = models.ManyToManyField(MultipleChoice)
    categories = TaggableManager()
    published = models.DateTimeField(_("published"))
    date_added = models.DateTimeField(_("date added"),auto_now_add=True)
    date_modified = models.DateTimeField(_("date_modified"),auto_now_add=True)
    allow_skipping = models.BooleanField(default=False)
    allow_jumping = models.BooleanField(default=False)
    backwards_navigation = models.BooleanField(default=False)
    random_question = models.BooleanField(default=False)
    feedback = models.IntegerField(_('feedback'), choices=FEEDBACK_CHOICES, default=1)
    multiple_takes = models.BooleanField(default=False) # conditional
	# default must be global setting
    no_of_takes_per_month = models.IntegerField(_('no. of times this quiz can be taken by the candidate per month'),
						    default=NO_OF_TAKES_PER_MONTH_PER_USER)
    no_of_instances_per_month = models.IntegerField(_('no. of times this quiz can be taken by the candidate per month'),
						    default=NO_OF_INSTANCES_PER_MONTH_PER_SETTER)


    def __unicode__(self):
        return u"%s" % truncatewords_html(self.description,10)

    class Meta:
        verbose_name = _('quiz')
        verbose_name_plural = _('quizzes')
        db_table = 'quizzes'
        ordering = ('-published',)

    @property
    def question_count(self):
        return len(self.questions.all())

    @property
    def get_question(self,id):
        return self.questions.all()[id]

    @property
    def get_instances(self):
        return QuizInstance.objects.filter(quiz=self)

    @property
    def get_completed_instances(self):
        return this.get_instances.filter(complete=True)

    def get_instances_since_month(self,no_of_months=1,user=None):
        instances = this.get_completed_instances.filter(quiz_taken__gt=date.today() - relativedelta(months = no_of_months))
        if user: return instances.filter(taker=user)
        else:return instances 

class QuizInstance(models.Model):
	'''A combination of user response and a quiz template.'''
	taker = models.ForeignKey(User,on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	quiz_taken = models.DateTimeField(_('quiz taken'), auto_now_add=True)
	score = models.IntegerField(default=0)
	complete = models.BooleanField(default=False)
	# prevent from setting score in the frontend to avoid tampering
	def __setattr__(self, name, value):
		if name == 'score':
			if getattr(self, 'score', None):
				if getattr(self, 'score') != 0 and getattr(self, 'score') != value:
					raise ScoreTamperedException(self.quiz, self.quiz.id, value)
		super(QuizInstance, self).__setattr__(name, value)

	def __unicode__(self):
		return u"%s, taken by %s on %s" % (self.quiz, self.taker, self.quiz_taken.strftime("%A, %d %B %Y %I:%M%p"))

	@property
	def get_responses(self):
		return UserResponse.objects.filter(quiz_instance=self).all()
	
	
class UserResponse(models.Model):
	'''User response to a single question.'''
	quiz_instance = models.ForeignKey(QuizInstance,on_delete=models.CASCADE)
	question = models.ForeignKey(MultipleChoice,on_delete=models.CASCADE)
	response = models.ManyToManyField(MultipleChoiceAnswer, related_name="response")
	time_taken = models.DateTimeField(_('When was the question posed'), auto_now_add=True)
	time_taken_delta = models.DateTimeField(_('When was the question answered'), blank=True)

	def __unicode__(self):
		return u"Response to %s for %s" % (self.question, self.quiz_instance)
	@property
	def is_correct(self):
		return self.question.correct_answer.all()==self.response.all()