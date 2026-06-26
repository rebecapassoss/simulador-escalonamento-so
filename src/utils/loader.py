import json

from models.process import Process

def load_processes(path):

    with open(path, "r") as f:
        dados = json.load(f)

    processos = []

    for p in dados["processos"]:

        processo = Process(
            pid=p["id"],
            chegada=p["chegada"],
            execucao=p["execucao"],
            prioridade=p["prioridade"],
            deadline=p["deadline"]
        )

        processos.append(processo)

    return dados, processos