# minha_app/tasks.py

from celery import shared_task
import time

@shared_task
def minha_primeira_tarefa(x, y):
    print(f"Executando minha_primeira_tarefa com {x} e {y}")
    time.sleep(5)  # Simula uma tarefa demorada
    result = x + y
    print(f"minha_primeira_tarefa concluída. Resultado: {result}")
    return result

@shared_task
def tarefa_que_falha():
    raise ValueError("Essa tarefa falhou intencionalmente!")