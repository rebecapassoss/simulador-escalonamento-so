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
                p["id"],
                p["tempo_chegada"],
                p["execucao"],
                p["prioridade"],
                p["deadline"]
            ])