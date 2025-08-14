from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import cv2
import face_recognition as fr
import numpy as np
from pathlib import Path
import os
import json
from PIL import Image
import re
from io import BytesIO

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
BASE_DIR = Path(r"C:\Users\lucas\Downloads\ProjetoFacial\BackCheckFace\MALODROMO")


@app.route("/uploads/<path:filename>")
def serve_image(filename):
    print(UPLOAD_FOLDER)
    return send_from_directory(UPLOAD_FOLDER, filename)



def ajustar_caminhos_imagens(html_content):
    return re.sub(
        r'src="([^"]+\.(?:png|jpg|jpeg|gif))"',
        lambda m: f'src="http://127.0.0.1:5000/uploads/{m.group(1)}"',
        html_content
    )

def compare_img_encoder(face2):
    pessoas = []
    for pasta in BASE_DIR.iterdir():
        if pasta.is_dir():
            print(f"📂 Pasta: {pasta.name}")
            for arquivo in pasta.glob("*.npy"):  # pega só arquivos .npy
                encode1 = np.load(arquivo)
                distancia = fr.face_distance([encode1], face2)[0]
                if distancia < 0.6:
                    html_file = next(pasta.glob("*.html"), None)
                    html_content = None

                    if html_file:
                        with open(html_file, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        # Troca src de imagens para /uploads/
                        html_content = ajustar_caminhos_imagens(html_content)

                    pessoas.append({
                        "nome_pasta": pasta.name,
                        "distancia": float(distancia),
                        "html": html_content
                    })
    return pessoas



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
    return encs[0]



@app.route('/reconhecimento', methods=['POST'])
def reconhecimento():
    if 'foto' not in request.files:
        return jsonify({"mensagem": "Nenhuma foto enviada"}), 400
    print("recebemos a foto")
    foto = request.files['foto']

    encode  = img_user_encoder(foto)
    if encode is None:
        return jsonify({"erro": "deu merda"}), 400
    print("encode deu certo")
    busca_finalizada = compare_img_encoder(encode)

    
    print(busca_finalizada)
    return jsonify({"mensagem": "Busca finalizada com sucesso.", "resultado": busca_finalizada})

if __name__ == '__main__':
    app.run(debug=True)
