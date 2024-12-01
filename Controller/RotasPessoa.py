from flask import jsonify, request
from Model.Database import executar_consulta, selecionar_dados

def criar_rotas(app):
    @app.route('/criar_tabela', methods=['POST'])
    def criar_tabela():
        query = """
        CREATE TABLE pessoa(
           id_pessoa int PRIMARY KEY,
           cpf VARCHAR(11),
           nome_pessoa VARCHAR(255),
           email VARCHAR(255),
           telefone VARCHAR(50)
        )
        """
        resultado = executar_consulta(query)
        if resultado:
            return jsonify({'mensagem': 'Tabela criada com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao criar a tabela.'}), 500

    @app.route('/inserir_pessoa', methods=['POST'])
    def inserir_pessoa():
        dados = request.json
        idPessoa = dados.get('id_pessoa')
        nome = dados.get('nome_pessoa')
        email = dados.get('email')
        telefone = dados.get('telefone')

        if not idPessoa or not nome or not email or not telefone:
            return jsonify({'mensagem': 'Dados incompletos'}), 400
        query = """
        INSERT INTO pessoa (id_pessoa, nome_pessoa, email, telefone)
        VALUES (%s,%s,%s, %s)
        """

        params = (idPessoa, nome, email, telefone)

        resultado = executar_consulta(query, params)
        if resultado:
            return jsonify({'mensagem': 'Pessoa inserida com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao inserir a pessoa'}), 500

    @app.route('/atualizar_pessoa', methods=['PUT'])
    def atualizar_pessoa():
        dados = request.json
        idPessoa = dados.get('id_pessoa')
        nome = dados.get('nome_pessoa')
        email = dados.get('email')
        telefone = dados.get('telefone')

        if not idPessoa:
            return jsonify({'mensagem': 'ID da pessoa não fornecido'}), 400

        query = """
        UPDATE pessoa
        SET nome_pessoa = %s, email = %s, telefone = %s
        WHERE id_pessoa = %s
        """

        params = (nome, email, telefone, idPessoa)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Pessoa atualizada com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao atualizar a pessoa'}), 500

    @app.route('/deletar_pessoa/<int:id_pessoa>', methods=['DELETE'])
    def deletar_pessoa(id_pessoa):
        query = """
        DELETE FROM pessoa WHERE id_pessoa = %s
        """

        params = (id_pessoa,)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Pessoa deletada com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao deletar a pessoa'}), 500

    @app.route('/listar_pessoas', methods=['GET'])
    def listar_pessoas():
        query = "SELECT * FROM pessoa"
        resultado = selecionar_dados(query)
        return jsonify(resultado)


    @app.route('/listar_pessoa/<int:id_pessoa>', methods=['GET'])
    def listar_pessoa(id_pessoa):
        query = "SELECT * FROM pessoa WHERE id_pessoa = %s"
        params = (id_pessoa,)
        resultado = selecionar_dados(query, params)
        if resultado:
            return jsonify({"pessoa": resultado[0]})
        else:
            return jsonify({"mensagem": "Pessoa não encontrada"}), 404