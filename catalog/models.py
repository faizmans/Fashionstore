from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, help_text="e.g., Small, Medium, 32 Waist")
    abbreviation = models.CharField(max_length=5, help_text="e.g., S, M, 32")

    def __str__(self):
        return self.abbreviation

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    
    sizes = models.ManyToManyField(Size, related_name='products')
    
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} | {self.name}"



class PosterImage(models.Model):
    title = models.CharField(max_length=100, help_text="e.g., Summer Campaign 1")
    image = models.ImageField(upload_to='posters/')
    order = models.IntegerField(default=0, help_text="Order in the carousel (1, 2, 3...)")
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title