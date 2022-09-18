from rest_framework.views import APIView
from .models import AnalysisRun
from .serializers import AnalysisRunSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, JsonResponse, HttpResponse
from rest_framework.parsers import FileUploadParser
from datamodelapp.models import DataModel
from cdaengine.cfenginetest import CfEngineTest
import json

# Create your views here.
class AnalysisRunList(APIView):
    def get(self, request):
        models = AnalysisRun.objects.all()
        serializer = AnalysisRunSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnalysisRunSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnalysisRunView(APIView):
    def get_object(self, pk):
        try:
            return AnalysisRun.objects.get(pk=pk)
        except AnalysisRun.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk)
        serializer = AnalysisRunSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk):
        model = self.get_object(pk)
        serializer = AnalysisRunSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        model = self.get_object(pk)
        model.delete()
        return Response(status=status.HTTP_200_OK)

class AnalyzerView(APIView):
    def get(self, request, pk):
        try:
            run = AnalysisRun.objects.get(pk=pk)
            samplefile = run.samplefile
            modelfile = (DataModel.objects.get(pk=run.modelname)).modelfile
            print(samplefile.path)
            print(modelfile.path)

            # Analyze the sample file with the model
            cftest = CfEngineTest()
            resultstring = cftest.executesinglemodel(samplefile.path, modelfile.path)
            jsonstring = json.dumps(resultstring)
            print(jsonstring)

            run.result = jsonstring
            run.save()

        except AnalysisRun.DoesNotExist:
            raise Http404

        return Response(resultstring, status=status.HTTP_200_OK)

