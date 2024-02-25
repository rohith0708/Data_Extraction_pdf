from django.db import models

# created model named uploadpdf with a file field
class uploadpdf(models.Model):
    pdf = models.FileField(upload_to='data/pdf')

    def __str__(self):
        return self.pdf