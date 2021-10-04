import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Seller
from .models import Product


"""
Endpoint will return the version of the site
"""
def version_endpoint(request):
    return JsonResponse({
        "version": 1.0,
    })

"""
Endpoint will accept a user name post and return a hello message.
"""
def hello_endpoint(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")

        return JsonResponse({
            "msg": "Hello " + name + "!",
        })
    else:
        return JsonResponse({
            "msg": "method not allowed",
        }, status=405)

"""
Endpoint will create or provide a list of Sellers in a paginated manner
"""
def list_create_seller_endpoint(request):
    if request.method == "GET": # A.k.a. "list"
        sellers = Seller.objects.all()
        sellers_count = Seller.objects.count()

        # for example: /api/sellers?limit=5
        limit_numb = request.GET.get("limit", 25)
        paginator = Paginator(sellers, limit_numb)
        # for example: /api/sellers?page=4
        page_numb = request.GET.get("page")
        page_obj = paginator.get_page(page_numb)
        # Perform "serialization".
        results = []
        for seller in page_obj:
            r = {
                "name": seller.name,
                "id": seller.id,
                "country": seller.country,
                "province": seller.province,
                "city": seller.city,
            }
            results.append(r)

        return JsonResponse({
            "count": sellers_count,
            "results": results,
        })
    elif request.method == "POST": # A.k.a. "create"
        data = json.loads(request.body) # "Deserialization"
        # Extract our data that the client sent us.
        nam = data.get("name")
        c = data.get("country")
        p = data.get("province")
        cy = data.get("city")
        # Create our record in the database.
        seller = Seller.objects.create(name=nam, country=c, province=p, city=cy)
        # Return success message to the client.
        # return JsonResponse({ # VERSION A
        #     "msg": "record created",
        # },status=201)
        # VERSION B
        response = {
            "id": seller.id,
            "name": seller.name,
            "province": seller.province,
            "city": seller.city,
            "country": seller.country,
        }
        return JsonResponse(response, status=201)
    else:
        return JsonResponse({
            "msg": "method not allowed",
        }, status=405)

"""
Endpoint will allow update, retrieve details and delete functionality for the
Seller models.
"""
def detail_update_delete_seller_endpoint(request, id):
    # For example
    # if /api/seller/1
    # then id=1
    # Get the record or return 404 error if D.N.E.
    try:
        seller = Seller.objects.get(id=id)
    except Seller.DoesNotExist:
        return JsonResponse({"error":"d.n.e."},status=404)
    if request.method == "GET": # Details
        # "Serialization"
        response = {
            "id": seller.id,
            "name": seller.name,
            "province": seller.province,
            "city": seller.city,
            "country": seller.country,
        }
        return JsonResponse(response, status=200)
    elif request.method == "PUT": # Update
        data = json.loads(request.body)

        n = data.get("name")
        c = data.get("country")
        p = data.get("province")
        cy = data.get("city")

        seller.name = n
        seller.country = c
        seller.province = p
        seller.city = cy
        seller.save()
        # "Serialization"
        response = {
            "id": seller.id,
            "name": seller.name,
            "province": seller.province,
            "city": seller.city,
            "country": seller.country,
        }
        return JsonResponse(response, status=200)
    elif request.method == "DELETE": # Delete
        seller.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({
            "msg": "method not allowed",
        }, status=405)

"""
Endpoint will create or provide a list of Products in a paginated manner
"""

def list_create_product_endpoint(request):
     # http GET 127.0.0.1:8000/api/products
    if request.method == "GET":
        products = Product.objects.all()
        products_count = Product.objects.count()

        limit_numb = request.GET.get("limit", 25)
        paginator = Paginator(products, limit_numb)
        page_numb = request.GET.get("page")
        page_obj = paginator.get_page(page_numb)

        r = []
        for p in page_obj:
            record = {
                "seller": p.seller,
                "name": p.name,
                "price": p.price,
            }
        return JsonResponse({
            "count": products_count,
            "results": r,
        })
    # http POST 127.0.0.1:8000/api/products seller=1 name=lala price=123
    elif request.method == "POST":
        data = json.loads(request.body)

        seller = data.get("seller")
        name = data.get("name")
        price = data.get("price")

        product = Product.objects.create(seller_id=seller, name=name, price=price)

        response = {
            "id": product.id,
            "seller_id": product.seller.id,
            "name": product.name,
            "price": product.price,
        }

        return JsonResponse(response, status = 201)
    else:
        return JsonResponse({
            "msg": "method not allowed",
        }, status=405)

"""
Endpoint will allow update, retrieve details and delete functionality for the
Product models.
"""

def detail_update_delete_product_endpoint(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return JsonResponse({"error":"d.n.e."},status=404)
#   http GET 127.0.0.1:8000/api/product/1
    if request.method == "GET":
        response = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "seller_id": product.seller.id,
        }
        return JsonResponse(response, status=200)

    elif request.method == "PUT":
        # http PUT 127.0.0.1:8000/api/product/2 seller=2 name=lilili price=412
        data = json.loads(request.body)

        n = data.get("name")
        id = data.get("seller_id")
        p = data.get("price")

        product.name = n
        product.price = p
        product.sellerid = id
        product.save()

        response = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "seller_id": product.seller_id,
        }
        return JsonResponse(response, status=200)

    elif request.method == "DELETE":
        product.delete()
        return JsonResponse({}, status=204)
    else:
        return JsonResponse({
            "msg": "method not allowed",
        }, status=405)
