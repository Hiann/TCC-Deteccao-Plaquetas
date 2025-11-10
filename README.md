# TCC: Detecção de Anaplasma em Plaquetas com YOLOv8

Este projeto é um Trabalho de Conclusão de Curso (TCC) focado na criação de um modelo de visão computacional para detectar plaquetas doentes (infectadas com Anaplasma) e saudáveis em imagens de microscopia.

## 🛠️ Tecnologias Utilizadas
* Python
* YOLOv8 (Ultralytics)
* OpenCV
* SQLite3

## 🚀 Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Hiann/TCC-Deteccao-Plaquetas.git]
    cd TCC-Deteccao-Plaquetas
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Para Treinar um Novo Modelo:**
    (Certifique-se que seu dataset está nas pastas `dataset/`)
    ```bash
    python train.py
    ```

5.  **Para Executar a Predição (Análise):**
    (O script analisará automaticamente as imagens da pasta `dataset/images/val/`)
    ```bash
    python predict_with_db.py
    ```

## 📊 Resultados
O modelo treinado (YOLOv8n com 300 épocas) atingiu X% de mAP50 no conjunto de validação. Os resultados de cada análise são salvos no banco de dados `resultados_analises.db`.