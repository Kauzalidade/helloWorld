import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import Flask, jsonify, request

from . import db as dbmod


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-troque-esta-chave-em-producao-0123456789"),
        DATABASE=os.environ.get("DATABASE", os.path.join(app.instance_path, "rh.db")),
        TOKEN_HORAS=int(os.environ.get("TOKEN_HORAS", "8")),   # controle de sessão (RNF-01)
        CORS_ORIGIN=os.environ.get("CORS_ORIGIN", "*"),         # origem do front-end em desenvolvimento
    )
    if config:
        app.config.update(config)
    os.makedirs(os.path.dirname(os.path.abspath(app.config["DATABASE"])), exist_ok=True)
    dbmod.init_app(app)

    from . import routes_auth, routes_cadastro, routes_misc
    for modulo in (routes_auth, routes_cadastro, routes_misc):
        app.register_blueprint(modulo.bp)

    @app.before_request
    def preflight():
        if request.method == "OPTIONS":
            resp = app.make_default_options_response()
            origem = app.config.get("CORS_ORIGIN", "*")
            if origem:
                resp.headers["Access-Control-Allow-Origin"] = origem
                resp.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
                resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            return resp

    @app.after_request
    def cors(resp):
        origem = app.config.get("CORS_ORIGIN", "*")
        if origem:
            resp.headers["Access-Control-Allow-Origin"] = origem
            resp.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return resp

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return jsonify({"erro": "Rota não encontrada."}), 404

    @app.errorhandler(405)
    def metodo(_e):
        return jsonify({"erro": "Método não permitido."}), 405

    return app
