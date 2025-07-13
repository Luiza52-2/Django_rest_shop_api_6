from django.contrib import admin
from django.urls import path, include
from . import swagger  # импорт swagger.py с твоими swagger urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('product.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Добавляем маршруты swagger в основной urlpatterns
urlpatterns += swagger.urlpatterns
