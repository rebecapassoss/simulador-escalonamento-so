class EDFScheduler:

    def run(self, processos):

        tempo = 0
        prontos = []
        gantt = []

        processos = [
            {
                "id": p.pid,
                "tempo_chegada": p.chegada,
                "execucao": p.execucao,
                "deadline": p.deadline
            }
            for p in processos
        ]

        while processos or prontos:

            for p in processos[:]:

                if p['tempo_chegada'] <= tempo:

                    prontos.append(p)
                    processos.remove(p)

            if prontos:

                menor = prontos[0]

                for p in prontos:

                    if p['deadline'] < menor['deadline']:

                        menor = p

                gantt.append({
                    'processo': menor['id'],
                    'tempo': tempo
                })

                menor['execucao'] -= 1

                if menor['execucao'] == 0:

                    prontos.remove(menor)

            else:

                gantt.append({
                    "tempo": tempo,
                    "processo": "ocioso"
                })

            tempo += 1

        return gantt