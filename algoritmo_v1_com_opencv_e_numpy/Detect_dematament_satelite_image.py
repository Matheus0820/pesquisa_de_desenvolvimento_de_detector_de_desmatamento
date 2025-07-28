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




# cv2.imshow('Imagem Original', image)
# cv2.imshow('Mascara NAO Verde', green_not_mask)
# cv2.imshow('Mascara NAO Azul', blue_not_mask)
# cv2.imshow('Mascara: NEM Verde NEM Azul (Interseccao)', non_green_and_blue_mask)
# # cv2.imshow('Resultado: Somente NEM Verde NEM Azul', res_non_green_and_non_blue)

cv2.waitKey(0)
# cv2.destroyAllWindows()
