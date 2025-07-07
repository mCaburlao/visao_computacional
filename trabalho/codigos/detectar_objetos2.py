import cv2
import numpy as np

cam = cv2.VideoCapture(0)

zona_x, zona_y, zona_largura, zona_altura = 150, 100, 300, 300

# Limites padrão (serão atualizados na calibração)
AREA_MIN = 2000
AREA_MAX = 40000

modo_calibrado = False  # Flag para indicar que a calibração foi feita

print("[INFO] Pressione 'c' para calibrar automaticamente com o objeto visível.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Desenhar área de leitura
    cv2.rectangle(frame, (zona_x, zona_y), 
                  (zona_x + zona_largura, zona_y + zona_altura), 
                  (255, 0, 0), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objeto_reconhecido = False

    for cnt in contours:
        if objeto_reconhecido:
            break

        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        perimetro = cv2.arcLength(cnt, True)

        if not (zona_x < x < zona_x + zona_largura and zona_y < y < zona_y + zona_altura):
            continue
        if area < AREA_MIN or area > AREA_MAX:
            continue

        approx = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
        lados = len(approx)

        forma = None
        if lados == 3:
            forma = "Triângulo"
        elif lados == 4:
            razao = w / float(h)
            if 0.9 <= razao <= 1.1:
                forma = "Quadrado"
            else:
                forma = "Retângulo"
        elif lados > 7:
            circularidade = (4 * np.pi * area) / (perimetro ** 2)
            if circularidade > 0.7:
                forma = "Círculo"

        if forma:
            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
            cv2.putText(frame, forma, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            objeto_reconhecido = True

    # Mostrar modo calibrado na tela
    if modo_calibrado:
        cv2.putText(frame, "CALIBRADO", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Detector com Calibracao Automatica", frame)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('q'):
        break

    elif tecla == ord('c'):
        print("[INFO] Calibrando com base no objeto atual...")

        # Captura novamente a imagem para calibrar
        ret, frame_calib = cam.read()
        if not ret:
            continue

        frame_calib = cv2.flip(frame_calib, 1)
        gray_calib = cv2.cvtColor(frame_calib, cv2.COLOR_BGR2GRAY)
        gray_calib = cv2.GaussianBlur(gray_calib, (5, 5), 0)
        edges_calib = cv2.Canny(gray_calib, 50, 150)

        contours_calib, _ = cv2.findContours(edges_calib, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Encontra maior contorno dentro da zona
        melhor_area = None

        for cnt in contours_calib:
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)

            if zona_x < x < zona_x + zona_largura and zona_y < y < zona_y + zona_altura:
                melhor_area = area
                break

        if melhor_area:
            AREA_MIN = int(melhor_area * 0.6)
            AREA_MAX = int(melhor_area * 1.6)
            modo_calibrado = True
            print(f"[INFO] Calibrado! AREA_MIN={AREA_MIN}, AREA_MAX={AREA_MAX}")
        else:
            print("[AVISO] Nenhum objeto detectado na zona azul!")

cam.release()
cv2.destroyAllWindows()
