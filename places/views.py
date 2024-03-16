from rest_framework.response import Response
from .serializers import RegionsSerializer
from rest_framework.views import APIView
from .models import Regions


class SnippetList(APIView):
    
    def get(self, request):
        snippets = Regions.objects.all()
        serializer = RegionsSerializer(snippets, many=True)
        return Response(serializer.data)