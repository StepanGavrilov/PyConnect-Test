import debug_toolbar

from django.urls import path, include

app_name = 'account_system_api'

urlpatterns = [

    path('', include('account_system_api.api.routers'))

]
