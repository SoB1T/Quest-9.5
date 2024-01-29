import django_filters
from django_filters import FilterSet
from .models import Post
from django import forms


class PostFilter(FilterSet):
    author__user_id__username = django_filters.CharFilter(field_name='author__user_id__username',
                                                          lookup_expr='icontains')

    date = django_filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='date',
        lookup_expr='date'
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'heading': ['icontains'],
            'categories': ['exact'],
            'raiting': ['lte', 'gte'],
        }
