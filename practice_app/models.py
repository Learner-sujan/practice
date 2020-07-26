from django.db import models

# Create your models here.
class record(models.Model):
    Uid = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=100, blank=True)
    Phone = models.CharField(max_length=50)
    Dob = models.DateField(blank=True, null=True)
    Profile = models.ImageField( upload_to = 'upload/', blank=True, help_text='Upload Image')

    def __str__(self):
        return str(self.Uid)+ " "+ self.Name +"  "+ self.Address +"  "+str(self.Profile) + " "

