from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models.lancamento import Lancamento
from core.serializers.lancamento import LancamentoSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class LancamentoViewSet(APIView):
    
    def get_object(self, pk):
        try:
            return Lancamento.objects.get(pk=pk)
        except Lancamento.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None):
        if pk:
            lancamento = Lancamento.objects.get(id=pk)
            
            serializer = LancamentoSerializer(lancamento)
            return JsonResponse(serializer.data, safe=False)

        lancamentos = Lancamento.objects.all()
        serializer = LancamentoSerializer(lancamentos, many=True)
        return JsonResponse(serializer.data, safe=False)
    

    def post(self, request):
        serializer = LancamentoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = LancamentoSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        lancamento = self.get_object(pk)
        lancamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
