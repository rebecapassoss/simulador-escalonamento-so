from dataclasses import dataclass
from typing import List, Optional


# ── Estrutura que os algoritmos devem preencher ──────────────────────────────

@dataclass
class EntradaGantt:
    processo: str   # id do processo, ex: "P1". Use "IDLE" pra CPU ociosa e "SO" pra sobrecarga
    inicio: int     # tempo em que começou
    fim: int        # tempo em que terminou


# ── Geração do Gantt em texto no terminal ────────────────────────────────────

CORES = {
    "IDLE": "\033[90m",   # cinza
    "SO":   "\033[33m",   # amarelo
}
CORES_PROCESSO = [
    "\033[94m",  # azul
    "\033[92m",  # verde
    "\033[91m",  # vermelho
    "\033[95m",  # magenta
    "\033[96m",  # ciano
]
RESET = "\033[0m"
BLOCO = "█"


def imprimir_gantt(entradas: List[EntradaGantt], largura_bloco: int = 2):
    """
    Imprime o gráfico de Gantt no terminal.

    Exemplo de saída:
    ┌─────────────────────────────┐
    │ Gráfico de Gantt            │
    └─────────────────────────────┘
    P1  ████░░░░
    P2  ░░░░████
        0   2   4   6   8

    Parâmetros:
        entradas      — lista de EntradaGantt produzida pelo algoritmo
        largura_bloco — quantos caracteres cada unidade de tempo ocupa (padrão 2)
    """
    if not entradas:
        print("Gantt vazio — nenhuma entrada para exibir.")
        return

    tempo_total = max(e.fim for e in entradas)
    processos = _ordem_processos(entradas)
    mapa_cores = _mapear_cores(processos)

    print("\n┌─────────────────────────────┐")
    print("│      Gráfico de Gantt       │")
    print("└─────────────────────────────┘")

    for proc in processos:
        linha = _montar_linha(proc, entradas, tempo_total, largura_bloco, mapa_cores)
        rotulo = f"{proc:<5}"
        print(f"  {rotulo} {linha}")

    _imprimir_eixo_tempo(tempo_total, largura_bloco)
    print()


def _ordem_processos(entradas: List[EntradaGantt]) -> List[str]:
    """Retorna os processos na ordem em que aparecem, com IDLE e SO por último."""
    vistos = []
    especiais = {"IDLE", "SO"}
    for e in entradas:
        if e.processo not in vistos and e.processo not in especiais:
            vistos.append(e.processo)
    for especial in ["SO", "IDLE"]:
        if any(e.processo == especial for e in entradas):
            vistos.append(especial)
    return vistos


def _mapear_cores(processos: List[str]) -> dict:
    cor_idx = 0
    mapa = {}
    for p in processos:
        if p in CORES:
            mapa[p] = CORES[p]
        else:
            mapa[p] = CORES_PROCESSO[cor_idx % len(CORES_PROCESSO)]
            cor_idx += 1
    return mapa


def _montar_linha(
    processo: str,
    entradas: List[EntradaGantt],
    tempo_total: int,
    largura_bloco: int,
    mapa_cores: dict,
) -> str:
    cor = mapa_cores.get(processo, "")
    linha = ""
    for t in range(tempo_total):
        ocupado = any(e.processo == processo and e.inicio <= t < e.fim for e in entradas)
        if ocupado:
            linha += f"{cor}{BLOCO * largura_bloco}{RESET}"
        else:
            linha += "░" * largura_bloco
    return linha


def _imprimir_eixo_tempo(tempo_total: int, largura_bloco: int):
    """Imprime a régua de tempo embaixo do gráfico."""
    eixo = ""
    for t in range(tempo_total + 1):
        marcador = str(t)
        eixo += marcador.ljust(largura_bloco)
    print(f"  {'':5} {eixo}")


# ── Conversão do formato bruto dos algoritmos ───────────────────────────────

def converter_gantt(gantt_bruto: list) -> List[EntradaGantt]:
    """
    Converte o formato bruto produzido pelos algoritmos (tick a tick) para
    uma lista de EntradaGantt (inicio/fim).

    Formato de entrada (um dict por tick):
        [
            {'processo': 'P1', 'tempo': 0},
            {'processo': 'P1', 'tempo': 1},
            {'processo': 'P2', 'tempo': 2},
            {'processo': 'ocioso', 'tempo': 3},
        ]

    Formato de saída:
        [
            EntradaGantt('P1',    inicio=0, fim=2),
            EntradaGantt('P2',    inicio=2, fim=3),
            EntradaGantt('IDLE',  inicio=3, fim=4),
        ]
    """
    if not gantt_bruto:
        return []

    entradas = []
    processo_atual = _normalizar_nome(gantt_bruto[0]['processo'])
    inicio_atual = gantt_bruto[0]['tempo']

    for tick in gantt_bruto[1:]:
        nome = _normalizar_nome(tick['processo'])
        if nome != processo_atual:
            entradas.append(EntradaGantt(processo_atual, inicio_atual, tick['tempo']))
            processo_atual = nome
            inicio_atual = tick['tempo']

    # fecha a última entrada
    ultimo_tempo = gantt_bruto[-1]['tempo'] + 1
    entradas.append(EntradaGantt(processo_atual, inicio_atual, ultimo_tempo))

    return entradas


def _normalizar_nome(nome: str) -> str:
    """Padroniza nomes especiais para IDLE e SO."""
    if nome.lower() in ("ocioso", "idle"):
        return "IDLE"
    if nome.lower() in ("so", "sobrecarga"):
        return "SO"
    return nome


# ── Exemplo de uso ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simula o vetor que um algoritmo produziria
    gantt = [
        EntradaGantt("P1", 0, 2),
        EntradaGantt("P2", 2, 4),
        EntradaGantt("SO", 4, 5),   # sobrecarga de contexto
        EntradaGantt("P1", 5, 7),
        EntradaGantt("IDLE", 7, 8), # CPU ociosa
        EntradaGantt("P3", 8, 10),
    ]

    imprimir_gantt(gantt)

if __name__ == "__main__":
    # Simula o vetor bruto que os algoritmos produzem (tick a tick)
    gantt_bruto = [
        {'processo': 'P1', 'tempo': 0},
        {'processo': 'P1', 'tempo': 1},
        {'processo': 'P2', 'tempo': 2},
        {'processo': 'P2', 'tempo': 3},
        {'processo': 'ocioso', 'tempo': 4},
        {'processo': 'P1', 'tempo': 5},
        {'processo': 'P1', 'tempo': 6},
        {'processo': 'P3', 'tempo': 7},
        {'processo': 'P3', 'tempo': 8},
        {'processo': 'P3', 'tempo': 9},
    ]

    entradas = converter_gantt(gantt_bruto)
    imprimir_gantt(entradas)
