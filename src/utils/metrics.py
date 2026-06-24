def count_preemptions(gantt):

    preempcoes = 0

    for i in range(1, len(gantt)):

        anterior = gantt[i - 1]["processo"]
        atual = gantt[i]["processo"]

        if anterior != atual:

            if anterior != "ocioso" and atual != "ocioso":

                preempcoes += 1

    return preempcoes


def calculate_metrics(gantt, processos):

    tempo_total = len(gantt)

    total_processos = len(processos)

    throughput = total_processos / tempo_total

    tempo_ocioso = sum(
        1
        for evento in gantt
        if evento["processo"] == "ocioso"
    )

    utilizacao_cpu = (
        (tempo_total - tempo_ocioso)
        / tempo_total
    ) * 100

    preempcoes = count_preemptions(gantt)

    total_processos = len(processos)

    turnaround_medio = calculate_turnaround_medio(processos)

    return {
        "tempo_total": tempo_total,
        "throughput": round(throughput, 4),
        "tempo_ocioso": tempo_ocioso,
        "utilizacao_cpu": round(utilizacao_cpu, 2),
        "preempcoes": preempcoes,
        "turnaround_medio": turnaround_medio
    }

def calculate_turnaround_medio(processos):

    soma = 0

    for p in processos:

        turnaround = p.termino - p.chegada

        soma += turnaround

    return round(
        soma / len(processos),
        2
    )