import cv2
import numpy as np
import pyttsx3
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Inicializa a engine de voz
voz = pyttsx3.init()
voz.setProperty('rate', 150)

# Função para identificar o nome da cor
def nome_da_cor(h, s, v):
    if s < 40 and v > 200:
        return "branco"
    elif v < 40:
        return "preto"
    elif h < 15 or h > 165:
        return "vermelho"
    elif 15 <= h < 35:
        return "amarelo"
    elif 35 <= h < 85:
        return "verde"
    elif 86 <= h < 135:
        return "azul"
    elif 135 <= h < 160:
        return "roxo"
    elif 161 <= h <= 169:
        return "rosa"
    return "indefinido"

# Função que fala a cor atual
def falar_cor():
    global cor_atual
    if cor_atual and cor_atual != "indefinido":
        threading.Thread(target=lambda: voz.say(f"A cor é {cor_atual}") or voz.runAndWait()).start()

# Atualiza a imagem da webcam
def atualizar_video():
    global cor_atual
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    altura, largura, _ = frame.shape
    cx, cy = largura // 2, altura // 2

    # Região para análise
    roi = frame[cy-10:cy+10, cx-10:cx+10]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[10, 10]
    cor_atual = nome_da_cor(h, s, v)

    # Desenha círculo e nome da cor
    cv2.circle(frame, (cx, cy), 10, (255, 255, 255), 2)
    cv2.putText(frame, cor_atual, (cx + 20, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # Converte para ImageTk e mostra no label
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    video_label.imgtk = img_tk
    video_label.configure(image=img_tk)

    # Repetir após 20 ms
    janela.after(20, atualizar_video)

# Inicia a câmera
cap = cv2.VideoCapture(0)
cor_atual = ""

# Interface Tkinter
janela = tk.Tk()
janela.title("Detector de Cor com Botão")

video_label = tk.Label(janela)
video_label.pack()

botao = tk.Button(janela, text="Falar Cor", font=("Arial", 16), command=falar_cor, bg="lightblue")
botao.pack(pady=10)

# Começa o loop de vídeo
atualizar_video()
janela.mainloop()

cap.release()
