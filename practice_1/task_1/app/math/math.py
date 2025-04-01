from flask import Blueprint, request, jsonify

math = Blueprint("math", __name__, url_prefix="/math")


@math.post("/squares")
def calc_square():
    number = request.form.get("number")

    if number and number.isdigit():
        answer = {"answer": int(number) ** 2}
        return jsonify({"data": answer})
    else:
        return jsonify({"message": "Number not found"}), 404
