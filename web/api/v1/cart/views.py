import logging
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


# Create your views here.

class CartAddView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        return Response({})
