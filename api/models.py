from django.db import models
from tastypie.resources import ModelResource
from store.models import Product

class StoreResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = "products"
