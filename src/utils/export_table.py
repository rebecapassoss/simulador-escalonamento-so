import csv


def calcular_inicios_por_processo(gantt):

    inicios = {}

    processo_anterior = None

    for evento in gantt:

        processo = evento["processo"]

        if processo in ["ocioso", "sobrecarga"]:
            processo_anterior = processo
            continue

        if processo != processo_anterior:

            if processo not in inicios:
                inicios[processo] = []

            inicios[processo].append(evento["tempo"])

        processo_anterior = processo

    return inicios


def save_table(processos, algoritmo, gantt=None):

    path = f"outputs/tables/{algoritmo.lower()}_table.csv"

    inicios_por_processo = {}

    if gantt is not None:
        inicios_por_processo = calcular_inicios_por_processo(gantt)

    with open(path, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "id",
            "chegada",
            "execucao",
            "prioridade",
            "deadline",
            "inicio",
            "inicios",
            "termino",
            "espera",
            "turnaround",
            "deadline_ok"
        ])

        for p in processos:

            turnaround = p.termino - p.chegada
            espera = turnaround - p.execucao
            deadline_ok = p.termino <= p.deadline

            inicios = inicios_por_processo.get(
                p.pid,
                [p.inicio]
            )

            writer.writerow([
                p.pid,
                p.chegada,
                p.execucao,
                p.prioridade,
                p.deadline,
                p.inicio,
                ";".join(str(i) for i in inicios),
                p.termino,
                espera,
                turnaround,
                deadline_ok
            ])