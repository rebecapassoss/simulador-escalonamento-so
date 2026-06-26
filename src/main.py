from utils.export_table import save_table
from utils.parser import parse_args
from utils.loader import load_processes
from utils.logger import setup_logger
from utils.directories import create_output_dirs
from utils.save_results import save_gantt, save_metrics
from utils.metrics import calculate_metrics
from utils.export_comparison import save_comparison

from algorithms.edf import EDFScheduler
from algorithms.prioridade import PriorityScheduler
from algorithms.cfs import CFSScheduler
from algorithms.fcfs import FCFSScheduler
from algorithms.sjf import SJFScheduler
from algorithms.round_robin import RoundRobinScheduler
from algorithms.eua import EUAScheduler

from visualization.gantt_plot import generate_gantt
from visualization.comparison_plot import generate_comparison_chart


ALGORITMOS = [
    "FCFS",
    "SJF",
    "ROUND_ROBIN",
    "PRIORIDADE",
    "EDF",
    "CFS",
    "EUA"
]


def get_scheduler(algoritmo, dados):

    algoritmo = algoritmo.upper()

    if algoritmo == "EDF":
        return EDFScheduler()

    elif algoritmo in ["PRIORITY", "PRIORIDADE"]:
        return PriorityScheduler()

    elif algoritmo == "CFS":
        return CFSScheduler()

    elif algoritmo == "FCFS":
        return FCFSScheduler()

    elif algoritmo == "SJF":
        return SJFScheduler()

    elif algoritmo in ["ROUND_ROBIN", "RR"]:
        return RoundRobinScheduler(
            quantum=dados.get("quantum", 2),
            sobrecarga=dados.get("sobrecarga", dados.get("sobrecarga_contexto", 1)
)
        )

    elif algoritmo == "EUA":
        return EUAScheduler(
            quantum=dados.get("quantum", 2),
            sobrecarga=dados.get("sobrecarga", dados.get("sobrecarga_contexto", 1))
        )

    else:
        raise ValueError("Algoritmo inválido")


def run_simulation(algoritmo, input_path, logger):

    dados, processos = load_processes(input_path)

    processos_execucao = processos.copy()

    scheduler = get_scheduler(algoritmo, dados)

    logger.info(f"Iniciando execução do algoritmo: {algoritmo.upper()}")

    resultado = scheduler.run(processos_execucao)

    metricas = calculate_metrics(
        resultado,
        processos,
        algoritmo
    )

    save_gantt(resultado, algoritmo)
    logger.info(f"Gantt JSON salvo em outputs/gantt/{algoritmo.lower()}_gantt.json")

    generate_gantt(resultado, algoritmo, processos)
    logger.info(f"Gantt PNG salvo em outputs/gantt/{algoritmo.lower()}_gantt.png")

    save_table(processos, algoritmo, resultado)
    logger.info(f"Tabela salva em outputs/tables/{algoritmo.lower()}_table.csv")

    save_metrics(metricas, algoritmo)
    logger.info(f"Métricas salvas em outputs/metrics/{algoritmo.lower()}_metrics.json")

    logger.info(f"Execução do algoritmo {algoritmo.upper()} concluída")

    metricas["algoritmo"] = algoritmo.upper()

    return metricas


def main():

    args = parse_args()

    create_output_dirs()

    logger = setup_logger()

    logger.info("Iniciando simulador")
    logger.info(f"Algoritmo selecionado: {args.alg.upper()}")
    logger.info(f"Arquivo de entrada: {args.input}")

    if args.alg.upper() == "ALL":

        resultados_comparacao = []

        for algoritmo in ALGORITMOS:

            metricas = run_simulation(
                algoritmo,
                args.input,
                logger
            )

            resultados_comparacao.append(metricas)

        save_comparison(resultados_comparacao)

        logger.info("Comparação salva em outputs/comparison/comparison.csv")

        generate_comparison_chart()

        logger.info("Gráfico de comparação salvo em outputs/comparison/comparison.png")

        logger.info("Execução de todos os algoritmos concluída com sucesso")

        return

    run_simulation(
        args.alg,
        args.input,
        logger
    )

    logger.info("Simulação concluída com sucesso")


if __name__ == "__main__":
    main()