from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# Create your models here.
# Enumerations
class DataModelType(models.IntegerChoices):
    PCA = 0
    SIMCA = 1
    PLSDA = 2
    KNN = 3
    SVM = 4


class DataModel(models.Model):
    modelname = models.CharField(max_length=20, primary_key=True)
    type = models.IntegerField(choices=DataModelType.choices, default=1)
    modelfile = models.FileField(upload_to="models", null=False, blank=False)

    def __str__(self):
        return str(self.modelname)

    class Meta:
        verbose_name = _("Data Model")
        verbose_name_plural = _("Data Models")

    # def delete(self, *args, **kwargs):
    #     storage, location = self.modelfile.storage, self.modelfile.path
    #     super(DataModel, self).delete(*args, **kwargs)
    #     storage.delete(location)


""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            # its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)


""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)