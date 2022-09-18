from django.db import models
from django.utils.translation import gettext_lazy as _
from datamodelapp.models import DataModel

# Create your models here.
class AnalysisRun(models.Model):
    id = models.BigAutoField(primary_key=True)
    samplefile = models.FileField(upload_to="samples", null=False, blank=False)
    modelname = models.ForeignKey(DataModel, on_delete=models.RESTRICT, null=False)
    result = models.TextField(null=True, blank=True)
    updatetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("Analysis Run")
        verbose_name_plural = _("Analysis Runs")

    def delete(self, *args, **kwargs):
        storage, location = self.samplefile.storage, self.samplefile.path
        super(AnalysisRun, self).delete(*args, **kwargs)
        storage.delete(location)
