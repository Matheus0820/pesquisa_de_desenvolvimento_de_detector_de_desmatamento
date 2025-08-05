# Importações
import numpy as np
import cv2
import os
from funcoes import *

def main():
    # Pasta de imgens a serem analisadas
    caminho_analise = 'Imagens_para_analise/'

    # Pasta de salvamento dos resultados
    caminho_resultados = 'Resultados/'

    list_imgs, nome_imgs = capturando_caminho_imagens_e_nome(caminho_analise)

    for img, nome in zip(list_imgs, nome_imgs):
        img = cv2.imread(img)

        img_sbp = indentificando_area_sem_vegeracao(img)
        img = redimensionar_imagem(img)
        img_sbp = redimensionar_imagem(img_sbp)

        result = sobrepondo_imagem(img, img_sbp)
        marged_result = colando_imagem(img, result)

        salvar_resultado(marged_result, caminho_resultados, nome)




if __name__ == "__main__":
    main()