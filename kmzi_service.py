from flask import Flask, request, jsonify

from Modules.math_module import is_prime_for_short

app = Flask(__name__)


@app.route('/sum_big_int/', methods=['POST'])
def sum_big_int():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        num1 = int(json_data["num1"])
        num2 = int(json_data["num2"])
        result = str(num1 + num2)
    except Exception as e:
        error = e.__str__()
    return jsonify(result=result, error=error)


@app.route('/check_is_prime/', methods=['POST'])
def check_is_prime():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        num1 = int(json_data["num"])
        result = str(is_prime_for_short(num1))
    except Exception as e:
        error = e.__str__()
    return jsonify(result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
