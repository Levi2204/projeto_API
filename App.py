from flask import Flask
from Rotas.RotasPessoa import criar_rotas
from Rotas.RotasObjetoP import criar_rotasP
from Rotas.RotasObjetoA import criar_rotasA

app = Flask(__name__)

criar_rotas(app)
criar_rotasP(app)
criar_rotasA(app)


if __name__ == "__main__":
    app.run(debug=True)
