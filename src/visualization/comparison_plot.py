import csv
import os

import matplotlib.pyplot as plt


def read_comparison_csv():

    path_csv = "outputs/comparison/comparison.csv"

    if not os.path.exists(path_csv):
        raise FileNotFoundError(
            "Arquivo outputs/comparison/comparison.csv não encontrado."
        )

    dados = []

    with open(path_csv, "r") as f:

        reader = csv.DictReader(f)

        for row in reader:
            dados.append(row)

    return dados


def generate_time_metrics_chart(dados):

    algoritmos = [
        row["algoritmo"]
        for row in dados
    ]

    turnaround = [
        float(row["turnaround_medio"])
        for row in dados
    ]

    waiting = [
        float(row["waiting_time_medio"])
        for row in dados
    ]

    response = [
        float(row["response_time_medio"])
        for row in dados
    ]

    x = range(len(algoritmos))
    largura = 0.25

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.bar(
        [i - largura for i in x],
        turnaround,
        width=largura,
        label="Turnaround médio"
    )

    ax.bar(
        x,
        waiting,
        width=largura,
        label="Waiting time médio"
    )

    ax.bar(
        [i + largura for i in x],
        response,
        width=largura,
        label="Response time médio"
    )

    ax.set_title("Comparação de tempos médios por algoritmo")
    ax.set_xlabel("Algoritmos")
    ax.set_ylabel("Tempo médio")

    ax.set_xticks(list(x))
    ax.set_xticklabels(algoritmos)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    ax.legend()

    plt.tight_layout()

    plt.savefig(
        "outputs/comparison/comparison_tempos.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def generate_deadline_chart(dados):

    algoritmos = [
        row["algoritmo"]
        for row in dados
    ]

    deadline_miss_rate = [
        float(row["deadline_miss_rate"])
        for row in dados
    ]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        algoritmos,
        deadline_miss_rate
    )

    ax.set_title("Taxa de perda de deadline por algoritmo")
    ax.set_xlabel("Algoritmos")
    ax.set_ylabel("Deadline miss rate (%)")

    ax.set_ylim(0, 100)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/comparison/comparison_deadlines.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def generate_cpu_chart(dados):

    algoritmos = [
        row["algoritmo"]
        for row in dados
    ]

    utilizacao_cpu_real = [
        float(row["utilizacao_cpu_real"])
        for row in dados
    ]

    tempo_sobrecarga = [
        float(row["tempo_sobrecarga"])
        for row in dados
    ]

    x = range(len(algoritmos))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.bar(
        [i - largura / 2 for i in x],
        utilizacao_cpu_real,
        width=largura,
        label="Utilização real da CPU (%)"
    )

    ax.bar(
        [i + largura / 2 for i in x],
        tempo_sobrecarga,
        width=largura,
        label="Tempo de sobrecarga"
    )

    ax.set_title("Comparação de CPU e sobrecarga por algoritmo")
    ax.set_xlabel("Algoritmos")
    ax.set_ylabel("Valor")

    ax.set_xticks(list(x))
    ax.set_xticklabels(algoritmos)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    ax.legend()

    plt.tight_layout()

    plt.savefig(
        "outputs/comparison/comparison_cpu.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def generate_comparison_chart():

    dados = read_comparison_csv()

    generate_time_metrics_chart(dados)

    generate_deadline_chart(dados)

    generate_cpu_chart(dados)