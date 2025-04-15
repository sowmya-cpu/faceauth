from django.shortcuts import render

def home(request):
    return render(request, "index.html")

import cv2
import numpy as np
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Attendance

@csrf_exempt
def register(request):
    """
    Endpoint to register a user.
    Expects POST data with:
      - username: text field
      - smile_image: file upload
      - angry_image: file upload
    """
    if request.method == "POST":
        username = request.POST.get('username')
        smile_image = request.FILES.get('smile_image')
        angry_image = request.FILES.get('angry_image')
        
        # Debug print: check what files we received
        print("=== Registration Request ===")
        print("Username:", username)
        if smile_image:
            print("Smile image received:", smile_image.name, "Size:", smile_image.size)
        else:
            print("No smile image received!")
        if angry_image:
            print("Angry image received:", angry_image.name, "Size:", angry_image.size)
        else:
            print("No angry image received!")
        
        if not username or not smile_image or not angry_image:
            return JsonResponse({'error': 'Missing username or images.'}, status=400)
        
        # Save the user profile (Django will store files in the defined MEDIA_ROOT)
        user_profile = UserProfile(username=username, smile_image=smile_image, angry_image=angry_image)
        user_profile.save()
        print("User profile saved successfully:", user_profile)
        return JsonResponse({'message': 'User registered successfully'})
    
    return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

def compare_images(image1, image2):
    """
    A simple function that compares two images using grayscale histograms.
    Returns a correlation value between the images.
    """
    # Convert to grayscale if necessary.
    if len(image1.shape) == 3:
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    else:
        gray1 = image1

    if len(image2.shape) == 3:
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    else:
        gray2 = image2
    
