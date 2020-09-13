from django.db import models


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = 'polls_question'
        managed = True
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Choice(models.Model):
    question = models.ForeignKey('Question',
                                 on_delete=models.CASCADE,
                                 db_constraint=False)
    choice_text = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = 'polls_choice'
        managed = True
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
