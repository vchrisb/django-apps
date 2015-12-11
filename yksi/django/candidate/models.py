from django.db import models
from yksi.custom_storages import SecureStorage

# class S3PrivateFileField(models.FileField):
#     def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
#         super(S3PrivateFileField, self).__init__(verbose_name=verbose_name,name=name, upload_to=upload_to, storage=storage, **kwargs)
#         self.storage.default_acl = "private"

# Create your models here.
class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo = models.FileField(blank=True, null=True, upload_to='candidate-photos')
    secure_photo = models.FileField(blank=True, null=True, upload_to='candidate-photos-secure', storage=SecureStorage())
