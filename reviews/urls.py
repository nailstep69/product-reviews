from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path(
        "products/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "reviews/<int:review_id>/edit/",
        views.review_edit,
        name="review_edit"
    ),

    path(
        "reviews/<int:review_id>/delete/",
        views.review_delete,
        name="review_delete"
    ),
]