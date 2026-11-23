from django.contrib import admin
from django.db import models as django_models
from . import models

for model in vars(models).values():
	if (
		isinstance(model, type)
		and issubclass(model, django_models.Model)
		and model.__module__ == models.__name__
		and not model._meta.abstract
	):
		admin.site.register(model)
