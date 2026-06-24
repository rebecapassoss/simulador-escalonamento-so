import os
import copy

from utils.export_table import save_table
from utils.parser import parse_args
from utils.loader import load_processes
from utils.logger import setup_logger
from utils.directories import create_output_dirs
from utils.save_results import save_gantt, save_metrics
from utils.metrics import calculate_metrics

from algorithms.edf import EDFScheduler
from algorithms.prioridade import PriorityScheduler
from algorithms.cfs import CFSScheduler
from algorithms.fcfs import FCFSScheduler
from algorithms.sjf  import SJFScheduler
from algorithms.round_robin import RoundRobinScheduler




def main():

    # CLI
    args = parse_args()

    # Logger
    logger = setup_logger()

    logger.info("Iniciando simulador")

    create_output_dirs()

    # Carrega JSON
    dados, processos = load_processes(args.input)

    processos_execucao = processos.copy()

    processos_metricas = processos.copy()

    logger.info(f"{len(processos)} processos carregados")

    # Seleção do algoritmo
    if args.alg.upper() == "EDF":

        scheduler = EDFScheduler()

    elif args.alg.upper() == "PRIORITY":

        scheduler = PriorityScheduler()
        
    elif args.alg.upper() == "CFS":

        scheduler = CFSScheduler()
        
    elif args.alg.upper() == "FCFS":

        scheduler = FCFSScheduler()

    elif args.alg.upper() == "SJF":

        scheduler = SJFScheduler()

    elif args.alg.upper() == "ROUND_ROBIN":

        scheduler = RoundRobinScheduler(
            quantum=dados.get("quantum", 2),
            sobrecarga=dados.get("sobrecarga", 1)
        )

    else:
        raise ValueError("Algoritmo inválido")

    # Executa
    resultado = scheduler.run(processos_execucao)


    logger.info("Simulação concluída")

    save_gantt(resultado, args.alg)

    logger.info("Resultado salvo com sucesso")

    save_table(processos, args.alg)

    logger.info(f"Resultado salvo em outputs/tables/{args.alg.lower()}_table.csv")

   

    metricas = calculate_metrics(
       resultado,
       processos_metricas
)   
    save_metrics(metricas, args.alg)

if __name__ == "__main__":
    main()