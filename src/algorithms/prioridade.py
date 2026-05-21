def executar_prioridade(processos):
    tempo =0
    prontos= []
    gantt=[]

    while processos or prontos:
        for p in processos[:]:
            if p['tempo_chegada'] <= tempo:
                prontos.append(p)
                processos.remove(p)
        if prontos:
            maior = prontos[0]
            for p in prontos:
                if p['prioridade'] > maior['prioridade']:
                    maior =p
            gantt.append({
                'processo': maior['id'],
                'tempo': tempo
            })
            maior['execucao'] -= 1
            if maior['execucao'] == 0:
                prontos.remove(maior)
        else:
            gantt.append({
                "tempo": tempo,
                "processo": "ocioso"
            })
        tempo += 1
    return gantt