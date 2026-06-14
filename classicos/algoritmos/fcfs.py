def executar(sim):
    fila = sorted(sim.processos, key=lambda p: p.chegada)

    for proc in fila:
        if sim.tempo < proc.chegada:
            sim._adicionar_evento("IDLE", sim.tempo, proc.chegada, "ocioso")
            sim.tempo = proc.chegada

        proc.inicio = sim.tempo
        t_fim = sim.tempo + proc.execucao

        sim._adicionar_evento(proc.id, sim.tempo, t_fim, "execucao")

        proc.restante = 0
        proc.termino  = t_fim
        sim.tempo     = t_fim