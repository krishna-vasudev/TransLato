from django.db import models
from django.contrib.auth.models import User
# Create your models here.

LANG_CHOICES=(
('Bengali','bn'),('Gujarati','gu'), ('Hindi','hi'), ('Kannada','kn'), ('Malayalam','ml'), ('Marathi','mr'),
('Nepali','ne'), ('Oriya','or' ), ('Punjabi','pa'), ('Sinhala','si'), ('Tamil','ta'),('Telugu','te'),
('Urdu','ur')

)

class Project(models.Model):
    wiki_title=models.CharField(max_length=120)
    target_lang=models.CharField(max_length=20,choices=LANG_CHOICES,default='Hindi')
    manager=models.ForeignKey(User,on_delete=models.CASCADE,related_name='manager',null=True)
    annotator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='annotator',null=True)

    def __str__(self):
        return self.target_lang+"_"+self.wiki_title

class Sentence(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    original_sentence=models.CharField(max_length=1000)
    translated_sentence=models.CharField(max_length=1000,null=True)

    def __str__(self):
        return str(self.id)+" "+self.project.wiki_title+" "+self.project.target_lang