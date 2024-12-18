from ultralytics import YOLO


def main():
    # Carregar um modelo
    #model = YOLO("yolov8n.yaml")  # criar um novo modelo do zero
    modelo = YOLO("yolov8n.pt")  # carregar um modelo pré-treinado 

    # Usar o modelo
    modelo.train(data="among.yaml", epochs=30, device=0)  # treinar o modelo
    metricas = modelo.val()  # avaliar o desempenho do modelo no conjunto de validação
    
if __name__ == '__main__':
    # freeze_support()
    main()
