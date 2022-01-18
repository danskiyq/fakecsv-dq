from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from . import views

app_name = 'fakecsv'
urlpatterns = [
    path('schemas', views.SchemaListView.as_view(), name='main'),
    # path('ad/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('create', views.SchemaCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.SchemaUpdateView.as_view(success_url=reverse_lazy('fakecsv:main')), name='update'),
    path('<int:pk>/delete', views.SchemaDeleteView.as_view(success_url=reverse_lazy('fakecsv:main')), name='delete'),
]