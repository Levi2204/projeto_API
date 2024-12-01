from flask import Flask
from Controller.RotasObjetoP import criar_rotasP
from Controller.RotasObjetoA import criar_rotasA

app = Flask(__name__)

criar_rotasP(app)
criar_rotasA(app)


if __name__ == "__main__":
    app.run(debug=True)
