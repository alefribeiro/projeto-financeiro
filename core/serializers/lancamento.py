from datetime import timedelta
from rest_framework import serializers
from core.models.lancamento import Lancamento


class LancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = '__all__'

    def validate(self, attrs):
        valor = attrs.get('valor')
        valor_efetivado = attrs.get('valor_efetivado')
        data_efetivacao = attrs.get('data_efetivacao')
        vencimento = attrs.get('vencimento')

        if data_efetivacao and data_efetivacao > vencimento:
            raise serializers.ValidationError(
                "A data de efetivação não pode ser maior que o vencimento."
            )

        if valor < 0 or (valor_efetivado is not None and valor_efetivado < 0):
            raise serializers.ValidationError(
                "O valor e o valor efetivado não podem ser negativos."
            )

        return attrs

    def create(self, validated_data):
        repeticoes = validated_data.pop('repeticoes', 5)
        valor = validated_data.get('valor')
        valor_efetivado = validated_data.get('valor_efetivado')
        vencimento = validated_data.get('vencimento')

        
        lancamento_principal = Lancamento.objects.create(**validated_data)

        novos_lancamentos = []

       
        if valor_efetivado is not None and valor_efetivado < valor:
            restante = valor - valor_efetivado
            novos_lancamentos.append(Lancamento(
                **self._build_lancamento_data(validated_data, restante, vencimento + timedelta(days=30))
            ))

        
        for i in range(1, repeticoes):
            novos_lancamentos.append(Lancamento(
                **self._build_lancamento_data(validated_data, valor, vencimento + timedelta(days=30 * i))
            ))

        if novos_lancamentos:
            Lancamento.objects.bulk_create(novos_lancamentos)

        return lancamento_principal

    def _build_lancamento_data(self, base_data, valor, vencimento):
        return {
            'descricao': base_data['descricao'],
            'forma_pagamento': base_data['forma_pagamento'],
            'tipo': base_data['tipo'],
            'categoria': base_data['categoria'],
            'valor': valor,
            'vencimento': vencimento,
            'fornecedor': base_data['fornecedor'],
        }

        
    # Data de efetivação não pode ser maior que o vencimento

       
    
    # Quando o valor_efetivado for menor que o valor deve-se
    # criar um novo registro copiando as mesmas informações,
    # exceto data_efetivado e valor_efetivado.
    # O valor deve ser o restante do que foi pago a menor
    
    # valor e valor_efetivado não podem ser negativos
    
    # Repetição do lançamento, com 30 dias de diferença entre cada
    # repetição