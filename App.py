from flask import Flask
from Controller.RotasPessoa import criar_rotas
from Controller.RotasObjetoP import criar_rotasP
from Controller.RotasObjetoA import criar_rotasA

app = Flask(__name__)

criar_rotas(app)
criar_rotasP(app)
criar_rotasA(app)


if __name__ == "__main__":
    app.run(debug=True)
