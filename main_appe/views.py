from django.shortcuts import render
from .models import Category,Brand,Product,ProductAttributes,Banner
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string

# Create your views here.
def home(request):
    data = Product.objects.filter(is_featured=True).order_by('-id')
    banner = Banner.objects.all().order_by('-id')
    return render(request,'index.html',{"data":data,"banner":banner})

def Category_list(request):
    data = Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{"data":data})

def Brands_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request,'brands_list.html',{"data":data})

def Product_List(request):
    total_products = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    # category=Product.objects.distinct().values('category__title','category__id')
    # brand = Product.objects.distinct().values('brand__title',"brand__id")
    # colors=ProductAttributes.objects.distinct().values('color__title','color__id',"color__color_code")
    # sizes = ProductAttributes.objects.distinct().values('size__title','size__id')
    return render(request,'product_list.html',{
        "data":data,
        'total_products':total_products,
        # 'category':category,
        # 'brand':brand,
        # 'colors':colors,
        # 'sizes':sizes
    })
def Category_Product_List(request,id):
    category = Category.objects.get(id=id)
    data = Product.objects.filter(category=category).order_by('-id')
    # category = Product.objects.distinct().values('category__title', 'category__id')
    # brand = Product.objects.distinct().values('brand__title', "brand__id")
    # colors = ProductAttributes.objects.distinct().values('color__title', 'color__id', "color__color_code")
    # sizes = ProductAttributes.objects.distinct().values('size__title', 'size__id')
    return render(request,'category_product_list.html',{
        'data':data,
        # 'category': category,
        # 'brand': brand,
        # 'colors': colors,
        # 'sizes': sizes
    })

def Brand_product_list(request,id):
    brand = Brand.objects.get(id=id)
    data = Product.objects.filter(brand=brand)
    # category = Product.objects.distinct().values('category__title', 'category__id')
    # brand = Product.objects.distinct().values('brand__title', "brand__id")
    # colors = ProductAttributes.objects.distinct().values('color__title', 'color__id', "color__color_code")
    # sizes = ProductAttributes.objects.distinct().values('size__title', 'size__id')
    return render(request,"brand_product_list.html",{
        'data':data,
        # 'category': category,
        # 'brand': brand,
        # 'colors': colors,
        # 'sizes': sizes
    })

# product details page
def Product_Details_page(request,slug,id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:3]
    colors=ProductAttributes.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttributes.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()
    print(sizes)
    print(colors)
    return render(request,'product_details_page.html',{
        "data":product,
        "related_product":related_products,
        "colors":colors,
        "sizes":sizes})

# search function for home page
def search_products(request):
    qs=request.GET['q']
    data = Product.objects.filter(title__icontains=qs).order_by('-id')
    return render(request,'search_product.html',{'data':data})

# filter data by products
def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minprice = request.GET['minprice']
    maxprice = request.GET['maxprice']
    allProducts=Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattributes__price__gte=minprice)
    allProducts = allProducts.filter(productattributes__price__lte=maxprice)
    if len(colors) > 0:
        allProducts =allProducts.filter(productattributes__color_id__in=colors).distinct()
        print(allProducts)
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(productattributes__size_id__in=sizes).distinct()
    t = render_to_string('ajax/product_list.html', {'data': allProducts})
    return JsonResponse({'data':t})


def loadmode_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    total = int(request.GET['total'])
    data = Product.objects.all().order_by('-id')[offset:total:limit]
    t=render_to_string('ajax/product_list.html',{"data":data})
    return JsonResponse({"data":t})

def Add_To_Cart(request):
    # del request.session['cartdata']
    cart_p={}
    cart_p[str(request.GET['id'])]={
        'title':request.GET['title'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['image']
    }
    print(cart_p)
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p
    return JsonResponse(
        {"data":request.session['cartdata'],
         "totalitems":len(request.session['cartdata'])})

def Cart_List(request):
    total_amount=0
    for p_id,item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'cart_list.html',
                      {"cart_data": request.session['cartdata'],
                       "totalitems": len(request.session['cartdata']),
                       'total_amount': total_amount
                       })
def Delete_Cart_Item(request):
    p_id = str(request.GET['id'])
    print(p_id)
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart_list.html', {"cart_data": request.session['cartdata'],
                       "totalitems": len(request.session['cartdata']),
                       'total_amount': total_amount
                       })
    return JsonResponse({"data": t,"totalitems": len(request.session['cartdata'])})

def Update_Cart_Vtem(request):
    p_id = str(request.GET['id'])
    p_qty=request.GET['qty']
    print(p_id,p_qty)
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            print("cart data",cart_data)
            request.session['cartdata'] = cart_data
    total_amount = 0
    for p_id,item in request.session['cartdata'].items():
        total_amount += int(item['qty']) * float(item['price'])
    t = render_to_string('ajax/cart_list.html', {"cart_data": request.session['cartdata'],
                                                 "totalitems": len(request.session['cartdata']),
                                                 'total_amount': total_amount
                                                 })
    return JsonResponse({"data": t, "totalitems": len(request.session['cartdata'])})