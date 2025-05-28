from django.http import  JsonResponse
from rest_framework.parsers import JSONParser
from core.models.fornecedor import Fornecedor
from core.serializers.fornecedor import FornecedorSerializer
from rest_framework.views import APIView
from django.db import IntegrityError, transaction


class FornecedorView(APIView):

    def get (self, request, pk=None):
        if pk:
            try:
                fornecedor = Fornecedor.objects.get(pk=pk)
            except Fornecedor.DoesNotExist:
                return JsonResponse({'error': 'Fornecedor not found'}, status=404)
            serializer = FornecedorSerializer(fornecedor)
            return JsonResponse(serializer.data)
        
        fornecedor = Fornecedor.objects.all()
        serializer = FornecedorSerializer(fornecedor, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    @transaction.atomic
    def post(self, request):  
        data = JSONParser().parse(request)

        telefones = data.pop('telefones')
        serializer = FornecedorSerializer(data=data)

        if serializer.is_valid():
            fornecedor = serializer.save()

            for telefone in telefones:
                fornecedor.telefones.create(telefone=telefone)
            return JsonResponse(serializer.data, status=201)
           
            
        return JsonResponse(serializer.errors, status=400)