from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, PosterImage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, PosterImage
from django.core.paginator import Paginator 





def home(request):
    posters = PosterImage.objects.all()[:5]
    
    brands = Brand.objects.all()
    brand_data = []
    for brand in brands:
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
    selected_brands = request.GET.getlist('brand') 
    
    # OPTIMIZATION: Fetch brand and sizes in the same query to stop database lagging
    products = Product.objects.select_related('brand').prefetch_related('sizes').all().order_by('-created_at')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(brand__name__icontains=query)
        )
        
    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)
        
    all_brands = Brand.objects.all().order_by('name')
    
    # PAGINATION: Show 12 products per page
    paginator = Paginator(products, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/index.html', {
        'products': page_obj, # Pass the paginated object instead of all products
        'all_brands': all_brands,
        'selected_brands': selected_brands,
        'brand': None 
    })

def brand_products(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    
    # OPTIMIZATION
    products = Product.objects.select_related('brand').prefetch_related('sizes').filter(brand=brand).order_by('-created_at')
    
    all_brands = Brand.objects.all().order_by('name')
    selected_brands = [str(brand.id)]
    
    # PAGINATION: Show 12 products per page
    paginator = Paginator(products, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/index.html', {
        'products': page_obj, # Pass the paginated object
        'all_brands': all_brands,
        'selected_brands': selected_brands, 
        'brand': brand  
    })



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(brand=product.brand).exclude(pk=pk).order_by('-created_at')[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products
    })