from django.db import models
from django.contrib.auth.models import User
import uuid

class UserFormTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="form_templates")
    name = models.CharField(max_length=255, help_text="Enter a unique name for the form.")
    html_code = models.TextField(help_text="The HTML code for the form.")
    css_files = models.TextField(blank=True, help_text="Comma-separated list of CSS file URLs.")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Time when the form was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Time when the form was last updated.")
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Unique identifier

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"
    
class FormResponse(models.Model):
    form_template = models.ForeignKey(UserFormTemplate, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who submitted the form (if authenticated).")
    response_data = models.JSONField(help_text="Stores the submitted form data in JSON format.")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Time when the form was submitted.")

    def __str__(self):
        return f"Response by {self.user} submitted at {self.submitted_at}"

