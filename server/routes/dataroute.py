from flask import Blueprint, request, jsonify, make_response
from sqlalchemy import text
from server import db  # Importa o db diretamente do pacote server

data_bp = Blueprint('data', __name__, url_prefix='/data')


##################################
###       SALVAR TREINO        ###
##################################
@data_bp.route("/salvar_treinos", methods=["POST"])
def salvar_treinos():

    data = request.get_json()

    nome = data.get("nome")
    exercicios = data.get("exercicios")

    if not nome or not exercicios:
        return jsonify({"success": False, "error": "Dados inválidos"}), 400

    try:
        result = db.session.execute(
            text("""
            INSERT INTO Treino (nome_treino)
            VALUES (:nome)
            """),
            {"nome": nome}
        )

        treino_id = result.lastrowid

        for ex in exercicios:
            db.session.execute(
                text("""
                INSERT INTO Exercicios
                (id_treino, nome_exercicio, series, repeticao)
                VALUES (:treino_id, :nome_exercicio, :serie, :repeticao)
                """),
                {
                    "treino_id": treino_id,
                    "nome_exercicio": ex["nomeExercicio"],
                    "serie": ex["serie"],
                    "repeticao": ex["repeticoes"]
                }
            )

        db.session.commit()

        return jsonify({"success": True}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


##################################
###        LER TREINOS         ###
##################################
@data_bp.route("/ler_treinos", methods=["GET"])
def ler_treinos():

    try:
        result = db.session.execute(text("""
        SELECT t.id AS treino_id, t.nome_treino,
            e.id AS exercicio_id, e.nome_exercicio, e.series, e.repeticao
        FROM Treino t
        LEFT JOIN Exercicios e
        ON t.id = e.id_treino
        ORDER BY t.id, e.id
        """))

        rows = result.fetchall()

        treinos = {}

        for row in rows:
            treino_id = row[0]

            if treino_id not in treinos:
                treinos[treino_id] = {
                    "id": treino_id,
                    "nome": row[1],
                    "exercicios": []
                }

            if row[2]:
                treinos[treino_id]["exercicios"].append({
                    "id": row[2],
                    "nome_exercicio": row[3],
                    "series": row[4],
                    "repeticoes": row[5]
                })

        return jsonify({
            "success": True,
            "data": list(treinos.values())
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

##################################
###       DELETAR TREINO       ###
##################################

@data_bp.route("/deletar_treino/<int:id>", methods=["DELETE"])
def deletar_treino(id):
    try:
        db.session.execute(
            text("DELETE FROM Treino WHERE id = :id"),
            {"id": id}
        )
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

##################################
###      ATUALIZAR TREINO      ###
##################################

@data_bp.route("/atualizar_treino/<int:idExercicio>", methods=["PUT"])
def atualizar_treino(idExercicio):

    data = request.get_json()

    nome_exercicio = data.get("nome_exercicio")
    serie = data.get("serie")
    repeticao = data.get("repeticao")

    try:
        db.session.execute(
            text(
                """UPDATE Exercicios
                SET nome_exercicio = :nome_exercicio, series = :serie, repeticao = :repeticao
                WHERE id = :id
                """),
                {
                    "id": idExercicio,
                    "nome_exercicio": nome_exercicio,
                    "serie": serie,
                    "repeticao": repeticao
                }
        )

        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
