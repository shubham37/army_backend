from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^student_api/', include('student.urls')),
    url(r'^assessor_api/', include('assessor.urls')),
    url(r'^admin_api/', include('admin_user.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns+= static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
