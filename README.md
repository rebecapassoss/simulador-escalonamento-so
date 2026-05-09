# Simulador de Escalonamento de Processos

Este repositório contém a implementação de um simulador de eventos discretos para algoritmos de escalonamento de processos, desenvolvido como trabalho da disciplina de Sistemas Operacionais (MATA58)

O objetivo principal é avaliar o impacto de sobrecargas de contexto, deadlines e prioridades no desempenho do sistema, incluindo uma análise simplificada do algoritmo CFS (Completely Fair Scheduler) do Linux.

## Algoritmos Implementados
1. **FIFO / FCFS** (Não preemptivo) 
2. **SJF** - Shortest Job First (Não preemptivo) 
3. **Round-Robin** (Preemptivo com quantum fixo) 
4. **Prioridades** (Preemptivo) 
5. **EDF** - Earliest Deadline First (Preemptivo) 
6. **CFS-Sim** - Completely Fair Scheduler Simplificado (Preemptivo, baseado em tempo virtual) 
7. **Autoral** - [Nome do algoritmo a ser definido] 

## Estrutura do Repositório

```text
simulador-escalonamento/
├── src/                # Código-fonte principal
│   ├── algorithms/     # Lógicas de escalonamento (FIFO, RR, CFS, etc.)
│   ├── models/         # Classes base (Processo, Motor de Eventos)
│   ├── visualization/  # Scripts para geração do Gráfico de Gantt
│   └── main.py         # Ponto de entrada (CLI)
├── inputs/             # Arquivos .json com os casos de teste
├── outputs/            # Imagens dos gráficos de Gantt e logs de saída
├── Dockerfile          # Configuração da imagem Docker
├── docker-compose.yml  # Orquestração do container
└── requirements.txt    # Dependências do Python (pandas, matplotlib)
```

## Como Executar (Recomendado via Docker)

Para garantir que o simulador rode da mesma forma em todas as máquinas sem problemas de dependências, utilize o Docker.

1. **Construa a imagem e suba o container:**
   ```bash
   docker compose build
   docker compose up -d
   ```

2. **Execute o simulador via terminal do container:**
   ```bash
   docker exec -it simulador_so python src/main.py --alg CFS-Sim --input inputs/caso1.json --gantt outputs/caso1.png
   ```
## Formato de Entrada (JSON)

Os casos de teste devem estar na pasta `inputs/` seguindo o formato abaixo:

docker compose up -d

```json
{
  "quantum": 2,
  "sobrecarga_contexto": 1,
  "seed": 42,
  "processos": [
    {
      "id": "P1",
      "chegada": 0,
      "execucao": 5,
      "deadline": 8,
      "prioridade": 2
    },
    {
      "id": "P2",
      "chegada": 1,
      "execucao": 4,
      "deadline": 12,
      "prioridade": 1
    }
  ]
}
```

## Saídas
O simulador gerará na pasta `outputs/`:
**Gráfico de Gantt (.png):** Visualização da execução, mostrando blocos de execução (verde), sobrecarga de contexto (vermelho) e estouro de deadline (cinza).
**Tabela de Métricas:** Resumo quantitativo contendo tempo de espera, turnaround, throughput e % de ociosidade da CPU.