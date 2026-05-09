# Simulador de Escalonamento de Processos

[cite_start]Este repositório contém a implementação de um simulador de eventos discretos para algoritmos de escalonamento de processos, desenvolvido como trabalho da disciplina de Sistemas Operacionais[cite: 1, 3].

[cite_start]O objetivo principal é avaliar o impacto de sobrecargas de contexto, deadlines e prioridades no desempenho do sistema [cite: 4][cite_start], incluindo uma análise simplificada do algoritmo CFS (Completely Fair Scheduler) do Linux[cite: 5, 14].

## 👥 Equipe
* [Seu Nome] - Infraestrutura e Motor de Simulação
* [Nome do Colega 2] - Algoritmos Clássicos
* [Nome do Colega 3] - CFS-Sim e Algoritmo Autoral
* [Nome do Colega 4] - Visualização de Dados e Relatório

## 🚀 Algoritmos Implementados
1. [cite_start]**FIFO / FCFS** (Não preemptivo) [cite: 9]
2. [cite_start]**SJF** - Shortest Job First (Não preemptivo) [cite: 10]
3. [cite_start]**Round-Robin** (Preemptivo com quantum fixo) [cite: 11]
4. [cite_start]**Prioridades** (Preemptivo) [cite: 12]
5. [cite_start]**EDF** - Earliest Deadline First (Preemptivo) [cite: 13]
6. [cite_start]**CFS-Sim** - Completely Fair Scheduler Simplificado (Preemptivo, baseado em tempo virtual) [cite: 14, 59-63]
7. [cite_start]**Autoral** - [Nome do algoritmo a ser definido] [cite: 15]

## 📁 Estrutura do Repositório

\`\`\`text
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
\`\`\`

## 🛠️ Como Executar (Recomendado via Docker)

Para garantir que o simulador rode da mesma forma em todas as máquinas sem problemas de dependências, utilize o Docker.

1. **Construa a imagem e suba o container:**
   \`\`\`bash
   docker-compose build
   docker-compose up -d
   \`\`\`

2. **Execute o simulador via terminal do container:**
   \`\`\`bash
   docker exec -it simulador_so python src/main.py --alg CFS-Sim --input inputs/caso1.json --gantt outputs/caso1.png
   \`\`\`

## ⚙️ Formato de Entrada (JSON)

[cite_start]Os casos de teste devem estar na pasta `inputs/` seguindo o formato abaixo [cite: 89-99]:

\`\`\`json
{
  "quantum": 2,
  "sobrecarga_contexto": 1,
  "seed": 42,
  "processos": [
    {"id": "P1", "chegada": 0, "execucao": 5, "deadline": 8, "prioridade": 2},
    {"id": "P2", "chegada": 1, "execucao": 4, "deadline": 12, "prioridade": 1}
  ]
}
\`\`\`

## 📊 Saídas
O simulador gerará na pasta `outputs/`:
* [cite_start]**Gráfico de Gantt (.png):** Visualização da execução, mostrando blocos de execução (verde), sobrecarga de contexto (vermelho) e estouro de deadline (cinza) [cite: 48-53].
* [cite_start]**Tabela de Métricas:** Resumo quantitativo contendo tempo de espera, turnaround, throughput e % de ociosidade da CPU [cite: 56-57].