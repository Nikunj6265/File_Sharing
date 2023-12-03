from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class File(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    allowed_extensions = ['pptx', 'docx', 'xlsx']

    def validate_file_extension(value):
        ext = value.name.split('.')[-1]
        if ext.lower() not in File.allowed_extensions:
            raise ValidationError('Invalid file extension. Allowed: pptx, docx, xlsx.')
    
    def save(self, *args, **kwargs):
        # Check if the owner is a superuser
        if not self.owner.is_superuser:
            raise PermissionError('Only Operation users are allowed to upload files.')

        super().save(*args, **kwargs)