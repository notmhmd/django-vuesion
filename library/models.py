from django.db import models
from django.conf import settings
from django.utils import timezone
import os

# Create your models here.


def get_upload_path(instance, filename):
    return os.path.join("books", "uploaded_by_%s" % instance.uploaded_by.username, "titled_%s" % instance.title, filename)


class Book(models.Model):
    title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=170, default="No Author")
    description = models.TextField(max_length=300)
    link = models.URLField(blank=True, null=True)
    document = models.FileField(upload_to=get_upload_path)
    book_cover = models.ImageField(upload_to=get_upload_path)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    blank=True,
                                    null=True,
                                    related_name="approved")

    def approve(self, user):
        if not self.approved:
            self.approved = True
            self.approved_at = timezone.now()
            self.approved_by = user
            self.save()
        else:
            self.approved = False
            self.approved_by = None
            self.approved_at = None
            self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wrote")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        if self.approved_comment:
            self.approved_comment = False
            self.save()
            return
        self.approved_comment = True
        self.save()
        return

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
