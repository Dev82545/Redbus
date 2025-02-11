from django.db import models

class buses(models.Model):
    sno = models.AutoField(primary_key= True)
    name = models.CharField(max_length= 255)
    city1 =models.CharField(max_length= 255)
    city2 =models.CharField(max_length= 255)
    dep_time =models.CharField(max_length= 255)
    arr_time =models.CharField(max_length= 255)
    stops =models.CharField(max_length= 255)
    slug = models.CharField(max_length= 255)
    seats =models.IntegerField()
    
    
    def __str__(self):
        return self.name
    


# Create your models here.
