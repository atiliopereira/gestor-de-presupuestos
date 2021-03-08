from django.conf.urls import url

from profesionales.views import ProfesionalesDashboardView

urlpatterns = [
    url(r'^profesionales_dashboard/$', ProfesionalesDashboardView.as_view(), name='profesionales_dashboard'),
]