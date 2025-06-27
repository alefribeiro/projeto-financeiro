from datetime import timedelta
from rest_framework import serializers
from core.models.lancamento import (
    Lancamento,
    
)

class LancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = '__all__'
        
    def validate(self, attrs):
        valor = attrs['valor']
        valor_efetivado = attrs['valor_efetivado']

        
        if valor_efetivado and valor_efetivado < valor:
            print('faça uma copia')

        if attrs['data_efetivacao'] > attrs['vencimento']:
            raise serializers.ValidationError(
                "A data de efetivação não pode ser maior que o vencimento."
            )
        
        if valor < 0 or (valor_efetivado is not None and valor_efetivado < 0):
            raise serializers.ValidationError(
                "O valor e o valor efetivado não podem ser negativos."
            )
        
        return attrs
    
    def create(self, validated_data):
        valor = validated_data.get('valor')
        valor_efetivado = validated_data.get('valor_efetivado')
        repeticoes = validated_data.pop('repeticoes', 5)

        
        lancamento_principal = Lancamento.objects.create(**validated_data)

        novos_lancamentos = []

       
        if valor_efetivado is not None and valor_efetivado < valor:
            restante = valor - valor_efetivado
            novos_lancamentos.append(Lancamento(
                descricao=validated_data['descricao'],
                forma_pagamento=validated_data['forma_pagamento'],
                tipo=validated_data['tipo'],
                categoria=validated_data['categoria'],
                valor=restante,
                vencimento=validated_data['vencimento'] + timedelta(days=30),
                fornecedor=validated_data['fornecedor'],
            ))

      
        for i in range(1, repeticoes):
            novos_lancamentos.append(Lancamento(
                descricao=validated_data['descricao'],
                forma_pagamento=validated_data['forma_pagamento'],
                tipo=validated_data['tipo'],
                categoria=validated_data['categoria'],
                valor=validated_data['valor'],
                vencimento=validated_data['vencimento'] + timedelta(days=30 * i),
                fornecedor=validated_data['fornecedor'],
            ))

        if novos_lancamentos:
            Lancamento.objects.bulk_create(novos_lancamentos)

        return lancamento_principal
    
        
    # Data de efetivação não pode ser maior que o vencimento

       
    
    # Quando o valor_efetivado for menor que o valor deve-se
    # criar um novo registro copiando as mesmas informações,
    # exceto data_efetivado e valor_efetivado.
    # O valor deve ser o restante do que foi pago a menor
    
    # valor e valor_efetivado não podem ser negativos
    
    # Repetição do lançamento, com 30 dias de diferença entre cada
    # repetição