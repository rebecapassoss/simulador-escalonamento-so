class FCFSScheduler:
    """
    FCFS - First Come, First Served (não preemptivo).

    Ordena os processos por chegada. Executa cada um do início
    ao fim sem interromper, independente do que chegue depois.
    """

    def run(self, processos):
        tempo = 0
        prontos = []
        gantt = []

        # cópia para não modificar a lista original
        fila = sorted(processos[:], key=lambda p: p.chegada)
        restantes = list(fila)

        while restantes or prontos:
            # adiciona na fila quem já chegou
            for p in restantes[:]:
                if p.chegada <= tempo:
                    prontos.append(p)
                    restantes.remove(p)

            if prontos:
                # FCFS: sempre o primeiro que chegou (fila já está ordenada)
                atual = prontos[0]

                if atual.inicio is None:
                    atual.inicio = tempo

                gantt.append({
                    "processo": atual.pid,
                    "tempo": tempo
                })

                atual.restante -= 1

                if atual.restante == 0:
                    atual.termino = tempo + 1
                    prontos.pop(0)
            else:
                # CPU ociosa: nenhum processo pronto ainda
                gantt.append({
                    "processo": "ocioso",
                    "tempo": tempo
                })

            tempo += 1

        return gantt