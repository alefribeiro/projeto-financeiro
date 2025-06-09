from django.core.management.base import BaseCommand
from core.models.fornecedor import Fornecedor


class Command(BaseCommand):

    def add_arguments(self, parser):
        print("TEste")
        
    def handle(self, *args, **options):
        cnpj = "06347409006953"
        objeto, _ = Fornecedor.objects.get_or_create(cnpj=cnpj, defaults={'nome': 'Álef'})

        print(objeto, _)