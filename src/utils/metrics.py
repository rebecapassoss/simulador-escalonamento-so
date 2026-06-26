def count_trocas_contexto(gantt):

    trocas = 0

    eventos_processos = [
        evento["processo"]
        for evento in gantt
        if evento["processo"] not in ["ocioso", "sobrecarga"]
    ]

    for i in range(1, len(eventos_processos)):

        anterior = eventos_processos[i - 1]
        atual = eventos_processos[i]

        if anterior != atual:

            trocas += 1

    return trocas


def count_preempcoes(gantt):

    preempcoes = 0

    for evento in gantt:

        if evento.get("preempcao", False):

            preempcoes += 1

    return preempcoes


def calculate_metrics(gantt, processos, algoritmo):

    tempo_total = len(gantt)

    total_processos = len(processos)

    throughput = total_processos / tempo_total

    tempo_ocioso = sum(
        1
        for evento in gantt
        if evento["processo"] == "ocioso"
    )

    tempo_sobrecarga = sum(
        1
        for evento in gantt
        if evento["processo"] == "sobrecarga"
    )

    utilizacao_cpu = (
        (tempo_total - tempo_ocioso)
        / tempo_total
    ) * 100

    utilizacao_cpu_real = (
        (tempo_total - tempo_ocioso - tempo_sobrecarga)
        / tempo_total
    ) * 100

    trocas_contexto = count_trocas_contexto(gantt)

    if algoritmo.upper() in [
        "EDF",
        "CFS",
        "PRIORIDADE",
        "ROUND_ROBIN",
        "RR",
        "FCFS",
        "SJF",
        "EUA"
    ]:
        preempcoes = count_preempcoes(gantt)
    else:
        preempcoes = 0

    turnaround_medio = calculate_turnaround_medio(processos)

    waiting_time_medio = calculate_waiting_time_medio(processos)

    response_time_medio = calculate_response_time_medio(processos)

    deadline_miss = calculate_deadline_miss(processos)

    deadline_miss_rate = round(
        (deadline_miss / total_processos) * 100,
        2
    )

    return {
        "tempo_total": tempo_total,
        "throughput": round(throughput, 4),
        "tempo_ocioso": tempo_ocioso,
        "tempo_sobrecarga": tempo_sobrecarga,
        "utilizacao_cpu": round(utilizacao_cpu, 2),
        "utilizacao_cpu_real": round(utilizacao_cpu_real, 2),
        "trocas_contexto": trocas_contexto,
        "preempcoes": preempcoes,
        "turnaround_medio": turnaround_medio,
        "waiting_time_medio": waiting_time_medio,
        "response_time_medio": response_time_medio,
        "deadline_miss": deadline_miss,
        "deadline_miss_rate": deadline_miss_rate
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

def calculate_waiting_time_medio(processos):

    soma = 0

    for p in processos:

        turnaround = p.termino - p.chegada

        espera = turnaround - p.execucao

        soma += espera

    return round(
        soma / len(processos),
        2
    )

def calculate_response_time_medio(processos):

    soma = 0

    for p in processos:

        response = p.inicio - p.chegada

        soma += response

    return round(
        soma / len(processos),
        2
    )

def calculate_deadline_miss(processos):

    perdas = 0

    for p in processos:

        if p.termino > p.deadline:

            perdas += 1

    return perdas