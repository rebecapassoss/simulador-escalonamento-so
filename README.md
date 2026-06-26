# Simulador de Escalonamento de Processos

Este repositório contém a implementação de um simulador de escalonamento de processos desenvolvido como trabalho da disciplina de Sistemas Operacionais (MATA58).

O objetivo do projeto é comparar diferentes algoritmos de escalonamento a partir de métricas quantitativas, gráficos de Gantt e análise de desempenho. O simulador permite avaliar fatores como deadlines, prioridades, preempções, trocas de contexto, sobrecarga e utilização da CPU.

## Algoritmos Implementados

1. **FCFS** - First Come, First Served
   Algoritmo não preemptivo que executa os processos na ordem de chegada.

2. **SJF** - Shortest Job First
   Algoritmo não preemptivo que escolhe o processo com menor tempo de execução entre os processos prontos.

3. **Round Robin**
   Algoritmo preemptivo com quantum fixo e custo de sobrecarga de contexto.

4. **Prioridade**
   Algoritmo preemptivo que escolhe o processo com maior prioridade. Neste projeto, valores menores indicam maior prioridade.

5. **EDF** - Earliest Deadline First
   Algoritmo preemptivo que escolhe o processo com menor deadline.

6. **CFS** - Completely Fair Scheduler Simplificado
   Algoritmo inspirado no escalonador do Linux, utilizando uma versão simplificada baseada em `vruntime`.

7. **EUA** - Escalonamento por Urgência Acumulada
   Algoritmo autoral em que cada processo acumula urgência enquanto espera na fila. O processo com maior urgência é escolhido para execução, e a urgência é reiniciada após sua execução por uma fatia de tempo.

## Estrutura do Repositório

```text
Simulador-de-Escalonamento/
├── inputs/                 # Arquivos JSON com casos de teste
├── outputs/                # Arquivos gerados pelo simulador
│   ├── comparison/         # CSV e gráficos comparativos
│   ├── gantt/              # Gantt em JSON e PNG
│   ├── logs/               # Logs da execução
│   ├── metrics/            # Métricas em JSON
│   └── tables/             # Tabelas em CSV
├── src/
│   ├── algorithms/         # Implementação dos algoritmos
│   ├── models/             # Modelo de processo
│   ├── utils/              # Parser, loader, logger, métricas e exportações
│   ├── visualization/      # Geração de gráficos
│   └── main.py             # Ponto de entrada do simulador
├── tests/                  # Testes do projeto
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Como Executar

A execução recomendada é via Docker.

### Rodar com Docker Compose

```bash
docker compose up --build
```

O comportamento padrão depende do comando configurado no `docker-compose.yml`.

Exemplo de configuração para rodar todos os algoritmos:

```yaml
services:
  simulador:
    build: .
    container_name: simulador_so

    volumes:
      - ./src:/app/src
      - ./inputs:/app/inputs
      - ./outputs:/app/outputs

    command: >
      --alg ALL
      --input inputs/caso1.json
