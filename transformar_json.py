
import json
import re

texto = """
nome:MARCELO MELQUIADES DE SOUZA 
nome_da_mae:ANTONIA PEREIRA FELICIANO CARVALHO 
cpf: 058.171.773-23  
data_de_nascimento:  12/02/1988 
endereco:  Rua 19, SN, SETOR PARQUE DOS BURITIS Paraíso do Tocantins/RUA 01 LT:02, P A SANTA CLARA (Energia Ativa no nome da mãe) CPF DELA : 33120945854 TEL: 6399108-6727 (Contato feito pela DPE) FAZ PORTO SEGURO, DIVINOPÓLIS-TO (CONTA ATIVA) 
naturalidade: Cristalandia - TO
passagem: Lei: 2848 Artigo: 217A 
"""


# Quebra por linhas e monta o dicionário
dados = {}
linhas = [l.strip() for l in texto.split("\n") if l.strip()]

for i, linha in enumerate(linhas):
    if ":" in linha:
        chave, valor = linha.split(":", 1)
        # Junta endereço se for quebrado em 2 linhas
        if chave.lower() == "endereco" and i + 1 < len(linhas) and ":" not in linhas[i+1]:
            valor += " " + linhas[i+1]
        dados[chave.strip()] = valor.strip()

# Converte para JSON formatado
json_str = json.dumps(dados, indent=4, ensure_ascii=False)
print(json_str)


