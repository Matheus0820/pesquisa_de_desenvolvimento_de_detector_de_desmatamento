# Importando bibliotecas
import numpy as np
import cv2
import os

def capturando_caminho_imagens_e_nome(caminho):
    # Lista de imagens a serem analisadas
    list_imgs = []
    nome_imgs = []

    for root, dirs, files in os.walk(caminho):
        for img_name in files:
            img_caminho = os.path.join(root, img_name)
            list_imgs.append(img_caminho)
            nome_imgs.append(img_name)

    return list_imgs, nome_imgs
def redimensionar_imagem(img):
    largura = 600
    altura = 500
    img = cv2.resize(img, (largura, altura), interpolation=cv2.INTER_AREA)

    return img

def indentificando_area_sem_vegeracao(img):
    # Criando HSV da imagem
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Delimitação das cores das nuvens
    white_donw = np.array([0, 0, 200])
    white_upper = np.array([179, 50, 255])

    # Delimitações de cores verde e azul
    # Verde
    green_donw = np.array([35, 10, 10])  # EM HSV
    green_upper = np.array([85, 255, 255])  # EM HSV

    # Azul
    blue_donw = np.array([90, 50, 20])  # EM HSV
    blue_upper = np.array([120, 255, 255])  # EM HSV

    # Criando máscaras para as duas cores
    green_mask = cv2.inRange(hsv, green_donw, green_upper)
    blue_mask = cv2.inRange(hsv, blue_donw, blue_upper)
    white_mask = cv2.inRange(hsv, white_donw, white_upper)

    # Criando a visinhaça de pixel considerada
    karnel = np.ones((5, 5), 'uint8')

    # Ditalando a mascara - Deixando ela maior e corrigindo erros
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, karnel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, karnel)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, karnel)

    # Região onde a área não é verde ou azul - Área desmatada, urbanizada ou queimada
    green_not_mask = cv2.bitwise_not(green_mask)
    res_not_green = cv2.bitwise_and(img, img, mask=green_not_mask)  # Imagem só com área sem verde

    blue_not_mask = cv2.bitwise_not(blue_mask)
    res_not_blue = cv2.bitwise_and(img, img, mask=blue_not_mask)  # Imagem só com a área azul

    white_not_mask = cv2.bitwise_not(white_mask)
    res_not_mask = cv2.bitwise_and(img, img, mask=white_not_mask)  # Imagem só com área branca

    # Juntando as duas mascaras da área desmatada em só uma
    non_green_and_blue_and_white_mask = cv2.bitwise_and(green_not_mask, blue_not_mask, white_not_mask)
    res_non_green_and_blue_and_white = cv2.bitwise_and(img, img, mask=non_green_and_blue_and_white_mask)

    # Criando sobreposição colorida na imagem original de área desmatada
    img_sbp = np.zeros_like(img, dtype=np.uint8)
    img_sbp[non_green_and_blue_and_white_mask == 255] = (0, 0, 255)  # Definindo a imagem de sobreposição como a mascara de cor vermelha

    return img_sbp

def sobrepondo_imagem(img, img_sobreposicao):
    # Colocando sobreposição na imagem original
    image_com_sbp = cv2.addWeighted(img, 0.5, img_sobreposicao, 0.5, 0)

    return image_com_sbp

def colando_imagem(img, img_com_sbp):
    merged_image = np.hstack((img, img_com_sbp))

    return merged_image

def salvar_resultado(img, caminho, nome):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    cv2.imwrite(caminho + nome, img)