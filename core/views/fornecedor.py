from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models.fornecedor import FornecedorModel
from core.serializers.fornecedor import FornecedorSerializer
from rest_framework.views import APIView


class FornecedorView(APIView):

    def get (self, request, pk=None):
        if pk:
            try:
                fornecedor = FornecedorModel.objects.get(pk=pk)
            except FornecedorModel.DoesNotExist:
                return JsonResponse({'error': 'Fornecedor not found'}, status=404)
            serializer = FornecedorSerializer(fornecedor)
            return JsonResponse(serializer.data)
        
        fornecedor = FornecedorModel.objects.all()
        serializer = FornecedorSerializer(fornecedor, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):  
        data = JSONParser().parse(request)
        serializer = FornecedorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)