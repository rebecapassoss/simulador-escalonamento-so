import os

from utils.parser import parse_args
from utils.loader import load_processes
from utils.logger import setup_logger
from utils.directories import create_output_dirs
from utils.save_results import save_gantt

from algorithms.edf import EDFScheduler
from algorithms.prioridade import PriorityScheduler
from algorithms.cfs import CFSScheduler




def main():

    # CLI
    args = parse_args()

    # Logger
    logger = setup_logger()

    logger.info("Iniciando simulador")

    create_output_dirs()

    # Carrega JSON
    dados, processos = load_processes(args.input)

    logger.info(f"{len(processos)} processos carregados")

    # Seleção do algoritmo
    if args.alg.upper() == "EDF":

        scheduler = EDFScheduler()

    elif args.alg.upper() == "PRIORITY":

        scheduler = PriorityScheduler()
        
    elif args.alg.upper() == "CFS":

        scheduler = CFSScheduler()

    else:
        raise ValueError("Algoritmo inválido")

    # Executa
    resultado = scheduler.run(processos)

    logger.info("Simulação concluída")

    save_gantt(resultado, args.alg)

    print("Resultado salvo com sucesso")


if __name__ == "__main__":
    main()