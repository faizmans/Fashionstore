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
            'name': brand.name,
            'cover_image': cover_product.image.url if cover_product and cover_product.image else None
        })
        
    return render(request, 'catalog/home.html', {
        'posters': posters,
        'brands': brand_data
    })

def index(request):
    # This is now the "Shop All" page
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'catalog/index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(brand=product.brand).exclude(pk=pk).order_by('-created_at')[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products
    })