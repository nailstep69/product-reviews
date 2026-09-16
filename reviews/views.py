from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout

from .models import Product, Review
from .forms import ReviewForm


def product_list(request):
    products = Product.objects.all()

    return render(request, "products/product_list.html", {
        "products": products
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {
        "form": form
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.review_set.all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, "products/product_detail.html", {
        "product": product,
        "reviews": reviews,
        "form": form
    })


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("product_detail", product_id=review.product.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            form.save()
            return redirect("product_detail", product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "products/review_edit.html", {
        "form": form,
        "review": review
    })


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("product_detail", product_id=review.product.id)

    if request.method == "POST":
        product_id = review.product.id
        review.delete()

        return redirect("product_detail", product_id=product_id)

    return render(request, "products/review_delete.html", {
        "review": review
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("product_list")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("product_list")