from flask import jsonify, request
from Model.Database import executar_consulta, selecionar_dados

def criar_rotasA(app):
    @app.route('/criar_tabela_ObjetoA', methods=['POST'])
    def criar_tabelaA():
        query = """
        CREATE TABLE IF NOT EXISTS objetos_achados(
           id_objetoA SERIAL PRIMARY KEY,
           nome_objeto_achado VARCHAR(255),
           cor_achado VARCHAR(100),
           nome_pessoa VARCHAR(255),
           cpf VARCHAR(14),
           contato VARCHAR(200)
        )
        """
        resultado = executar_consulta(query)
        if resultado:
            return jsonify({'mensagem': 'Tabela criada com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao criar a tabela.'}), 500

    @app.route('/inserir_objetoA', methods=['POST'])
    def inserir_objetoA():
        dados = request.json
        id_objeto = dados.get('id_objeto')
        nome_pessoa = dados.get('nome_pessoa')
        cpf = dados.get('cpf')
        contato = dados.get('contato')

        if not id_objeto:
            return jsonify({'mensagem': 'ID do objeto perdido e ID da pessoa são obrigatórios'}), 400

        query_select = "SELECT nome_objeto, cor FROM objetos_perdidos WHERE id_objeto = %s"
        params_select = (id_objeto,)
        resultado = selecionar_dados(query_select, params_select)

        if not resultado:
            return jsonify({'mensagem': 'Objeto perdido não encontrado'}), 404

        nome_objeto, cor = resultado[0]

        query_insert = """
            INSERT INTO objetos_achados (nome_objeto_achado, cor_achado, nome_pessoa, cpf, contato)
            VALUES (%s, %s, %s, %s, %s)
            """
        params_insert = (nome_objeto, cor, nome_pessoa, cpf, contato)

        resultado_insert = executar_consulta(query_insert, params_insert)

        if resultado_insert:
            return jsonify({'mensagem': 'Objeto achado inserido com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao inserir o objeto achado'}), 500
    @app.route('/atualizar_objetoA', methods=['PUT'])
    def atualizar_objetoA():
        dados = request.json
        id_objetoA = dados.get('id_objetoA')
        nome_objeto_achado = dados.get('nome_objeto_achado')
        cor_achado = dados.get('cor_achado')
        nome_pessoa = dados.get('nome_pessoa')
        cpf = dados.get('cpf')
        contato = dados.get('contato')


        if not id_objetoA:
            return jsonify({'mensagem': 'ID do objeto não fornecido'}), 400

        query = """
        UPDATE objetos_achados
        SET nome_objeto_achado = %s, cor_achado = %s, nome_pessoa = %s, cpf = %s, contato = %s
        WHERE id_objetoA = %s
        """

        params = (nome_objeto_achado, cor_achado, id_objetoA)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Objeto atualizado com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao atualizar o objeto'}), 500

    @app.route('/deletar_objetoA/<int:id_objetoA>', methods=['DELETE'])
    def deletar_objetoA(id_objetoA):
        query = """
        DELETE FROM objetos_achados WHERE id_objetoA = %s
        """

        params = (id_objetoA,)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Objeto deletado com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao deletar o objeto'}), 500

    @app.route('/listar_objetosA', methods=['GET'])
    def listar_objetosA():
        query = "SELECT * FROM objetos_achados"
        resultado = selecionar_dados(query)
        return jsonify(resultado)

    @app.route('/listar_objetoA/<int:id_objetoA>', methods=['GET'])
    def listar_objetoA(id_objetoA):
        query = "SELECT * FROM objetos_achados WHERE id_objetoA = %s"
        params = (id_objetoA,)
        resultado = selecionar_dados(query, params)
        if resultado:
            return jsonify({"Objeto-perdido": resultado[0]})
        else:
            return jsonify({"mensagem": "Objeto não encontrado"}), 404