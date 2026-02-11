from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import Car

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