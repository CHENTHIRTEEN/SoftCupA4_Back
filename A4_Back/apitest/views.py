import json

from django.http import HttpResponse
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['POST'])
def index(request):
    if request.method == 'POST':
        print("==================hello")
        return HttpResponse(json.dumps({"code": 200, "message": "success"}))
