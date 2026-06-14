def executar(sim):
    """
    SJF — Shortest Job First (não preemptivo).

    Toda vez que a CPU fica livre, olha quem já chegou
    e escolhe o processo com MENOR tempo de execução.
    Uma vez que começou, não para.
    """
    pendentes = list(sim.processos)   # cópia para poder remover conforme executa

    while pendentes:
        # quem já chegou e ainda não rodou
        prontos = [p for p in pendentes if p.chegada <= sim.tempo]

        if not prontos:
            # ninguém pronto ainda: avança o tempo até o próximo chegar
            proxima = min(p.chegada for p in pendentes)
            sim._adicionar_evento("IDLE", sim.tempo, proxima, "ocioso")
            sim.tempo = proxima
            continue

        # ÚNICA diferença do FCFS: ordena por execucao, não por chegada
        proc = min(prontos, key=lambda p: p.execucao)
        pendentes.remove(proc)

        if sim.tempo < proc.chegada:
            sim._adicionar_evento("IDLE", sim.tempo, proc.chegada, "ocioso")
            sim.tempo = proc.chegada

        proc.inicio = sim.tempo
        t_fim = sim.tempo + proc.execucao

        sim._adicionar_evento(proc.id, sim.tempo, t_fim, "execucao")

        proc.restante = 0
        proc.termino  = t_fim
        sim.tempo     = t_fim