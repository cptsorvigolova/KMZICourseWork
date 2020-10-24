from flask import Flask, request, jsonify
from Modules.math_module import is_prime, factorize_int
from Modules.rsa_module import get_open_exp_candidates

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
        num = int(json_data["num"])
        result = str(is_prime(num))
    except Exception as e:
        error = e.__str__()
    return jsonify(result=result, error=error)


@app.route('/generate_open_exp/', methods=['POST'])
def generate_open_exp():
    p, q, n, r = 0, 0, 0, 0
    error = ''
    candidates = []
    try:
        json_data = request.get_json()
        p = int(json_data["p"])
        q = int(json_data["q"])
        if not is_prime(p):
            raise Exception('p is not prime')
        if not is_prime(q):
            raise Exception('q is not prime')
        n = p * q
        r = (p - 1) * (q - 1)
        candidates = get_open_exp_candidates(r)
    except Exception as e:
        error = e.__str__()
    return jsonify(n=str(n), r=str(r), candidates=candidates, error=error)


@app.route('/factorize/', methods=['POST'])
def factorize():
    error = ''
    result = []
    try:
        json_data = request.get_json()
        num = int(json_data["num"])
        result = factorize_int(num)
    except Exception as e:
        error = e.__str__()
    return jsonify(result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
