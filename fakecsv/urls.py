from django.urls import path, reverse_lazy
from . import views

app_name = 'fakecsv'
urlpatterns = [
    path('', views.GenerateCsvView.as_view(), name='main'),
    path('schemas', views.SchemaListView.as_view(), name='edit'),
    path('create', views.SchemaCreateView.as_view(), name='create'),
    path('<int:pk>/update', views.SchemaUpdateView.as_view(success_url=reverse_lazy('fakecsv:edit')), name='update'),
    path('<int:pk>/delete', views.SchemaDeleteView.as_view(success_url=reverse_lazy('fakecsv:edit')), name='delete'),
]
