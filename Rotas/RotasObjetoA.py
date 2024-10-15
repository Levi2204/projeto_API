from flask import jsonify, request
from Database import executar_consulta, selecionar_dados

def criar_rotasA(app):
    @app.route('/criar_tabela_ObjetoA', methods=['POST'])
    def criar_tabelaA():
        query = """
        CREATE TABLE IF NOT EXISTS objetos_achados(
           id_objetoA SERIAL PRIMARY KEY,
           nome_objeto_achado VARCHAR(255),
           cor_achado VARCHAR(100),
           id_objeto int,
           id_pessoa int,
           FOREIGN KEY (id_objeto) REFERENCES objetos_perdidos (id_objeto),
           FOREIGN KEY (id_pessoa) REFERENCES pessoa (id_pessoa)
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
        nome_objeto_achado = dados.get('nome_objeto_achado')
        cor_achado = dados.get('cor_achado')
        id_objeto = dados.get('id_objeto')
        id_pessoa = dados.get('id_pessoa')

        if not nome_objeto_achado or not cor_achado or not id_objeto or not id_pessoa:
            return jsonify({'mensagem': 'Dados incompletos'}), 400
        query = """
        INSERT INTO objetos_achados (nome_objeto_achado, cor_achado, id_objeto, id_pessoa)
        VALUES (%s,%s,%s,%s)
        """

        params = (nome_objeto_achado, cor_achado, id_objeto, id_pessoa)

        resultado = executar_consulta(query, params)
        if resultado:
            return jsonify({'mensagem': 'Objeto inserido com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao inserir o objeto'}), 500

    @app.route('/atualizar_objetoA', methods=['PUT'])
    def atualizar_objetoA():
        dados = request.json
        id_objetoA = dados.get('id_objetoA')
        nome_objeto_achado = dados.get('nome_objeto_achado')
        cor_achado = dados.get('cor_achado')
        id_objeto = dados.get('id_objeto')
        id_pessoa = dados.get('id_pessoa')


        if not id_objetoA:
            return jsonify({'mensagem': 'ID do objeto não fornecido'}), 400

        query = """
        UPDATE objetos_achados
        SET nome_objeto_achado = %s, cor_achado = %s, id_objeto = %s, id_pessoa = %s
        WHERE id_objetoA = %s
        """

        params = (nome_objeto_achado, cor_achado, id_objeto, id_pessoa, id_objetoA)

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