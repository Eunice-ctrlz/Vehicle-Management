from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import Car

def home(request):
    query = request.GET.get('q')
    max_price = request.GET.get('price')
    cars = Car.objects.filter(is_available=True)

    if query:
        # Search by brand or car name
        cars = cars.filter(name__icontains=query) | cars.filter(brand__icontains=query)
    
    if max_price:
        # Filter by daily rate
        cars = cars.filter(daily_rate__lte=max_price)

    return render(request, 'fleet/home.html', {'cars': cars})

@csrf_exempt
def update_gps(request, car_id):
    if request.method == 'POST':
        car = Car.objects.get(id=car_id)
        car.latitude = request.POST.get('lat')
        car.longitude = request.POST.get('lng')
        car.save()
        return JsonResponse({'status': 'success'})
    
def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'fleet/home.html', {'cars': cars})
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'fleet/car_detail.html', {'car': car})