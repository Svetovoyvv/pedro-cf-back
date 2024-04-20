from django.apps import apps
from django.contrib import admin
from django.contrib.admin.exceptions import AlreadyRegistered


def register_app_models(app_name):
    if '.' in app_name:
        app_name = app_name.split('.')[-1]
    app_models = apps.get_app_config(app_name).get_models()
    for model in app_models:
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            continue
