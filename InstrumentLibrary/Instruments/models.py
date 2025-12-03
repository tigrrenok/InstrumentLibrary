from django.db import models
from slugify import slugify
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_published=1)


class Instrument(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'снято с производства'
        PUBLISHED = 1, 'доступно'
    title = models.CharField(max_length=100, verbose_name="название")
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    image = models.ImageField(upload_to=f'images/', null=True, blank=True, default=None,
                              verbose_name="image")

    content = models.TextField(blank=True, verbose_name="содержание")
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.IntegerField(choices=Status, default=0, verbose_name="актуальность")
    cat = models.ForeignKey('InstrumentCategory', on_delete=models.PROTECT, related_name='instruments', verbose_name="категории")
    tags = models.ManyToManyField('TagInstrument', blank=True, related_name='instruments', verbose_name="тэги")
    specifications = models.OneToOneField('InstrumentSpecification', on_delete=models.SET_NULL,
                                          null=True, blank =True, related_name='instrument', verbose_name="спецификация")

    objects = models.Manager()
    published_objects = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['-time_created']),
        ]
        verbose_name = 'лабораторное оборудование'
        verbose_name_plural = verbose_name


    def get_absolute_url(self):
        return reverse('instrument', kwargs={'instrument_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class InstrumentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="название категории")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категории оборудования"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class TagInstrument(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="название тэга")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="слаг")

    class Meta:
        verbose_name = "Тэги для оборудования"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

class InstrumentSpecification(models.Model):
    accuracy = models.CharField(blank=True, null=True, verbose_name="Точность")
    resolution = models.CharField(blank=True, null=True, verbose_name="Разрешение")
    method = models.CharField(max_length=255, blank=True, null=True)

class UploadedFiles(models.Model):
    file = models.FileField(upload_to='uploads_instrument')