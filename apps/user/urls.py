from rest_framework import routers

from apps.user import views

user_router = routers.DefaultRouter()
user_router.register(r'create-user',views.UserListView,basename='create-user')