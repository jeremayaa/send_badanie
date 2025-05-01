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
    path('pacjenci/dodaj/',  views.PacjentCreateView.as_view(), name='pacjent-add'),

    path('pacjenci/<int:pk>/',        views.PacjentDetailView.as_view(), name='pacjent-detail'),
    path('pacjenci/<int:pk>/edit/',   views.PacjentUpdateView.as_view(), name='pacjent-edit'),
    path('pacjenci/<int:pk>/delete/', views.PacjentDeleteView.as_view(), name='pacjent-delete'),


    path('badania/',   views.BadanieListView.as_view(),   name='badanie-list'),
    path('badania/dodaj/',   views.BadanieCreateView.as_view(), name='badanie-add'),
    path('badania/<int:pk>/',views.BadanieDetailView.as_view(), name='badanie-detail'),
    path('badania/<int:pk>/edit/',   views.BadanieUpdateView.as_view(), name='badanie-edit'),
    path('badania/<int:pk>/delete/', views.BadanieDeleteView.as_view(), name='badanie-delete'),

    # path('badania/<int:pk>/analyze/', views.BadanieAnalyzeView.as_view(), name='badanie-analyze'),

    path(
      'badania/<int:badanie_pk>/analizy/dodaj/',
      views.AnalizaCreateView.as_view(),
      name='analiza-add'
    ),
    # programowe dodawanie analizy
    path(
      'badania/<int:badanie_pk>/analizy/program/',
      views.AnalizaProgramCreateView.as_view(),
      name='analiza-add-program'
    ),

    # detail / edit / delete analizy…
    path(
      'analizy/<int:pk>/',
      views.AnalizaDetailView.as_view(),
      name='analiza-detail'
    ),
    path(
      'analizy/<int:pk>/edit/',
      views.AnalizaUpdateView.as_view(),
      name='analiza-edit'
    ),
    path(
      'analizy/<int:pk>/delete/',
      views.AnalizaDeleteView.as_view(),
      name='analiza-delete'
    ),

    # path(
    #   'analizy/<int:pk>/analyze/',
    #   views.AnalizaAnalyzeView.as_view(),
    #   name='analiza-analyze'
    # ),
    path(
      'analizy/<int:pk>/program/',
      views.AnalizaProgramUpdateView.as_view(),
      name='analiza-edit-program'
    ),

        # „program” dla badania
    path(
      'program/badanie/<int:badanie_pk>/',
      views.ProgramAnalyzeView.as_view(),
      name='program-analyze-badanie'
    ),
    # „program” dla istniejącej analizy
    path(
      'program/analiza/<int:analiza_pk>/',
      views.ProgramAnalyzeView.as_view(),
      name='program-analyze-analiza'
    ),
    
]