from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CarwashView, RatingsView, CarwashDetailView, RatingDetailView, BranchView, BranchDetailView

router = DefaultRouter()
# router.register(r'', CarwashView)

urlpatterns = [
    path('', CarwashView.as_view()),
    path('<int:pk>/', CarwashDetailView.as_view()),
    path('<int:pk>/ratings/', RatingsView.as_view()),
    path('ratings/<int:review_id>/', RatingDetailView.as_view()),
    path('<int:pk>/branches/', BranchView.as_view()),
    path('branches/<int:pk>/', BranchDetailView.as_view()),
]

urlpatterns += router.urls
