from ultralytics import YOLO
import cv2
from windowcapture import WindowCapture
from collections import defaultdict
import numpy as np

# Configurações para captura de janela
offset_x = 400  # Offset horizontal
offset_y = 300  # Offset vertical
tamanho_janela = (800, 600)  # Tamanho da janela capturada
captura_janela = WindowCapture(size=tamanho_janela, origin=(offset_x, offset_y))

# Carrega o modelo YOLO pré-treinado (você pode trocar pelo modelo customizado)
modelo = YOLO("yolov8n.pt")
# Para usar um modelo treinado com dados personalizados, substitua pela linha abaixo:
# modelo = YOLO("runs/detect/train4/weights/best.pt")

# Histórico de rastreamento de objetos
historico_rastreamento = defaultdict(lambda: [])
rastrear_objetos = True
mostrar_rastro = True

while True:
    # Captura a imagem da tela
    imagem = captura_janela.get_screenshot()

    # Realiza a detecção ou rastreamento usando o modelo
    if rastrear_objetos:
        resultados = modelo.track(imagem, persist=True)
    else:
        resultados = modelo(imagem)

    # Processa os resultados
    for resultado in resultados:
        # Desenha os resultados na imagem
        imagem = resultado.plot()

        if rastrear_objetos and mostrar_rastro:
            try:
                # Obtém as caixas delimitadoras e IDs de rastreamento
                caixas = resultado.boxes.xywh.cpu()
                ids_rastreamento = resultado.boxes.id.int().cpu().tolist()

                # Desenha o histórico de rastreamento
                for caixa, id_rastreamento in zip(caixas, ids_rastreamento):
                    x, y, largura, altura = caixa
                    historico = historico_rastreamento[id_rastreamento]
                    historico.append((float(x), float(y)))  # Ponto central (x, y)
                    if len(historico) > 30:  # Mantém até 30 quadros no histórico
                        historico.pop(0)

                    # Desenha as linhas de rastreamento
                    pontos = np.hstack(historico).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(imagem, [pontos], isClosed=False, color=(230, 0, 0), thickness=5)
            except Exception as e:
                print(f"Erro no rastreamento: {e}")
                pass

    # Exibe a imagem processada
    cv2.imshow("Tela", imagem)

    # Fecha o programa ao pressionar a tecla 'q'
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

cv2.destroyAllWindows()
print("Programa finalizado.")
