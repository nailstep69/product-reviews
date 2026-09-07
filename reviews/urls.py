from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("register/", views.register, name="register"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("login/", views.login_view, name="login"),

]