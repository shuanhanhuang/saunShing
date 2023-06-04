from .models import Home
import django_filters

class HomeFilter(django_filters.FilterSet):
    class Meta:
        model = Home
        fields = '__all__'


