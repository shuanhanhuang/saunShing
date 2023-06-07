from .models import Home
import django_filters
from django.db import models

class HomeFilter(django_filters.FilterSet):
    class Meta:
        model = Home
        fields = '__all__'
        filter_overrides = {
            models.FileField: {
                'filter_class': django_filters.CharFilter,  # 將 'FileField' 覆蓋為 'CharFilter'
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                },
            },
        }


