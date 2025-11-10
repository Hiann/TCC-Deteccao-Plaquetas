import os
import glob

# Define o caminho para a pasta principal de labels
base_label_dir = 'Dataset/Labels'

# Encontra todos os arquivos .txt dentro de Train, Val, e Test
search_path = os.path.join(base_label_dir, '**', '*.txt')
all_txt_files = glob.glob(search_path, recursive=True)

if not all_txt_files:
    print(f"Nenhum arquivo .txt encontrado em {base_label_dir}.")
    print("Verifique se o caminho está correto.")
else:
    print(f"Encontrados {len(all_txt_files)} arquivos .txt para processar...")

total_linhas_removidas = 0
arquivos_modificados = 0

for file_path in all_txt_files:
    linhas_para_manter = []
    linhas_removidas_neste_arquivo = 0
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Se a linha NÃO começar com '2 ' (com espaço), nós a mantemos
                if not line.strip().startswith('2 '):
                    linhas_para_manter.append(line)
                else:
                    total_linhas_removidas += 1
                    linhas_removidas_neste_arquivo += 1

        # Se removemos alguma linha, reescrevemos o arquivo
        if linhas_removidas_neste_arquivo > 0:
            with open(file_path, 'w') as f:
                f.writelines(linhas_para_manter)
            arquivos_modificados += 1
            
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")

print("\n--- Limpeza Concluída ---")
print(f"Arquivos .txt modificados: {arquivos_modificados}")
print(f"Total de anotações (Hemaceas) removidas: {total_linhas_removidas}")
print("Seu dataset agora contém apenas as classes 0 e 1.")