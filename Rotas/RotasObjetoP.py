from flask import jsonify, request
from Database import executar_consulta, selecionar_dados, conectar_BD


def criar_rotasP(app):
    @app.route('/criar_tabela_ObjetoP', methods=['POST'])
    def criar_tabelaP():
        query = """
        CREATE TABLE IF NOT EXISTS objetos_perdidos(
           id_objeto SERIAL PRIMARY KEY,
           nome_objeto VARCHAR(255),
           cor VARCHAR(100),
           data_perdido VARCHAR(50)
        )
        """
        resultado = executar_consulta(query)
        if resultado:
            return jsonify({'mensagem': 'Tabela criada com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao criar a tabela.'}), 500

    def chamar_stored_procedure(query, params):
        conn = conectar_BD()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                cursor.close()
                return True
            except Exception as error:
                print(f"Erro ao chamar stored procedure: {error}")
                conn.rollback()
                return False
            finally:
                conn.close()
        return False


    @app.route('/inserir_objeto_perdido', methods=['POST'])
    def inserir_objeto_perdido():
        dados = request.json
        nome_objeto = dados.get('nome_objeto')
        cor = dados.get('cor')
        data_perdido = dados.get('data_perdido')

        if not nome_objeto or not cor or not data_perdido:
            return jsonify({'mensagem': 'Dados incompletos'}), 400

        query = "CALL inserir_objeto_perdido(%s, %s, %s)"

        params = (nome_objeto, cor, data_perdido)

        resultado = chamar_stored_procedure(query, params)

        if resultado:
            return jsonify({'mensagem': 'Objeto perdido inserido com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao inserir o objeto perdido'}), 500

    @app.route('/inserir_objeto', methods=['POST'])
    def inserir_objeto():
        dados = request.json
        nome_objeto = dados.get('nome_objeto')
        cor = dados.get('cor')
        data_perdido = dados.get('data_perdido')

        if not nome_objeto or not cor or not data_perdido:
            return jsonify({'mensagem': 'Dados incompletos'}), 400
        query = """
        INSERT INTO objetos_perdidos (nome_objeto, cor, data_perdido)
        VALUES (%s,%s, %s)
        """

        params = (nome_objeto, cor, data_perdido)

        resultado = executar_consulta(query, params)
        if resultado:
            return jsonify({'mensagem': 'Objeto inserido com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao inserir o objeto'}), 500

    @app.route('/listar_logs', methods=['GET'])
    def listar_logs():
        conn = conectar_BD()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM log_insercoes")
                resultado = cursor.fetchall()
                cursor.close()
                return jsonify(resultado)
            except Exception as error:
                print("Erro ao listar logs: ", error)
                return jsonify({'mensagem': 'Erro ao listar logs.'}), 500
            finally:
                conn.close()
        else:
            return jsonify({'mensagem': 'Erro ao conectar ao banco de dados.'}), 500

    @app.route('/atualizar_objeto', methods=['PUT'])
    def atualizar_objeto():
        dados = request.json
        id_objeto = dados.get('id_objeto')
        nome_objeto = dados.get('nome_objeto')
        cor = dados.get('cor')
        data_perdido = dados.get('data_perdido')

        if not id_objeto:
            return jsonify({'mensagem': 'ID do objeto não fornecido'}), 400

        query = """
        UPDATE objetos_perdidos
        SET nome_objeto = %s, cor = %s, data_perdido = %s
        WHERE id_objeto = %s
        """

        params = (nome_objeto, cor, data_perdido, id_objeto)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Objeto atualizado com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao atualizar o objeto'}), 500

    @app.route('/deletar_objeto/<int:id_objeto>', methods=['DELETE'])
    def deletar_objeto(id_objeto):
        query = """
        DELETE FROM objetos_perdidos WHERE id_objeto = %s
        """

        params = (id_objeto,)

        resultado = executar_consulta(query, params)

        if resultado:
            return jsonify({'mensagem': 'Objeto deletado com sucesso'})
        else:
            return jsonify({'mensagem': 'Erro ao deletar o objeto'}), 500

    @app.route('/listar_objetos', methods=['GET'])
    def listar_objetos():
        query = "SELECT * FROM objetos_perdidos"
        resultado = selecionar_dados(query)
        return jsonify(resultado)

    @app.route('/listar_viewObjP', methods=['GET'])
    def listar_viewObjP():
        query = "SELECT * FROM view_objetos_perdidos"
        resultado = selecionar_dados(query)
        return jsonify(resultado)

    @app.route('/listar_objeto/<int:id_objeto>', methods=['GET'])
    def listar_objeto(id_objeto):
        query = "SELECT * FROM objetos_perdidos WHERE id_objeto = %s"
        params = (id_objeto,)
        resultado = selecionar_dados(query, params)
        if resultado:
            return jsonify({"Objeto-perdido": resultado[0]})
        else:
            return jsonify({"mensagem": "Objeto não encontrado"}), 404
