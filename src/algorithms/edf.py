class EDFScheduler:

    def run(self, processos):

        tempo = 0
        prontos = []
        gantt = []

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

                gantt.append({
                    "processo": menor.pid,
                    "tempo": tempo
                })

                menor.restante -= 1

                if menor.restante == 0:

                    menor.termino = tempo + 1

                    prontos.remove(menor)

            else:

                gantt.append({
                    "tempo": tempo,
                    "processo": "ocioso"
                })

            tempo += 1

        return gantt