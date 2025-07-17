import cv2
import numpy as np

# === Carrega a imagem de referência ===
ref_img = cv2.imread('top_0.png', cv2.IMREAD_GRAYSCALE)
if ref_img is None:
    raise ValueError("Não foi possível carregar a imagem de referência!")

# Inicializa o detector SIFT
sift = cv2.SIFT_create()

# Detecta keypoints e descritores da imagem de referência
kp_ref, des_ref = sift.detectAndCompute(ref_img, None)

# Cria o matcher FLANN
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Inicializa as webcams
cam1 = cv2.VideoCapture(0)  # Primeira câmera
cam2 = cv2.VideoCapture(2)  # Segunda câmera

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1 or not ret2:
        print("Erro ao capturar imagens das webcams!")
        break

    # Converte os frames para escala de cinza
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Detecta keypoints e descritores das câmeras
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # Define função para encontrar matches e desenhar resultados
    def match_and_draw(des_cam, kp_cam, frame_cam, window_name):
        matches = flann.knnMatch(des_ref, des_cam, k=2)

        # Aplica o teste de Lowe
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        result = frame_cam.copy()

        if len(good) > 10:
            src_pts = np.float32([kp_ref[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_cam[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            # Calcula homografia
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            # Desenha o polígono ao redor do objeto encontrado
            h, w = ref_img.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            result = cv2.polylines(result, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
        else:
            matchesMask = None

        # Desenha os matches
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matchesMask,
                           flags=2)
        img_matches = cv2.drawMatches(ref_img, kp_ref, frame_cam, kp_cam, good, None, **draw_params)

        cv2.imshow(window_name, img_matches)

    # Faz matching e desenha resultados para cada câmera
    match_and_draw(des1, kp1, frame1, "Camera 1 - Matching")
    match_and_draw(des2, kp2, frame2, "Camera 2 - Matching")

    # Função para obter matches e imagem desenhada
    def get_matches_img(des_cam, kp_cam, frame_cam, matchColor):
        matches = flann.knnMatch(des_ref, des_cam, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        matchesMask = None
        if len(good) > 10:
            src_pts = np.float32([kp_ref[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_cam[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            # Desenha o polígono ao redor do objeto encontrado
            h, w = ref_img.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            frame_cam = cv2.polylines(frame_cam, [np.int32(dst)], True, matchColor, 3, cv2.LINE_AA)
        else:
            matchesMask = None
        
        draw_params = dict(matchColor=matchColor,
                            singlePointColor=None,
                            matchesMask=matchesMask,
                            flags=2)
        img_matches = cv2.drawMatches(ref_img, kp_ref, frame_cam, kp_cam, good, None, **draw_params)
        return img_matches

    # Gera imagens de matches para cada câmera com cores diferentes
    img_matches1 = get_matches_img(des1, kp1, frame1, (0, 255, 0))   # Verde para Camera 1
    img_matches2 = get_matches_img(des2, kp2, frame2, (0, 0, 255))   # Vermelho para Camera 2

    # Redimensiona para garantir que tenham o mesmo tamanho
    h = max(img_matches1.shape[0], img_matches2.shape[0])
    w = max(img_matches1.shape[1], img_matches2.shape[1])
    img_matches1 = cv2.resize(img_matches1, (w, h))
    img_matches2 = cv2.resize(img_matches2, (w, h))

    # Junta lado a lado
    combined = np.hstack((img_matches1, img_matches2))

    cv2.imshow("Camera 1 & 2 - Matching", combined)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cam1.release()
cam2.release()
cv2.destroyAllWindows()
