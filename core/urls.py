from django.urls import path
from . import views

# urlpatterns = [
#     path('pacjenci/', views.PacjentListView.as_view(), name='pacjent-list'),
#     path('pacjenci/dodaj/', views.PacjentCreateView.as_view(), name='pacjent-add'),
#     path('pacjenci/<int:pk>/badania/', views.BadanieListView.as_view(), name='badanie-list'),
#     path('badania/dodaj/', views.BadanieCreateView.as_view(), name='badanie-add'),
#     path('badania/<int:pk>/', views.BadanieDetailView.as_view(), name='badanie-detail'),
#     path('badania/<int:badanie_pk>/analizy/dodaj/', views.AnalizaCreateView.as_view(), name='analiza-add'),
#     path('analizy/<int:pk>/', views.AnalizaDetailView.as_view(), name='analiza-detail'),
# ]
app_name = 'core'
urlpatterns = [
    path('pacjenci/', views.PacjentListView.as_view(), name='pacjent-list'),
    path('badania/',   views.BadanieListView.as_view(),   name='badanie-list'),
]