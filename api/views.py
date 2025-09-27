from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def status(request):
    """
    Endpoint simples que retorna status OK.
    """
    return Response({"message": "OK"})
