from flask import Blueprint, render_template, request, jsonify, Response, url_for
from .db import USERS
from dicttoxml import dicttoxml
from .model import User, PartialUser, UserWithId

user = Blueprint("user", __name__, url_prefix="/users")


@user.get("/page")
def get_users_page():
    return render_template("users.html", users=USERS.values(), title="Пользователи")


@user.get("/queries")
def get_users_by_queries():
    format = request.args.get("format", "json")

    if format == "xml":
        data = dicttoxml(USERS.values(), custom_root="users", attr_type=False).decode()

        return Response(data, mimetype="application/xml")
    else:
        return jsonify({"data": list(USERS.values())})


@user.get("/headers")
def get_users_by_headers():
    format = request.headers.get("Accept")

    if not format:
        return jsonify({"message": "Accept header not found"}), 404

    format = set(format.split(","))
    print(format)

    if "application/json" in format:
        return jsonify({"data": list(USERS.values())})
    elif "application/xml" in format:
        res = dicttoxml(USERS.values(), custom_root="users", attr_type=False).decode()

        return Response(res, mimetype="application/xml")
    else:
        return (
            jsonify({"message": "The server cannot give data of types from Accept"}),
            404,
        )


@user.get("/<int:user_id>")
def get_user_by_id(user_id: int):
    if user_id in USERS:
        user = USERS[user_id].copy()
        user.pop("id")
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404


@user.post("/")
def create_user():
    user: User | None = request.json

    if not user:
        return jsonify({"message": "User not found"}), 404

    id = (max(USERS.keys()) if USERS else 0) + 1

    USERS[id] = {**user, "id": id}

    res = jsonify(user)
    res.status_code = 201
    res.headers.set(
        "Location", url_for("user.get_user_by_id", user_id=id, _external=True)
    )

    return res


@user.delete("/<int:user_id>")
def delete_user(user_id: int):
    USERS.pop(user_id, None)
    return jsonify({"success": True}), 204


@user.put("/<int:user_id>")
def replace_user(user_id: int):
    user: User | None = request.json

    if not user or user_id not in USERS:
        return jsonify({"message": "User not found"}), 404

    USERS[user_id] = {**user, "id": user_id}

    return jsonify(user)


@user.patch("/<int:user_id>")
def update_user(user_id: int):
    partial_user: PartialUser | None = request.json

    if not partial_user or user_id not in USERS:
        return jsonify({"message": "User not found"}), 404

    user = USERS[user_id]
    print(partial_user)

    for key, value in partial_user.items():
        user[key] = value

    updated_user: UserWithId = user.copy()
    updated_user.pop("id")

    return jsonify(updated_user)
