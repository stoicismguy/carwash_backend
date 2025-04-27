from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', get_branch_services, name='Услуги автомойки'),
    path('<int:pk>/groups/', BranchServiceGroupDetailView.as_view(), name='C группы услуг'),
    path('groups/<int:pk>/', ServiceGroupDetailView.as_view(), name='CU услугу для группы'),
]