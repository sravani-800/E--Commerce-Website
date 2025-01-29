from django.shortcuts import render
from django.http import JsonResponse
import json
import os

cart = []

# Create your views here.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, 'product.json')
def load_products():
    with open(PRODUCTS_FILE, 'r') as file:
        return json.load(file)


def get_products(request):
    products = load_products()
    return JsonResponse(products, safe=False)

