class SJFScheduler:
    """
    SJF - Shortest Job First (não preemptivo).

    Quando a CPU fica livre, escolhe o processo com menor
    tempo de execução dentre os que já chegaram.
    Uma vez que começou, não é interrompido.
    """

    def __init__(self):
        self.atual = None   # processo em execução no momento

    def run(self, processos):
        tempo = 0
        prontos = []
        gantt = []
        self.atual = None

        restantes = list(processos[:])

        while restantes or prontos:
            # adiciona quem chegou
            for p in restantes[:]:
                if p.chegada <= tempo:
                    prontos.append(p)
                    restantes.remove(p)

            if prontos:
                # só escolhe novo processo quando o atual terminar
                # (não preemptivo: não interrompe quem está rodando)
                if self.atual is None or self.atual.restante == 0:
                    self.atual = min(prontos, key=lambda p: p.execucao)

                if self.atual.inicio is None:
                    self.atual.inicio = tempo

                gantt.append({
                    "processo": self.atual.pid,
                    "tempo": tempo
                })

                self.atual.restante -= 1

                if self.atual.restante == 0:
                    self.atual.termino = tempo + 1
                    prontos.remove(self.atual)
                    self.atual = None
            else:
                gantt.append({
                    "processo": "ocioso",
                    "tempo": tempo
                })

            tempo += 1

        return gantt