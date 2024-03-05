from rest_framework.response import Response
from .serializers import RegionsSerializer
from .models import Regions
from rest_framework.views import APIView

class SnippetList(APIView):
    def get(self, request, format=None):
        snippets = Regions.objects.all()
        serializer = RegionsSerializer(snippets, many=True)
        return Response(serializer.data)