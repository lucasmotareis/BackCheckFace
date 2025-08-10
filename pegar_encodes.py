import cv2
import face_recognition as fr
import numpy as np
from pathlib import Path
import os
import json


def load_rgb(path, use_cv2=False):
    if use_cv2:
        bgr = cv2.imread(path)
        if bgr is None:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    else:
        # face_recognition.load_image_file já entrega RGB
        img = fr.load_image_file(path)
        if img is None:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        return img

caminho = Path(r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition")
pastas = [p for p in caminho.iterdir() if p.is_dir()]



for pasta in pastas:
    contador = 1
    imagens_jpeg = [f.name for f in pasta.iterdir() if f.suffix.lower() == ".jpeg"]
    print(f"📂 Pasta: {pasta.name}")        
    arquivos_json = [f for f in pasta.iterdir() if f.suffix.lower() == ".json"]
    if not arquivos_json:
        print(f"Nenhum JSON encontrado em {pasta.name}")
        continue
    with open(arquivos_json[0], "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        nome_individuo = dados.get("nome", "Desconhecido")


    for imagem in imagens_jpeg:
        p1 = os.path.join(pasta, imagem)  # monta o caminho completo
        img1 = load_rgb(p1, use_cv2=False)
        # detectar faces (tente model='cnn' se hog falhar e você tiver dlib com suporte)
        locs1 = fr.face_locations(img1,model='cnn')  

        if not locs1:
            print("Nenhuma face detectada em img1 — verifique rotação/recorte/qualidade.")
        # Extrair encodings com segurança
        enc1 = fr.face_encodings(img1, known_face_locations=locs1) if locs1 else []

        if not enc1:
            print("Não foi possível extrair encoding de uma das imagens. Abortando comparação.")
        else:
            nome_malandro = os.path.join(pasta, f"{nome_individuo}.npy")

            while os.path.exists(nome_malandro):
                nome_malandro = os.path.join(pasta,f"{nome_individuo}_{contador}.npy")

                contador += 1
            e1 = enc1[0]
            np.save(nome_malandro, e1)

