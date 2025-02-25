from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', views.EmployeeViewset, basename='employees')

urlpatterns = [
    path('students/', views.studentsview),
    path('student/<int:pk>', views.studentdetailview),
    
    # path('employee/', views.Employees.as_view()),
    # path('employee/<int:pk>', views.EmployeeDetails.as_view()),
    
    path('', include(router.urls)),
    
    path('blog/', views.Blogviews.as_view()),
    path('comment/', views.Commentviews.as_view()),
    
    path('blog/<int:pk>', views.blogdetails.as_view()),
    path('comment/<int:pk>', views.commentdetails.as_view()),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]