from dataclasses import dataclass, field

@dataclass
class Processo:
    id: str
    chegada: int
    execucao: int
    deadline: int
    prioridade: int

    restante: int = field(init=False)
    inicio: int = None
    termino: int = None

    def __post_init__(self):
        self.restante = self.execucao

    @property
    def turnaround(self):
        if self.termino is None:
            return None
        return self.termino - self.chegada

    @property
    def espera(self):
        if self.turnaround is None:
            return None
        return self.turnaround - self.execucao

    @property
    def deadline_ok(self):
        if self.termino is None:
            return None
        return self.termino <= self.deadline