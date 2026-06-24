class EUAScheduler:
    """
    EUA - Escalonamento por Urgência Acumulada (algoritmo autoral).

    Motivação: o FIFO é injusto com quem chega depois e o Round Robin
    trata todos igual independente de quanto esperaram. A ideia é simples:
    cada processo acumula "urgência" a cada unidade de tempo que passa sem
    executar. Quem ficou mais tempo ignorado grita mais alto e vai primeiro.

    Regras:
    - Urgência começa em 0 quando o processo chega.
    - A cada unidade de tempo parado na fila, urgência += 1.
    - A CPU sempre escolhe o processo de maior urgência.
    - Empate: desempata por chegada (quem chegou antes).
    - Ao executar por uma fatia (quantum), urgência zera.
    - Preemptivo: a cada quantum, reavalia quem tem maior urgência.
    """

    def __init__(self, quantum=2, sobrecarga=1):
        self.quantum = quantum
        self.sobrecarga = sobrecarga

    def run(self, processos):
        import copy
        procs = copy.deepcopy(processos)

        # inicializa urgência de todos
        for p in procs:
            p.urgencia = 0

        tempo = 0
        gantt = []
        prontos = []
        nao_chegaram = sorted(procs, key=lambda p: p.chegada)
        em_sobrecarga = False
        ticks_sobrecarga = 0
        atual = None
        ticks_executando = 0

        def enfileirar_chegados():
            for p in nao_chegaram[:]:
                if p.chegada <= tempo:
                    prontos.append(p)
                    nao_chegaram.remove(p)

        enfileirar_chegados()

        while nao_chegaram or prontos or atual:

            # --- modo sobrecarga ---
            if em_sobrecarga:
                gantt.append({
                    "processo": "sobrecarga",
                    "tempo": tempo
                })
                ticks_sobrecarga += 1
                tempo += 1
                enfileirar_chegados()

                # acumula urgência de quem está esperando durante a sobrecarga
                for p in prontos:
                    p.urgencia += 1

                if ticks_sobrecarga >= self.sobrecarga:
                    em_sobrecarga = False
                    ticks_sobrecarga = 0
                    # processo preemptado volta para a fila com urgência zerada
                    if atual and atual.restante > 0:
                        atual.urgencia = 0
                        prontos.append(atual)
                    atual = None
                    ticks_executando = 0
                continue

            # --- seleciona processo se CPU livre ---
            if atual is None:
                enfileirar_chegados()
                if not prontos:
                    gantt.append({
                        "processo": "ocioso",
                        "tempo": tempo
                    })
                    tempo += 1
                    enfileirar_chegados()
                    continue

                # escolhe maior urgência; empate vai para quem chegou antes
                atual = max(prontos, key=lambda p: (p.urgencia, -p.chegada))
                prontos.remove(atual)
                ticks_executando = 0

            if atual.inicio is None:
                atual.inicio = tempo

            # --- executa 1 unidade ---
            gantt.append({
                "processo": atual.pid,
                "tempo": tempo
            })
            atual.restante -= 1
            ticks_executando += 1
            tempo += 1
            enfileirar_chegados()

            # acumula urgência de quem está esperando
            for p in prontos:
                p.urgencia += 1

            # --- processo terminou ---
            if atual.restante == 0:
                atual.termino = tempo
                atual = None
                ticks_executando = 0

            # --- quantum esgotado ---
            elif ticks_executando >= self.quantum:
                em_sobrecarga = True
                ticks_sobrecarga = 0

        return gantt