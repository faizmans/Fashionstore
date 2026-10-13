from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, PosterImage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, PosterImage





def home(request):
    # Get up to 5 poster images for the carousel
    posters = PosterImage.objects.all()[:5]
    
    # Get all brands and attach their first product's image to use as a cover photo
    brands = Brand.objects.all()
    brand_data = []
    for brand in brands:
        # Get the newest product for this brand to use as the category image
        cover_product = brand.products.order_by('-created_at').first()
        brand_data.append({
            'id': brand.id,
            'name': brand.name,
            'cover_image': cover_product.image.url if cover_product and cover_product.image else None
        })
        
    return render(request, 'catalog/home.html', {
        'posters': posters,
        'brands': brand_data
    })




def index(request):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')

    if query:
        # Filter products by matching the product name OR the brand name
        products = products.filter(
            Q(name__icontains=query) | 
            Q(brand__name__icontains=query)
        )
    
    # We pass brand=None because this is the global shop
    return render(request, 'catalog/index.html', {
        'products': products,
        'brand': None 
    })

def brand_products(request, brand_id):
    # Fetch the exact brand clicked
    brand = get_object_or_404(Brand, pk=brand_id)
    
    # Filter products where the brand matches
    products = Product.objects.filter(brand=brand).order_by('-created_at')
    
    return render(request, 'catalog/index.html', {
        'products': products,
        'brand': brand  # Pass the brand to the template to customize the header
    })






def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(brand=product.brand).exclude(pk=pk).order_by('-created_at')[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products
    })