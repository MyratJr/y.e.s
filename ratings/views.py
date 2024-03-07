# from .serializers import *
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import Rate_User
# from users.models import User
# from django.http import Http404
# from rest_framework import mixins, generics, permissions, status
# from rest_framework.parsers import MultiPartParser, FormParser


# class User_CommentsAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def get(self, request, pk, format=None):
#         try:
#             user = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404()
#         snippets = Rate_User.objects.filter(rated_user=user)
#         serializer = User_CommentsSerializer(snippets, many=True)
#         user_serializer = User_data_Serializer(user)
#         return Response([user_serializer.data, serializer.data])


# class Leave_CommentAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Rate_User.objects.all()
#     serializer_class = Leave_Comment_Serializer
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         rated_user_id = serializer.validated_data.get('rated_user')
#         user = User.objects.get(pk=rated_user_id.id)
#         user.point_counter += 1
#         user.rate_point_total += serializer.validated_data.get('rate_number')
#         user.rate_point = user.rate_point_total / user.point_counter
#         user.save()
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)