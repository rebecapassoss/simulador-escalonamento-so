import csv

def save_table(processos, algoritmo):
    path = f"outputs/tables/{algoritmo.lower()}_table.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id",
            "chegada",
            "execucao",
            "prioridade",
            "deadline"
        ])
        for p in processos:
            writer.writerow([
                p.pid,        # era p["id"]
                p.chegada,    # era p["tempo_chegada"]
                p.execucao,   # era p["execucao"]
                p.prioridade, # era p["prioridade"]
                p.deadline    # era p["deadline"]
            ])