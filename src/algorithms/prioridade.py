class PriorityScheduler:

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
                maior = prontos[0]

                for p in prontos:
                    if p.prioridade > maior.prioridade:
                        maior = p

                    if maior.inicio is None:
                        maior.inicio = tempo


                gantt.append({
                    'processo': maior.pid,
                    'tempo': tempo
                })

                maior.restante -= 1

                if maior.restante == 0:
                    maior.termino = tempo + 1
                    prontos.remove(maior)
            else:
               
                gantt.append({
                    "tempo": tempo,
                    "processo": "ocioso"
                })
            tempo += 1
        return gantt