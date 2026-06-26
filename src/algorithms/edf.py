class EDFScheduler:

    def run(self, processos):

        tempo = 0
        prontos = []
        gantt = []
        ativo_anterior = None

        while processos or prontos:

            for p in processos[:]:

                if p.chegada <= tempo:

                    prontos.append(p)
                    processos.remove(p)

            if prontos:

                menor = prontos[0]

                for p in prontos:
                    if p.deadline < menor.deadline:
                        menor = p

                if menor.inicio is None:
                    menor.inicio = tempo

                evento = {
                    "processo": menor.pid,
                    "tempo": tempo
                }

                if (
                    ativo_anterior is not None
                    and ativo_anterior != menor
                    and ativo_anterior.restante > 0
                ):
                    gantt[-1]["preempcao"] = True

                gantt.append(evento)

                menor.restante -= 1

                if menor.restante == 0:
                    menor.termino = tempo + 1
                    prontos.remove(menor)

                ativo_anterior = menor

            else:

                gantt.append({
                    "tempo": tempo,
                    "processo": "ocioso"
                })

                ativo_anterior = None

            tempo += 1

        return gantt