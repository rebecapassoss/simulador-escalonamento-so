import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Processo:
    id: str
    chegada: int
    execucao: int
    prioridade: int = 0
    deadline: Optional[int] = None
    num_paginas: int = 0

    # Campos preenchidos durante a simulação (não vêm do JSON)
    tempo_inicio: int = -1
    tempo_fim: int = -1
    tempo_restante: int = field(init=False)
    vruntime: float = 0.0  # usado pelo CFS

    def __post_init__(self):
        self.tempo_restante = self.execucao

    @property
    def turnaround(self) -> int:
        """Tempo total desde chegada até terminar."""
        if self.tempo_fim == -1:
            return -1
        return self.tempo_fim - self.chegada

    @property
    def tempo_espera(self) -> int:
        """Tempo que ficou na fila sem executar."""
        if self.tempo_fim == -1:
            return -1
        return self.turnaround - self.execucao


@dataclass
class ConfigSimulacao:
    seed: int
    quantum: int
    sobrecarga_contexto: int
    custo_disco: int
    processos: List[Processo]


def carregar_json(caminho: str) -> ConfigSimulacao:
    """
    Lê o arquivo JSON e retorna a configuração completa da simulação.

    Exemplo de JSON esperado:
    {
        "quantum": 2,
        "sobrecarga_contexto": 1,
        "custo_disco": 3,
        "seed": 42,
        "processos": [
            {"id": "P1", "chegada": 0, "execucao": 5, "deadline": 8, "prioridade": 2, "num_paginas": 6},
            {"id": "P2", "chegada": 1, "execucao": 4, "deadline": 12, "prioridade": 1, "num_paginas": 4}
        ]
    }
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with open(caminho, "r") as f:
        dados = json.load(f)

    _validar_json(dados, caminho)

    processos = []
    for i, p in enumerate(dados["processos"]):
        _validar_processo(p, i)
        processos.append(Processo(
            id=p["id"],
            chegada=p["chegada"],
            execucao=p["execucao"],
            prioridade=p.get("prioridade", 0),
            deadline=p.get("deadline", None),
            num_paginas=p.get("num_paginas", 0),
        ))

    return ConfigSimulacao(
        seed=dados.get("seed", 0),
        quantum=dados.get("quantum", 2),
        sobrecarga_contexto=dados.get("sobrecarga_contexto", 0),
        custo_disco=dados.get("custo_disco", 0),
        processos=processos,
    )


def _validar_json(dados: dict, caminho: str):
    """Verifica se os campos obrigatórios do JSON estão presentes."""
    if "processos" not in dados:
        raise ValueError(f"'{caminho}' não tem o campo 'processos'.")
    if not isinstance(dados["processos"], list) or len(dados["processos"]) == 0:
        raise ValueError("'processos' deve ser uma lista não vazia.")


def _validar_processo(p: dict, indice: int):
    """Verifica se um processo tem os campos obrigatórios e valores válidos."""
    campos_obrigatorios = ["id", "chegada", "execucao"]
    for campo in campos_obrigatorios:
        if campo not in p:
            raise ValueError(f"Processo [{indice}] está sem o campo obrigatório '{campo}'.")

    if p["execucao"] <= 0:
        raise ValueError(f"Processo '{p['id']}': 'execucao' deve ser maior que 0.")
    if p["chegada"] < 0:
        raise ValueError(f"Processo '{p['id']}': 'chegada' não pode ser negativa.")
    if "deadline" in p and p["deadline"] is not None:
        if p["deadline"] <= p["chegada"]:
            raise ValueError(f"Processo '{p['id']}': 'deadline' deve ser maior que 'chegada'.")


# ── Exemplo de uso ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    caminho = "inputs/caso1.json"

    try:
        config = carregar_json(caminho)
        print(f"Seed: {config.seed} | Quantum: {config.quantum} | "
              f"Sobrecarga: {config.sobrecarga_contexto} | Custo disco: {config.custo_disco}")
        print(f"Total de processos: {len(config.processos)}\n")
        for p in config.processos:
            print(f"  {p.id} | chegada={p.chegada} | execucao={p.execucao} "
                  f"| prioridade={p.prioridade} | deadline={p.deadline} "
                  f"| num_paginas={p.num_paginas}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Erro ao carregar JSON: {e}")
