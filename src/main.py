import json
import os

def main():
    print("Iniciando simulador...")
    
    # Testa a leitura do volume de inputs
    input_path = "inputs/caso1.json"
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            dados = json.load(f)
            print(f"JSON lido com sucesso! Semente configurada: {dados.get('seed')}")
            print(f"Total de processos carregados: {len(dados.get('processos', []))}")
    else:
        print("Erro: Arquivo input.json não encontrado.")

    # Testa a escrita no volume de outputs
    output_path = "outputs/teste_infra.txt"
    with open(output_path, 'w') as f:
        f.write("A infraestrutura do Docker está funcionando perfeitamente! Os volumes estão mapeados.")
    
    print("Arquivo de teste salvo na pasta outputs/.")

if __name__ == "__main__":
    main()