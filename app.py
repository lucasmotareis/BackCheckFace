from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import face_recognition as fr
import numpy as np
from pathlib import Path
import os
import json
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)
# Rota simples para testar
@app.route('/')

def buscar_info_json(arquivos_json,nome_pasta):
    if not arquivos_json:
        print(f"Nenhum JSON encontrado em {nome_pasta}")
        return
    with open(arquivos_json[0], "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        nome_individuo = dados.get("nome", "Desconhecido")
        nome_da_mae = dados.get("nome_da_mae", "Desconhecido")
        cpf = dados.get("cpf", "Desconhecido")
        data_de_nascimento = dados.get("data_de_nascimento", "Desconhecido")
        endereco = dados.get("endereco", "Desconhecido")
        passagem = dados.get("passagem", "Desconhecido")
    return nome_individuo,cpf,nome_da_mae,data_de_nascimento

def compare_img_encoder(face2):
    base_dir = Path(r"C:\Users\lucas\Downloads\WhatsApp Unknown 2025-08-07 at 11.04.37\facialRecognition")
    pessoas = []
    for pasta in base_dir.iterdir():
        if pasta.is_dir():
            print(f"📂 Pasta: {pasta.name}")
            arquivos_json = [f for f in pasta.iterdir() if f.suffix.lower() == ".json"]
            resultado = buscar_info_json(arquivos_json,pasta.name)
            if resultado == None:
                print("Não é uma pessoa")
                continue
            else:
                nome_individuo,cpf,nome_da_mae,data_de_nascimento=resultado
            for arquivo in pasta.glob("*.npy"):  # pega só arquivos .npy
                encode1 = np.load(arquivo)
                distancia = fr.face_distance([encode1], face2)[0]
                if distancia < 0.6:
                    pessoas.append({
                        "nome": nome_individuo,
                        "distancia": distancia,
                        "cpf": cpf,
                        "nome_da_mae": nome_da_mae,
                        "data_de_nascimento": data_de_nascimento
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



# Exemplo: rota POST que recebe dados JSON e responde
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
