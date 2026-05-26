class Process:

    def __init__(
        self,
        pid,
        chegada,
        execucao,
        prioridade,
        deadline
    ):

        self.pid = pid
        self.chegada = chegada
        self.execucao = execucao
        self.restante = execucao

        self.prioridade = prioridade
        self.deadline = deadline

        self.inicio = None
        self.termino = None

    def __repr__(self):
        return f"{self.pid}"