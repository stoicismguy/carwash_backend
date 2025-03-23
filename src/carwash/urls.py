from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CarwashView, RatingsView, RatingBranchView, CarwashDetailView, RatingDetailView, BranchView, BranchDetailView

router = DefaultRouter()
# router.register(r'', CarwashView)

urlpatterns = [
    path('', CarwashView.as_view()),
    path('<int:pk>/', CarwashDetailView.as_view(), name='CRUD автомойки'),

    path('<int:pk>/ratings/', RatingsView.as_view(), name='Рейтинги автомойки'),

    path('branches/<int:pk>/ratings/', RatingBranchView.as_view(), name="CR рейтинги филиала"),
    path('ratings/<int:review_id>/', RatingDetailView.as_view(), name="D рейтинга"),

    path('<int:pk>/branches/', BranchView.as_view()),
    path('branches/<int:pk>/', BranchDetailView.as_view()),
]

urlpatterns += router.urls
