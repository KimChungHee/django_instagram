from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)

    def __str__(self):
        return "text : "+self.text

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])

# class Comment(models.Model):
#     document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
#     text = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     like = models.IntegerField(default=0)
#     dislike = models.IntegerField(default=0)
#
#     def __str__(self):
#         return (self.author.username if self.author else "무명") + "의 댓글"
