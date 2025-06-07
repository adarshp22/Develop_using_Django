from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Mainapp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    photo= models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at= models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.user.username}- {self.text[:10]}"
    
class SEOAnalysis(models.Model):
    original_text = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)
    readability_score = models.FloatField(null=True, blank=True)
    keywords = models.JSONField(default=list)  # stores keyword list as JSON

    def __str__(self):
        return f"Analysis on {self.analyzed_at.strftime('%Y-%m-%d %H:%M:%S')}"