```

### Rodar um algoritmo específico

Também é possível executar diretamente com `docker compose run`:

```bash
docker compose run --rm simulador --alg EDF --input inputs/caso1.json
```

Exemplos:

```bash
docker compose run --rm simulador --alg FCFS --input inputs/caso1.json
docker compose run --rm simulador --alg SJF --input inputs/caso1.json
docker compose run --rm simulador --alg ROUND_ROBIN --input inputs/caso1.json
docker compose run --rm simulador --alg PRIORIDADE --input inputs/caso1.json
docker compose run --rm simulador --alg EDF --input inputs/caso1.json
docker compose run --rm simulador --alg CFS --input inputs/caso1.json
docker compose run --rm simulador --alg EUA --input inputs/caso1.json
```

### Rodar todos os algoritmos

```bash
docker compose run --rm simulador --alg ALL --input inputs/caso1.json
```

O modo `ALL` executa todos os algoritmos implementados e gera os arquivos de saída individuais e comparativos.

## Formato de Entrada

Os casos de teste devem estar na pasta `inputs/` em formato JSON.

Exemplo:

```json
{
  "seed": 42,
  "quantum": 2,
  "sobrecarga": 1,
  "processos": [
    {
      "id": "P1",
      "chegada": 0,
      "execucao": 5,
      "prioridade": 2,
      "deadline": 8
    },
    {
      "id": "P2",
      "chegada": 1,
      "execucao": 4,
      "prioridade": 1,
      "deadline": 12
    }
  ]
}
```

### Campos

* `id`: identificador do processo.
* `chegada`: instante em que o processo chega ao sistema.
* `execucao`: tempo total necessário de CPU.
* `prioridade`: prioridade do processo. Valores maiores indicam maior prioridade.
* `deadline`: prazo máximo desejado para conclusão.
* `quantum`: fatia de tempo usada por algoritmos como Round Robin e EUA.
* `sobrecarga`: custo de troca de contexto.

## Saídas Geradas

O simulador gera arquivos automaticamente dentro de `outputs/`.

### Gantt

```text
outputs/gantt/<algoritmo>_gantt.json
outputs/gantt/<algoritmo>_gantt.png
```

O JSON contém a sequência de execução no tempo.
O PNG contém a visualização gráfica do escalonamento.

### Métricas

```text
outputs/metrics/<algoritmo>_metrics.json
```

Exemplo:

```json
{
  "tempo_total": 11,
  "throughput": 0.2727,
  "tempo_ocioso": 0,
  "tempo_sobrecarga": 0,
  "utilizacao_cpu": 100.0,
  "utilizacao_cpu_real": 100.0,
  "trocas_contexto": 4,
  "preempcoes": 2,
  "turnaround_medio": 5.0,
  "waiting_time_medio": 1.33,
  "response_time_medio": 0.0,
  "deadline_miss": 0,
  "deadline_miss_rate": 0.0
}
```

### Tabelas

```text
outputs/tables/<algoritmo>_table.csv
```

Contém os dados dos processos utilizados na simulação.

### Comparação entre algoritmos

Ao executar com `--alg ALL`, são gerados:

```text
outputs/comparison/comparison.csv
outputs/comparison/comparison_tempos.png
outputs/comparison/comparison_deadlines.png
outputs/comparison/comparison_cpu.png
```

Esses arquivos consolidam as métricas dos algoritmos e geram gráficos comparativos.

### Logs

```text
outputs/logs/simulator.log
```

Contém registros da execução, incluindo algoritmo selecionado, arquivo de entrada, arquivos gerados e conclusão da simulação.

## Métricas Calculadas

O simulador calcula:

* `tempo_total`: duração total da simulação.
* `throughput`: quantidade de processos concluídos por unidade de tempo.
* `tempo_ocioso`: tempo em que a CPU ficou sem processo para executar.
* `tempo_sobrecarga`: tempo gasto com troca de contexto.
* `utilizacao_cpu`: percentual de tempo em que a CPU não ficou ociosa.
* `utilizacao_cpu_real`: percentual de tempo útil, descontando ociosidade e sobrecarga.
* `trocas_contexto`: quantidade de mudanças entre processos executados.
* `preempcoes`: quantidade de interrupções reais, quando um processo perde a CPU antes de terminar.
* `turnaround_medio`: média do tempo entre chegada e término dos processos.
* `waiting_time_medio`: média do tempo total de espera dos processos.
* `response_time_medio`: média do tempo até cada processo receber CPU pela primeira vez.
* `deadline_miss`: quantidade de processos que terminaram após o deadline.
* `deadline_miss_rate`: percentual de processos que perderam o deadline.

## Casos de Teste

Alguns casos utilizados para validação:

```text
inputs/caso1.json
inputs/caso_preempcao.json
inputs/caso_ocioso.json
inputs/caso_deadline.json
inputs/caso_sobrecarga.json
```

Cada caso foi criado para validar aspectos diferentes do simulador:

* `caso1.json`: execução básica.
* `caso_preempcao.json`: preempções e deadlines.
* `caso_ocioso.json`: tempo ocioso da CPU.
* `caso_deadline.json`: perda de deadlines.
* `caso_sobrecarga.json`: impacto da sobrecarga em Round Robin e EUA.

## Limpar Arquivos Gerados

Para remover JSONs, PNGs, CSVs e logs gerados em `outputs/`:

```bash
find outputs -type f \( -name "*.json" -o -name "*.png" -o -name "*.csv" -o -name "*.log" \) -delete
```

## Interface Web com Streamlit

Além da execução via terminal, o projeto possui uma interface web simples feita com Streamlit.

Para executar:

```bash
make front
```


## Dependências

As dependências Python estão listadas em:

```text
requirements.txt
```

Principais bibliotecas utilizadas:

* `matplotlib`
* bibliotecas padrão do Python, como `json`, `csv`, `logging`, `argparse` e `os`


## Observações

* A implementação do CFS é uma versão simplificada e didática, baseada em `vruntime`.
* O algoritmo EUA é autoral e usa urgência acumulada para tentar reduzir injustiças causadas por espera prolongada.
* O simulador é baseado em execução discreta por unidade de tempo.
* Os algoritmos podem produzir resultados diferentes dependendo de chegada, execução, prioridade, deadline, quantum e sobrecarga.
