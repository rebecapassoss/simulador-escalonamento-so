import copy
from core.processo import Processo

class Simulador:
    def __init__(self, processos, quantum, sobrecarga_contexto):
        self.processos = copy.deepcopy(processos)
        self.quantum = quantum
        self.sobrecarga = sobrecarga_contexto
        self.tempo = 0
        self.timeline = []
        self.trocas_contexto = 0

    def _adicionar_evento(self, proc_id, t_inicio, t_fim, tipo):
        self.timeline.append({
            "processo": proc_id,
            "t_inicio": t_inicio,
            "t_fim":    t_fim,
            "tipo":     tipo
        })

    def calcular_metricas(self):
        concluidos = [p for p in self.processos if p.termino is not None]
        n = len(concluidos)
        if n == 0:
            return {}
        tempo_total = max(p.termino for p in concluidos)
        tempo_ocioso = sum(
            e["t_fim"] - e["t_inicio"]
            for e in self.timeline if e["tipo"] == "ocioso"
        )
        return {
            "turnaround_medio": sum(p.turnaround for p in concluidos) / n,
            "espera_media":     sum(p.espera     for p in concluidos) / n,
            "throughput":       n / tempo_total,
            "pct_ocioso":       100 * tempo_ocioso / tempo_total if tempo_total else 0,
            "trocas_contexto":  self.trocas_contexto,
        }