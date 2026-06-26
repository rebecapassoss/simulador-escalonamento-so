import csv
import os


def save_comparison(resultados):

    path = "outputs/comparison/comparison.csv"

    campos = [
        "algoritmo",
        "tempo_total",
        "throughput",
        "tempo_ocioso",
        "tempo_sobrecarga",
        "utilizacao_cpu",
        "utilizacao_cpu_real",
        "trocas_contexto",
        "preempcoes",
        "turnaround_medio",
        "waiting_time_medio",
        "response_time_medio",
        "deadline_miss",
        "deadline_miss_rate"
    ]

    with open(path, "w", newline="") as f:

        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()

        for resultado in resultados:
            writer.writerow(resultado)