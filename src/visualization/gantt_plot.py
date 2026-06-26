import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def generate_gantt(gantt, algoritmo, processos):

    fig, ax = plt.subplots(figsize=(12, 4))

    processos_no_gantt = sorted(
        list(
            set(
                evento["processo"]
                for evento in gantt
            )
        )
    )

    posicoes = {
        processo: i
        for i, processo in enumerate(processos_no_gantt)
    }

    deadlines = {
        p.pid: p.deadline
        for p in processos
    }

    cores = {
        "P1": "tab:blue",
        "P2": "tab:orange",
        "P3": "tab:green",
        "P4": "tab:red",
        "P5": "tab:purple",
        "ocioso": "lightgray",
        "sobrecarga": "red"
    }

    tempo_max = max(
        evento["tempo"]
        for evento in gantt
    )

    ax.set_xticks(
        range(0, tempo_max + 2)
    )

    for evento in gantt:

        processo = evento["processo"]
        tempo = evento["tempo"]

        y = posicoes[processo]

        cor = cores.get(
            processo,
            "tab:blue"
        )

        # Execução depois do deadline fica em cinza escuro
        if (
            processo in deadlines
            and tempo >= deadlines[processo]
        ):
            cor = "gray"

        ax.barh(
            y=y,
            width=1,
            left=tempo,
            height=0.5,
            color=cor,
            edgecolor="black"
        )

        cor_texto = "black" if cor == "lightgray" else "white"

        ax.text(
            tempo + 0.5,
            y,
            processo,
            ha="center",
            va="center",
            fontsize=8,
            color=cor_texto
        )

    # Linhas verticais de deadline
    for p in processos:

        ax.axvline(
            x=p.deadline,
            linestyle="--",
            linewidth=1,
            alpha=0.6,
            color="black"
        )

        ax.text(
            p.deadline,
            len(posicoes) - 0.2,
            f"D {p.pid}",
            rotation=90,
            fontsize=7,
            ha="right",
            va="top"
        )

    ax.set_yticks(
        list(posicoes.values())
    )

    ax.set_yticklabels(
        list(posicoes.keys())
    )

    ax.set_xlabel("Tempo")

    ax.set_ylabel("Processos")

    ax.set_title(
        f"Diagrama de Gantt - {algoritmo.upper()}"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.5
    )

    legenda = [
        Patch(facecolor="lightgray", label="CPU ociosa"),
        Patch(facecolor="red", label="Sobrecarga de contexto"),
        Patch(facecolor="gray", label="Execução após deadline"),
        Patch(facecolor="white", edgecolor="black", label="Linha de deadline")
    ]

    ax.legend(handles=legenda)

    deadline_max = max(
        p.deadline
        for p in processos
    )

    limite_x = max(
        tempo_max + 1,
        deadline_max + 1
    )

    ax.set_xlim(
        0,
        limite_x
    )

    ax.set_xticks(
        range(0, limite_x + 1)
    )

    plt.tight_layout()

    path = (
        f"outputs/gantt/"
        f"{algoritmo.lower()}_gantt.png"
    )

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()