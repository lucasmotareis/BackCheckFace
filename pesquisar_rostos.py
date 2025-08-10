

from pathlib import Path
import numpy as np
import face_recognition as fr
from PIL import Image
import os

def compare_img_encoder(face2):
    base_dir = Path(r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition")
    
    for pasta in base_dir.iterdir():
        if pasta.is_dir():
            print(f"📂 Pasta: {pasta.name}")
            
            for arquivo in pasta.glob("*.npy"):  # pega só arquivos .npy
                encode1 = np.load(arquivo)
                distancia = fr.face_distance([encode1], face2)[0]
                if distancia < 0.6:
                    print(f"✅ {pasta.name} reconhecido (distância: {distancia:.4f})")
            

def img_user_encoder(file_storage):
    img = np.array(Image.open(file_storage).convert("RGB"))

    locs = fr.face_locations(img)
    if not locs:
        print("Nenhuma face detectada.")
        locs = fr.face_locations(img, model='cnn')
        if not locs:
            return

    encs = fr.face_encodings(img, known_face_locations=locs)
    if not encs:
        print("Não foi possível extrair encoding.")
        return
    
    compare_img_encoder(encs[0])

# Teste
caminho_img = Path(r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition\gilvitao.jpeg")
img_user_encoder(caminho_img)
