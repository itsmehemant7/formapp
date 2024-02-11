from django.db import models

# Create your models here.



class Client(models.Model):
    json = models.TextField() # or can use JSONField
    def __str__(self):
        return self.id
    

class Files(models.Model):
    FILE_TYPE_CHOICES = [
        ('AUDIO', 'Audio'),
        ('CV', 'Curriculum Vitae'),
        ('LOR', 'Letter of Recommendation'),
        ('FILE', 'Generic File'),
    ]
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to="files")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
