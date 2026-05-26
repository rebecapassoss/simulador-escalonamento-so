import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulador de Escalonamento"
    )

    parser.add_argument(
        "--alg",
        required=True,
        help="Algoritmo: FCFS, RR, EDF, PRIORITY..."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Arquivo JSON de entrada"
    )

    parser.add_argument(
        "--output",
        default="outputs/",
        help="Pasta de saída"
    )

    return parser.parse_args()