class PriorityScheduler:

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

                maior = prontos[0]

                for p in prontos:
                    if p.prioridade < maior.prioridade:
                        maior = p

                if maior.inicio is None:
                    maior.inicio = tempo

                evento = {
                    "processo": maior.pid,
                    "tempo": tempo
                }

                if (
                    ativo_anterior is not None
                    and ativo_anterior != maior
                    and ativo_anterior.restante > 0
                ):
                    evento["preempcao"] = True

                gantt.append(evento)

                maior.restante -= 1

                if maior.restante == 0:
                    maior.termino = tempo + 1
                    prontos.remove(maior)

                ativo_anterior = maior

            else:

                gantt.append({
                    "tempo": tempo,
                    "processo": "ocioso"
                })

                ativo_anterior = None

            tempo += 1

        return gantt