from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np

# Configuração da captura de vídeo
# Pode ser câmera local, vídeo ou stream online
camera = cv2.VideoCapture(0)  # Captura da câmera padrão
# Para utilizar outra câmera, descomente a linha abaixo:
# camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Carrega o modelo YOLO pré-treinado (pode ser alterado para um modelo customizado)
modelo = YOLO("yolov8n.pt")
# Para usar um modelo customizado, substitua pela linha abaixo:
# modelo = YOLO("caminho_para_o_modelo_treinado.pt")

# Configuração de rastreamento
historico_rastreamento = defaultdict(lambda: [])
rastrear_objetos = True
mostrar_rastro = True

while True:
    sucesso, imagem = camera.read()  # Captura a imagem da câmera

    if sucesso:
        # Realiza a detecção ou rastreamento
        if rastrear_objetos:
            resultados = modelo.track(imagem, persist=True)
        else:
            resultados = modelo(imagem)

        # Processa os resultados da detecção
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

        # Exibe a imagem com as detecções
        cv2.imshow("Detecção", imagem)

    # Finaliza o programa ao pressionar a tecla 'q'
    tecla = cv2.waitKey(1)
    if tecla == ord('q'):
        break

# Libera a câmera e fecha as janelas
camera.release()
cv2.destroyAllWindows()
print("Programa finalizado.")
