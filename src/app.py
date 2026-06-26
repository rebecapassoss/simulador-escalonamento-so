import json
import os
import subprocess
import csv

import streamlit as st


ALGORITMOS = [
    "ALL",
    "FCFS",
    "SJF",
    "ROUND_ROBIN",
    "PRIORIDADE",
    "EDF",
    "CFS",
    "EUA"
]


def listar_inputs():

    if not os.path.exists("inputs"):
        return []

    arquivos = [
        arquivo
        for arquivo in os.listdir("inputs")
        if arquivo.endswith(".json")
    ]

    return sorted(arquivos)


def carregar_json(path):

    with open(path, "r") as f:
        return json.load(f)


def executar_simulador(algoritmo, input_path):

    comando = [
        "python",
        "src/main.py",
        "--alg",
        algoritmo,
        "--input",
        input_path
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True
    )

    return resultado


def mostrar_metricas_individuais(algoritmo):

    path = f"outputs/metrics/{algoritmo.lower()}_metrics.json"

    if os.path.exists(path):

        metricas = carregar_json(path)

        st.subheader("Métricas")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Tempo total",
            metricas.get("tempo_total")
        )

        col1.metric(
            "Throughput",
            metricas.get("throughput")
        )

        col2.metric(
            "Turnaround médio",
            metricas.get("turnaround_medio")
        )

        col2.metric(
            "Waiting time médio",
            metricas.get("waiting_time_medio")
        )

        col3.metric(
            "Response time médio",
            metricas.get("response_time_medio")
        )

        col3.metric(
            "Deadline miss rate",
            f'{metricas.get("deadline_miss_rate")}%'
        )

        with st.expander("Ver JSON completo das métricas"):
            st.json(metricas)

    else:
        st.warning("Arquivo de métricas não encontrado.")


def mostrar_gantt(algoritmo):

    path_png = f"outputs/gantt/{algoritmo.lower()}_gantt.png"
    path_json = f"outputs/gantt/{algoritmo.lower()}_gantt.json"

    if os.path.exists(path_png):

        st.subheader("Diagrama de Gantt")
        st.image(path_png)

    else:
        st.warning("Imagem do Gantt não encontrada.")

    if os.path.exists(path_json):

        with st.expander("Ver Gantt em JSON"):
            gantt = carregar_json(path_json)
            st.json(gantt)


def carregar_csv(path):

    with open(path, "r") as f:

        reader = csv.DictReader(f)

        return list(reader)
    

def carregar_texto(path):

    with open(path, "r") as f:

        return f.read()
    

def mostrar_comparacao():

    st.subheader("Comparação entre algoritmos")

    path_csv = "outputs/comparison/comparison.csv"

    if os.path.exists(path_csv):

        dados = carregar_csv(path_csv)

        st.dataframe(
            dados,
            use_container_width=True
        )

    else:

        st.warning("comparison.csv não encontrado.")

    graficos = [
        (
            "Comparação de tempos médios",
            "outputs/comparison/comparison_tempos.png"
        ),
        (
            "Taxa de perda de deadline",
            "outputs/comparison/comparison_deadlines.png"
        ),
        (
            "CPU e sobrecarga",
            "outputs/comparison/comparison_cpu.png"
        )
    ]

    for titulo, path in graficos:

        if os.path.exists(path):

            st.markdown(f"### {titulo}")

            st.image(path)

def mostrar_tabela_processos(algoritmo):

    path = f"outputs/tables/{algoritmo.lower()}_table.csv"

    st.subheader("Tabela final dos processos")

    if os.path.exists(path):

        dados = carregar_csv(path)

        st.dataframe(
            dados,
            use_container_width=True
        )

        with open(path, "rb") as f:
            st.download_button(
                label="Baixar tabela CSV",
                data=f,
                file_name=f"{algoritmo.lower()}_table.csv",
                mime="text/csv"
            )

    else:

        st.warning("Tabela CSV não encontrada.")


def mostrar_logs():

    path = "outputs/logs/simulator.log"

    st.subheader("Logs da execução")

    if os.path.exists(path):

        conteudo = carregar_texto(path)

        st.code(
            conteudo,
            language="text"
        )

        with open(path, "rb") as f:
            st.download_button(
                label="Baixar logs",
                data=f,
                file_name="simulator.log",
                mime="text/plain"
            )

    else:

        st.warning("Arquivo de log não encontrado.")

def main():

    st.set_page_config(
        page_title="Simulador de Escalonamento",
        layout="wide"
    )

    st.title("Simulador de Escalonamento de Processos")

    st.markdown(
        """
        Interface simples para executar os algoritmos de escalonamento,
        visualizar métricas, diagramas de Gantt e comparações.
        """
    )

    st.sidebar.header("Configuração")

    inputs = listar_inputs()

    if not inputs:
        st.error("Nenhum arquivo JSON encontrado em inputs/.")
        return

    arquivo_input = st.sidebar.selectbox(
        "Caso de teste",
        inputs
    )

    algoritmo = st.sidebar.selectbox(
        "Algoritmo",
        ALGORITMOS
    )

    input_path = f"inputs/{arquivo_input}"

    with st.expander("Ver entrada JSON"):
        entrada = carregar_json(input_path)
        st.json(entrada)

    if st.sidebar.button("Executar simulação"):

        with st.spinner("Executando simulador..."):

            resultado = executar_simulador(
                algoritmo,
                input_path
            )

        if resultado.returncode != 0:

            st.error("Erro ao executar o simulador.")

            st.code(resultado.stderr)

            return

        st.success("Simulação executada com sucesso.")

        if resultado.stdout:
            with st.expander("Saída do terminal"):
                st.code(resultado.stdout)

    st.divider()

    if algoritmo == "ALL":

        mostrar_comparacao()

        mostrar_logs()

    else:

        mostrar_metricas_individuais(algoritmo)
        mostrar_gantt(algoritmo)
        mostrar_tabela_processos(algoritmo)
        mostrar_logs()
        


if __name__ == "__main__":
    main()