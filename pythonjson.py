 # arquivos_json = [f for f in pasta.iterdir() if f.suffix.lower() == ".json"]
        # if not arquivos_json:
        #     print(f"Nenhum JSON encontrado em {pasta.name}")
        #     continue
        # with open(arquivos_json[0], "r", encoding="utf-8") as arquivo:
        #     dados = json.load(arquivo)
        #     nome_individuo = dados.get("nome", "Desconhecido")
        #     nome_da_mae = dados.get("nome_da_mae", "Desconhecido")
        #     cpf = dados.get("cpf", "Desconhecido")
        #     data_de_nascimento = dados.get("data_de_nascimento", "Desconhecido")
        #     endereco = dados.get("endereco", "Desconhecido")
        #     passagem = dados.get("passagem", "Desconhecido")