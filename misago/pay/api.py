from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['GET'])
def gen_payment_url(request):
    return JsonResponse({"test": "xiaodong"})
