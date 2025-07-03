import numpy as np
import cv2 as cv
import os

# Certifique-se de que o diretório existe
output_dir = os.path.expanduser('~/data_you/')
os.makedirs(output_dir, exist_ok=True)

# Inicializa as câmeras
capL = cv.VideoCapture(0)
capR = cv.VideoCapture(2)

# Verifica se ambas as câmeras foram abertas com sucesso
if not capL.isOpened():
    print("Não foi possível abrir a câmera esquerda (capL)")
    exit()

if not capR.isOpened():
    print("Não foi possível abrir a câmera direita (capR)")
    exit()

# Obtém as propriedades das câmeras (usa a da esquerda como base)
width = int(capL.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(capL.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = 20.0

while True:
    # Captura os frames de ambas as câmeras
    retL, frameL = capL.read()
    retR, frameR = capR.read()

    if not retL or not retR:
        print("Erro ao capturar frames. Encerrando...")
        break


    # Exibe os vídeos em janelas separadas
    cv.imshow('frameL', frameL)
    cv.imshow('frameR', frameR)

    # Sai com 'q'
    if cv.waitKey(1) == ord('q'):
        break

# Libera tudo
#capL.release()
#capR.release()
#cv.destroyAllWindows()

fourcc = cv.VideoWriter_fourcc(*'XVID')
outL = cv.VideoWriter('stereoL.avi', fourcc, fps, (width, height))
outR = cv.VideoWriter('stereoR.avi', fourcc, fps, (width, height))

while capL.isOpened():
    retL, frameL = capL.read()
    retR, frameR = capR.read()
    if not retL:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # write the flipped frame
    outL.write(frameL)
    outR.write(frameR)
    cv.imshow('frameL', frameL)
    cv.imshow('frameR', frameR)
    if cv.waitKey(1) == ord('q'):
        break

# Release everything if job is finished
capL.release()
capR.release()
outL.release()
outR.release()
cv.destroyAllWindows()
