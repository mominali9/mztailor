from django.shortcuts import render
from django.http import JsonResponse
from tailors.models.base_models import Logo
from tailors.models.ai_models import MeasurementProfile
from tailors.ai_measure import extract_measurements

def ai_measure(request):
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/ai_measure.html', {'logo': logo})

def process_measurement(request):
    if request.method == 'POST':
        height_cm = request.POST.get('height_cm')
        image = request.FILES.get('image')
        
        if not height_cm or not image:
            return JsonResponse({"error": "Height and image are required."}, status=400)
            
        try:
            height_cm = float(height_cm)
            image_bytes = image.read()
            measurements = extract_measurements(image_bytes, height_cm)
            
            if 'error' in measurements:
                return JsonResponse({"error": measurements['error']}, status=400)
                
            # Optionally save to the database here
            if request.user.is_authenticated:
                MeasurementProfile.objects.create(
                    user=request.user,
                    height_cm=height_cm,
                    chest_cm=measurements['chest_cm'],
                    waist_cm=measurements['waist_cm'],
                    shoulder_cm=measurements['shoulder_cm'],
                    arm_length_cm=measurements['arm_length_cm'],
                    recommended_size=measurements['recommended_size']
                )
                
            return JsonResponse(measurements)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
