from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    preview = models.ImageField(upload_to='blog_previews/', blank=True, null=True, verbose_name="Preview")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Views")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Владелец'
    )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['title',]
        permissions = [
            ("can_publish_post", "Может публиковать пост"),
        ]