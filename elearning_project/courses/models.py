from django.db import models

class Subject(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.CharField(
        max_length=300
    )

    def __str__(self):
        return self.name
    
class Lesson(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)

    content = models.TextField()

    order = models.IntegerField(default=1)

    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)

    class Meta:
        unique_together = ['subject', 'title']

    def __str__(self):
        return self.title  
    
class Bookmark(models.Model):
    user_id = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    
class History(models.Model):
    user_id = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    