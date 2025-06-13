from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# Mainapp model: Stores user-submitted content for SEO analysis
# -----------------------------

class Mainapp(models.Model):
    # Each entry is associated with a user; deleting the user deletes their entries
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The main block of text input by the user (e.g., blog, tweet, caption)
    text = models.TextField(max_length=250)
    
    # Optional photo input; images are stored under the 'photos/' directory
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    
    # Timestamp when the entry was first created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Timestamp updated whenever the entry is saved again
    uploaded_at = models.DateTimeField(auto_now=True)

    # String representation showing username and a preview of text
    def __str__(self):
        return f"{self.user.username} - {self.text[:10]}"


# -----------------------------
# SEOAnalysis model: Stores results returned from the SEO API (e.g., TextRazor)
# -----------------------------

class SEOAnalysis(models.Model):
    # The raw text that was analyzed
    input_text = models.TextField()
    
    # Timestamp indicating when the analysis was performed
    analyzed_on = models.DateTimeField(auto_now_add=True)
    
    # List of keyword suggestions from the API (stored as JSON)
    keywords = models.JSONField(default=list)
    
    # Readability score returned from the API (optional)
    readability_score = models.FloatField(null=True, blank=True)
    
    # Text-based suggestions or optimization tips (optional)
    suggestions = models.TextField(blank=True)

    # String representation showing the analysis ID
    def __str__(self):
        return f"SEOAnalysis {self.id}"
