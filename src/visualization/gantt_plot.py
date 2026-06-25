import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def generate_gantt(gantt, algoritmo):

    fig, ax = plt.subplots(figsize=(12, 4))

    processos = sorted(
        list(
            set(
                evento["processo"]
                for evento in gantt
                
            )
        )

    )

    posicoes = {
        processo: i
        for i, processo in enumerate(processos)
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


        ax.barh(
            y=y,
            width=1,
            left=tempo,
            height=0.5,
            color=cor,
            edgecolor="black"
        )

        ax.text(
            tempo + 0.5,
            y,
            processo,
            ha="center",
            va="center",
            fontsize=8,
            color="white"
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
        f"Diagrama Gantt - {algoritmo.upper()}"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.5
    )

    legenda = [
    Patch(facecolor="lightgray", label="CPU Ociosa"),
    Patch(facecolor="red", label="Troca de Contexto")
]

    ax.legend(handles=legenda)


    ax.set_xlim(
    0,
    tempo_max + 1
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