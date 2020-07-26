from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
# Create your models here.

def upload_location(instance, filename):
    file_path = 'blog{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
        )
    return file_path

class BlogPost(models.Model):
    title                   = models.CharField(max_length=50, blank=False, null=False)
    body                    = models.TextField(max_length=5000, blank=False, null=False)
    image                   = models.ImageField(upload_to=upload_location, blank=False, null=False)
    date_published          = models.DateTimeField(verbose_name='date_published', auto_now_add=True)
    date_updated            = models.DateTimeField(verbose_name='date_updated', auto_now=True)
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)


    def __str__(self):
        return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, *args, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.author.username)+"-"+ instance.title

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)