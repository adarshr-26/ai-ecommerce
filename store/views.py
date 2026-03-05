from sklearn.linear_model import LinearRegression
import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product, Order, OrderItem


# ------------------ PRODUCT LIST ------------------

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# ------------------ SIGNUP ------------------

def signup(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:product_list')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


# ------------------ PLACE ORDER ------------------

@login_required
def place_order(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    order = Order.objects.create(
        customer=request.user,
        total_price=product.price
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
    )

    return redirect('store:product_list')


# ------------------ ORDER HISTORY ------------------

@login_required
def order_history(request):

    orders = Order.objects.filter(customer=request.user)

    return render(request, 'orders.html', {'orders': orders})


# ------------------ LOGOUT ------------------

@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


# ------------------ SMART SEARCH ------------------

def smart_search(request):

    query = request.GET.get('q')

    if not query:
        return JsonResponse({'error': 'No query provided'})

    products = Product.objects.all()

    product_list = []
    descriptions = []

    for product in products:
        text = product.name + " " + product.description
        descriptions.append(text)
        product_list.append(product)

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(descriptions)

    query_vector = vectorizer.transform([query])

    similarity = cosine_similarity(query_vector, tfidf_matrix).flatten()

    results = []

    for i in similarity.argsort()[::-1]:

        results.append({
            'id': product_list[i].id,
            'name': product_list[i].name,
            'description': product_list[i].description,
            'price': float(product_list[i].price),
            'score': float(similarity[i])
        })

    return JsonResponse({'results': results[:5]})


# ------------------ RECOMMEND PRODUCTS ------------------

def recommend_products(request, product_id):

    products = Product.objects.all()

    product_list = []
    descriptions = []

    for product in products:

        text = product.name + " " + product.description

        descriptions.append(text)

        product_list.append(product)

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(descriptions)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    try:

        index = next(i for i, p in enumerate(product_list) if p.id == product_id)

    except StopIteration:

        return JsonResponse({'error': 'Product not found'})

    similarity_scores = list(enumerate(similarity_matrix[index]))

    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    results = []

    for i, score in similarity_scores[1:4]:

        results.append({
            'id': product_list[i].id,
            'name': product_list[i].name,
            'description': product_list[i].description,
            'price': float(product_list[i].price),
            'similarity_score': float(score)
        })

    return JsonResponse({'recommendations': results})


# ------------------ AI PRICE PREDICTION ------------------

def predict_price(request):

    try:
        storage = float(request.GET.get('storage'))
        rating = float(request.GET.get('rating'))

    except:

        return JsonResponse({'error': 'Provide storage and rating'})

    X = np.array([
        [64,4.0],
        [128,4.2],
        [256,4.5],
        [512,4.8],
        [128,3.8],
        [256,4.3]
    ])

    y = np.array([
        20000,
        30000,
        50000,
        80000,
        25000,
        55000
    ])

    model = LinearRegression()

    model.fit(X,y)

    predicted_price = model.predict([[storage,rating]])

    return JsonResponse({
        'predicted_price': float(predicted_price[0])
    })