from rest_framework.routers import DefaultRouter
from .views import PacjentViewSet, BadanieViewSet, AnalizaViewSet

router = DefaultRouter()
router.register(r'pacjenci', PacjentViewSet, basename='pacjent')
router.register(r'badania', BadanieViewSet, basename='badanie')
router.register(r'analizy', AnalizaViewSet, basename='analiza')

urlpatterns = router.urls
