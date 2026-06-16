from collections import deque

class RoundRobinScheduler:
    """
    Round Robin com quantum fixo e sobrecarga de contexto (preemptivo).

    Cada processo executa por no máximo `quantum` unidades de tempo.
    Se não terminou, vai para o fim da fila e a CPU registra a sobrecarga
    antes de continuar.

    Detalhe importante sobre ordem da fila:
    Processos que chegam durante uma fatia entram na fila
    ANTES do processo que acabou de ser preemptado.
    """

    def __init__(self, quantum=2, sobrecarga=1):
        self.quantum = quantum
        self.sobrecarga = sobrecarga

    def run(self, processos):
        tempo = 0
        gantt = []
        fila = deque()
        nao_chegaram = sorted(processos[:], key=lambda p: p.chegada)
        contador_quantum = 0   # quantas unidades o processo atual já executou
        atual = None
        em_sobrecarga = False
        ticks_sobrecarga = 0

        def enfileirar_chegados():
            for p in nao_chegaram[:]:
                if p.chegada <= tempo:
                    fila.append(p)
                    nao_chegaram.remove(p)

        enfileirar_chegados()

        while nao_chegaram or fila or atual:

            # --- modo sobrecarga: CPU ocupada com troca de contexto ---
            if em_sobrecarga:
                gantt.append({
                    "processo": "sobrecarga",
                    "tempo": tempo
                })
                ticks_sobrecarga += 1
                tempo += 1
                enfileirar_chegados()

                if ticks_sobrecarga >= self.sobrecarga:
                    em_sobrecarga = False
                    ticks_sobrecarga = 0
                    # processo preemptado volta para o fim da fila
                    if atual and atual.restante > 0:
                        fila.append(atual)
                    atual = None
                    contador_quantum = 0
                continue

            # --- seleciona próximo processo se CPU livre ---
            if atual is None:
                enfileirar_chegados()
                if not fila:
                    # ocioso
                    gantt.append({
                        "processo": "ocioso",
                        "tempo": tempo
                    })
                    tempo += 1
                    enfileirar_chegados()
                    continue
                atual = fila.popleft()
                contador_quantum = 0

            if atual.inicio is None:
                atual.inicio = tempo

            # --- executa 1 unidade ---
            gantt.append({
                "processo": atual.pid,
                "tempo": tempo
            })
            atual.restante -= 1
            contador_quantum += 1
            tempo += 1
            enfileirar_chegados()

            # --- processo terminou ---
            if atual.restante == 0:
                atual.termino = tempo
                atual = None
                contador_quantum = 0

            # --- quantum esgotado e processo ainda não terminou ---
            elif contador_quantum >= self.quantum:
                em_sobrecarga = True
                ticks_sobrecarga = 0

        return gantt