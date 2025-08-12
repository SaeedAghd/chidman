from django.shortcuts import render
 
def features_view(request):
    return render(request, 'store_analysis/features.html') 