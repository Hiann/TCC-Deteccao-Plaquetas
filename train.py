from ultralytics import YOLO

# MUDANÇA AQUI: Voltamos para o 'yolov8n.pt'
# Esta é a versão estável, principal e 100% garantida
# que a biblioteca 'ultralytics' sabe como baixar.
model = YOLO('yolov8n.pt')

# Inicia o treinamento do modelo
print("Iniciando treinamento com o dataset de 2 classes (Plaquetas) 80/20...")
print("Usando a arquitetura estável: YOLOv8")

results = model.train(
    data='plaquetas.yaml',   
    epochs=300,              
    imgsz=640,               
    batch=8,                 
    name='treino_plaquetas_YOLOv8_final',
    
    patience=100 
)

print("-----------------------------------")
print("Treinamento com YOLOv8 concluído com sucesso!")
print("Seu novo modelo está salvo na pasta 'runs/detect/treino_plaquetas_YOLOv8_final'")
print("-----------------------------------")