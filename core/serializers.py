from rest_framework import serializers
from core.models import Fornecedor, Estado, Cidade
import requests

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['nome', 'uf']


class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = Cidade
        fields = ['nome', 'estado']

class FornecedorSerializer(serializers.ModelSerializer):
    cidade = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Fornecedor
        fields = '__all__' 

    def get_cidade(self, obj):
        return CidadeSerializer(obj.cidade).data
    
    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
    

    def create(self, validated_data):
        response_cnpj = requests.get(f'https://receitaws.com.br/v1/cnpj/{validated_data.get('cnpj')}')  

        if response_cnpj.status_code == 200:

            dados_convertidos = response_cnpj.json()
            
            validated_data['logradouro'] = dados_convertidos.get('logradouro', '')
            validated_data['numero'] = dados_convertidos.get('numero', '')  
            validated_data['complemento'] = dados_convertidos.get('complemento', '')
            validated_data['bairro'] = dados_convertidos.get('bairro', '')
            validated_data['cep'] = dados_convertidos.get('cep', '')
        
        return Fornecedor.objects.create(**validated_data)

    