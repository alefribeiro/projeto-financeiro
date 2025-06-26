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
        
        return attrs
        
    # Data de efetivação não pode ser maior que o vencimento
    
    # Quando o valor_efetivado for menor que o valor deve-se
    # criar um novo registro copiando as mesmas informações,
    # exceto data_efetivado e valor_efetivado.
    # O valor deve ser o restante do que foi pago a menor
    
    # valor e valor_efetivado não podem ser negativos
    
    # Repetição do lançamento, com 30 dias de diferença entre cada
    # repetição