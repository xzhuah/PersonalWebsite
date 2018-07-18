from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('update/',views.update,name="update"),
    path('',views.index,name="index")

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)