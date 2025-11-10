import sqlite3
import cv2
from ultralytics import YOLO
from datetime import datetime
import os

# --- Funções do Banco de Dados (NÃO MUDAM) ---
def setup_database():
    """Cria o banco de dados e a tabela ATUALIZADA para 2 classes."""
    conn = sqlite3.connect('resultados_analises.db') 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            nome_imagem TEXT NOT NULL,
            plaquetas_saudaveis_contagem INTEGER,
            plaquetas_doentes_contagem INTEGER,
            total_plaquetas INTEGER,
            proporcao_doentes REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("Banco de dados 'resultados_analises.db' configurado.")

def salvar_resultado(nome_imagem, contagens):
    """Salva o resultado de uma análise no banco de dados ATUALIZADO."""
    conn = sqlite3.connect('resultados_analises.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    p_saudaveis = contagens.get('Plaquetas_saudaveis', 0)
    p_doentes = contagens.get('Plaquetas_doentes', 0)
    
    total_plaquetas = p_saudaveis + p_doentes
    proporcao_doentes = 0.0
    if total_plaquetas > 0:
        proporcao_doentes = (p_doentes / total_plaquetas) * 100 

    cursor.execute('''
        INSERT INTO analises (timestamp, nome_imagem, plaquetas_saudaveis_contagem, plaquetas_doentes_contagem, total_plaquetas, proporcao_doentes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, nome_imagem, p_saudaveis, p_doentes, total_plaquetas, proporcao_doentes))

    conn.commit()
    conn.close()
    print(f"-> Resultado da imagem '{nome_imagem}' salvo no banco de dados.")

# --- Seção de Análise (NVÃO MUDA) ---
def analisar_pasta_e_salvar(caminho_modelo, caminho_pasta):
    """Carrega o modelo, faz a análise em LOTE e salva os resultados."""
    
    print(f"Carregando modelo de: {caminho_modelo}")
    model = YOLO(caminho_modelo)
    
    if not os.path.exists('resultados_predicao'):
        os.makedirs('resultados_predicao')
        print("Pasta 'resultados_predicao' criada.")

    print(f"Iniciando análise em lote na pasta: {caminho_pasta}")
    
    # Se os resultados não aparecerem, adicione o filtro 'conf='
    # Ex: results_list = model(caminho_pasta, stream=True, conf=0.1) 
    results_list = model(caminho_pasta, stream=True) 
    
    total_imagens = 0
    for result in results_list:
        total_imagens += 1
        nome_arquivo = os.path.basename(result.path)
        
        contagem_classes = {
            'Plaquetas_saudaveis': 0,
            'Plaquetas_doentes': 0
        }
        
        nomes_classes = result.names 
        for c in result.boxes.cls:
            id_classe = int(c)
            nome_classe = nomes_classes[id_classe]
            if nome_classe in contagem_classes:
                contagem_classes[nome_classe] += 1

        print("---------------------------------")
        print(f"Analisando Imagem: {nome_arquivo}")
        print(f"Plaquetas Saudáveis: {contagem_classes['Plaquetas_saudaveis']}")
        print(f"Plaquetas Doentes (Anaplasma): {contagem_classes['Plaquetas_doentes']}")

        salvar_resultado(nome_arquivo, contagem_classes)

        imagem_com_caixas = result.plot()
        caminho_saida_img = f'resultados_predicao/analise_{nome_arquivo}'
        cv2.imwrite(caminho_saida_img, imagem_com_caixas)
        
    print("\n--- Análise em lote concluída ---")
    print(f"Total de {total_imagens} imagens analisadas.")


# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    
    # MUDANÇA AQUI: O caminho agora aponta para a nova pasta do YOLOv8
    caminho_do_modelo = 'runs/detect/treino_plaquetas_YOLOv8_final/weights/best.pt'

    # O caminho da pasta de validação não muda
    caminho_da_pasta_para_analisar = 'dataset/images/val' 

    # Executa o processo
    print("Iniciando processo de análise em lote...")
    setup_database() 
    analisar_pasta_e_salvar(caminho_do_modelo, caminho_da_pasta_para_analisar)
    print("Processo finalizado.")