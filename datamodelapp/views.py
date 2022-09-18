from django.shortcuts import render
from rest_framework.views import APIView
from .models import DataModel
from .serializers import DataModelSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.parsers import FileUploadParser

# Create your views here.
class DataModelList(APIView):
    def get(self, request):
        models = DataModel.objects.all()
        serializer = DataModelSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DataModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DataModelView(APIView):
    def get_object(self, pk):
        try:
            return DataModel.objects.get(pk=pk)
        except DataModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk)
        serializer = DataModelSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk):
        model = self.get_object(pk)
        serializer = DataModelSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        model = self.get_object(pk)
        model.delete()
        return Response(status=status.HTTP_200_OK)