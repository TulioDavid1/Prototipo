Passo 1: Instalar o PyTorch com suporte à GPU (opcional)
Se você possui uma GPU compatível com CUDA, instale o PyTorch com suporte à GPU para acelerar o treinamento. Siga as instruções no site oficial:

Passo 2: Instalar o YOLOv8
Instale a biblioteca Ultralytics, que contém o YOLOv8, executando o comando abaixo no terminal:


pip install ultralytics

Passo 3: Rodar os Arquivos
Testar com Webcam
Para realizar detecções usando a webcam, execute:

python detectar_usando_webcam.py

Testar Capturando Tela
Para realizar detecções capturando uma parte da tela, execute:

python detectar_capturando_tela.py


Configuração adicional para captura de tela:

Ajuste o tamanho da área de captura no campo size.
Configure a posição inicial da captura no campo offset.