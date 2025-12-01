from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_published=1)


class Instrument(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Не актуально'
        PUBLISHED = 1, 'Опубликовано'
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status, default=Status.PUBLISHED)
    cat = models.ForeignKey('InstrumentCategory', on_delete=models.PROTECT, related_name='instruments')
    tags = models.ManyToManyField('TagInstrument', blank=True, related_name='instruments')

    published_objects = PublishedManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created']),
        ]
    def get_absolute_url(self):
        return reverse('instrument', kwargs={'instrument_slug': self.slug})


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class TagInstrument(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

