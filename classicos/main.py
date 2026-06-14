import json
from core.processo import Processo
from core.simulador import Simulador
from algoritmos import fcfs, sfj

def carregar_json(caminho):
    with open(caminho) as f:
        dados = json.load(f)
    processos = [Processo(**p) for p in dados["processos"]]
    return processos, dados["quantum"], dados["sobrecarga_contexto"]

def imprimir_resultado(sim, nome):
    print(f"\n{'='*52}")
    print(f"  {nome}")
    print(f"{'='*52}")
    print(f"{'ID':<5} {'Início':<8} {'Término':<9} {'Espera':<8} {'Turnaround':<12} {'Prazo?'}")
    print("-"*52)
    for p in sim.processos:
        print(f"{p.id:<5} {p.inicio:<8} {p.termino:<9} "
              f"{p.espera:<8} {p.turnaround:<12} "
              f"{'OK' if p.deadline_ok else 'ESTOUROU'}")
    m = sim.calcular_metricas()
    print(f"\nTurnaround médio : {m['turnaround_medio']:.2f}")
    print(f"Espera média     : {m['espera_media']:.2f}")
    print(f"Throughput       : {m['throughput']:.4f} proc/ut")
    print(f"CPU ociosa       : {m['pct_ocioso']:.1f}%")

processos, quantum, sobrecarga = carregar_json("testes/caso_base.json")

# FCFS
sim = Simulador(processos, quantum, sobrecarga)
fcfs.executar(sim)
imprimir_resultado(sim, "FCFS")

# SJF
sim = Simulador(processos, quantum, sobrecarga)
sfj.executar(sim)
imprimir_resultado(sim, "SJF")

print("\nTimeline detalhada:")
for e in sim.timeline:
    print(f"  t={e['t_inicio']:>2}→{e['t_fim']:>2}  {e['processo']:<5}  ({e['tipo']})")