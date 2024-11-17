from django.db import models

# Create your models here.
class task(models.Model):
   
   title=models.CharField(max_length=300, default='Default Title')
   completed=models.BooleanField(default=False)
   updated=models.DateTimeField(auto_now=True)
   created=models.DateTimeField(auto_now_add=True)
   class Meta:
      ordering = ['-updated', '-created']

   def __str__(self):
      return self.title