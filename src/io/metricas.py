def calcular_metricas(processos: list) -> list:
    """
    Recebe uma lista de objetos Process e retorna uma lista de dicts
    com as métricas calculadas de cada processo.

    Campos esperados no objeto Process:
        pid, chegada, execucao, inicio, termino
    """
    resultados = []
    for p in processos:
        if p.inicio is None or p.termino is None:
            continue  # processo não foi executado

        turnaround    = p.termino - p.chegada
        tempo_espera  = turnaround - p.execucao
        tempo_resposta = p.inicio - p.chegada

        resultados.append({
            "pid":             p.pid,
            "chegada":         p.chegada,
            "execucao":        p.execucao,
            "inicio":          p.inicio,
            "termino":         p.termino,
            "turnaround":      turnaround,
            "tempo_espera":    tempo_espera,
            "tempo_resposta":  tempo_resposta,
        })

    return resultados


def imprimir_tabela(processos: list):
    """
    Imprime a tabela de métricas no terminal.

    Exemplo de saída:
    ┌──────────────────────────────────────────────────────────────────┐
    │                      Tabela de Métricas                         │
    └──────────────────────────────────────────────────────────────────┘
    PID   Chegada  Execução  Início  Término  Turnaround  Espera  Resposta
    P1        0        5       0        5          5         0        0
    P2        1        4       5        9          8         4        4
    P3        3        6       9       15         12         6        6
    ──────────────────────────────────────────────────────────────────
    Média                                          8.3       3.3      3.3
    """
    metricas = calcular_metricas(processos)

    if not metricas:
        print("Nenhum processo finalizado para exibir métricas.")
        return

    print("\n┌──────────────────────────────────────────────────────────────────┐")
    print("│                      Tabela de Métricas                          │")
    print("└──────────────────────────────────────────────────────────────────┘")

    cab = f"{'PID':<6} {'Chegada':>8} {'Execução':>9} {'Início':>7} {'Término':>8} {'Turnaround':>11} {'Espera':>7} {'Resposta':>9}"
    print(cab)
    print("─" * len(cab))

    for m in metricas:
        print(
            f"{m['pid']:<6} {m['chegada']:>8} {m['execucao']:>9} "
            f"{m['inicio']:>7} {m['termino']:>8} "
            f"{m['turnaround']:>11} {m['tempo_espera']:>7} {m['tempo_resposta']:>9}"
        )

    print("─" * len(cab))

    n = len(metricas)
    media_turnaround  = sum(m["turnaround"]      for m in metricas) / n
    media_espera      = sum(m["tempo_espera"]    for m in metricas) / n
    media_resposta    = sum(m["tempo_resposta"]  for m in metricas) / n

    print(
        f"{'Média':<6} {'':>8} {'':>9} {'':>7} {'':>8} "
        f"{media_turnaround:>11.1f} {media_espera:>7.1f} {media_resposta:>9.1f}"
    )
    print()


def salvar_metricas(processos: list, caminho: str = "outputs/metricas.txt"):
    """
    Salva a tabela de métricas em um arquivo de texto.
    """
    import io
    import sys

    # captura o print da tabela e salva no arquivo
    buffer = io.StringIO()
    sys.stdout = buffer
    imprimir_tabela(processos)
    sys.stdout = sys.__stdout__

    with open(caminho, "w") as f:
        f.write(buffer.getvalue())

    print(f"Métricas salvas em '{caminho}'.")


# ── Exemplo de uso ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simula objetos Process após a simulação
    class ProcessoFake:
        def __init__(self, pid, chegada, execucao, inicio, termino):
            self.pid = pid
            self.chegada = chegada
            self.execucao = execucao
            self.inicio = inicio
            self.termino = termino

    processos = [
        ProcessoFake("P1", chegada=0, execucao=5, inicio=0,  termino=5),
        ProcessoFake("P2", chegada=1, execucao=4, inicio=5,  termino=9),
        ProcessoFake("P3", chegada=3, execucao=6, inicio=9,  termino=15),
    ]

    imprimir_tabela(processos)
    salvar_metricas(processos)
