# Importando bibliotecas
import numpy as np
import cv2

# Carregando imagem
image = cv2.imread('imagens/img_1.png')

# Criando HSV da imagem
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Delimitações de cores verde e azul
# Verde
green_donw = np.array([35, 10, 10]) # EM HSV
green_upper = np.array([85, 255, 255]) # EM HSV

# Azul
blue_donw = np.array([94, 80, 2]) # EM HSV
blue_upper = np.array([120, 255, 255]) # EM HSV

# Criando máscaras para as duas cores
green_mask = cv2.inRange(hsv, green_donw, green_upper)
blue_mask = cv2.inRange(hsv, blue_donw, blue_upper)

# Criando a visinhaça de pixel considerada
karnel = np.ones((5, 5), 'uint8')

# Ditalando a mascara - Deixando ela maior
green_mask = cv2.dilate(green_mask, karnel)
blue_mask = cv2.dilate(blue_mask, karnel)

# Região onde a área não é verde ou azul - Área desmatada, urbanizada ou queimada
green_not_mask = cv2.bitwise_not(green_mask)
res_not_green = cv2.bitwise_and(image, image, mask=green_not_mask) # Imagem só com área sem verde

blue_not_mask = cv2.bitwise_not(blue_mask)
res_not_blue = cv2.bitwise_and(image, image, mask=blue_not_mask) # Imagem só com a área azul

# Juntando as duas mascaras da área desmatada em só uma
non_green_and_blue_mask = cv2.bitwise_and(green_not_mask, blue_not_mask)
res_non_green_and_blue = cv2.bitwise_and(image, image, mask=non_green_and_blue_mask)


# Criando sobreposição colorida na imagem original de área desmatada
img_sbp = np.zeros_like(image, dtype=np.uint8)
img_sbp[non_green_and_blue_mask == 255] = (0, 0, 255) # Definindo a imagem de sobreposição como a mascara de cor vermelha

# Colocando sobreposição na imagem original
image_com_sbp = cv2.addWeighted(image, 0.5, img_sbp, 0.5, 0)


# Redimensionando imagens
largura = 600
altura = 500
image = cv2.resize(image, (largura, altura), interpolation=cv2.INTER_AREA)
image_com_sbp = cv2.resize(image_com_sbp, (largura, altura), interpolation=cv2.INTER_AREA)

# Colando Imagens
merged_image = np.hstack((image, image_com_sbp))

# Mostrando Resultado
cv2.imshow('Resultado - Áreas possivelmente desmatada', merged_image)

# Mostrando imagens
# cv2.imshow('Imagem Original', image)
# cv2.imshow('Mascara: Sem verde e azul (Interseccao)', non_green_and_blue_mask)
# cv2.imshow('Localização de desmatamento', image_com_sbp)

cv2.waitKey(0)
# cv2.destroyAllWindows()
