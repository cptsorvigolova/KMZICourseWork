import binascii

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Modules.math_module import is_prime, factorize_int, is_coprime
from Modules.rsa_module import get_exponent_candidates, encrypt
import Modules.kuznechik_module as kuznechik

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def apply_caching(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Max-Age", "86400")
    return response


@app.route('/rsa/sum_big_int/', methods=['POST'])
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
    response = jsonify(result=result, error=error)
    return response


@app.route('/rsa/check_is_prime/', methods=['POST'])
def check_is_prime():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        num = int(json_data["num"])
        result = str(is_prime(num))
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result, error=error)
    return response


@app.route('/rsa/factorize/', methods=['POST'])
def factorize():
    error = ''
    result = []
    try:
        json_data = request.get_json()
        num = int(json_data["num"])
        if is_prime(num):
            raise Exception('Число простое.')
        result = factorize_int(num)
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result, error=error)
    return response


@app.route('/rsa/generate_exponents/', methods=['POST'])
def generate_exponents():
    p, q, n, r = 0, 0, 0, 0
    error = ''
    candidates = []
    try:
        json_data = request.get_json()
        p = int(json_data["p"])
        q = int(json_data["q"])
        if not is_prime(p):
            raise Exception('p не простое.')
        if not is_prime(q):
            raise Exception('q не простое.')
        if len(bin(p)) != len(bin(q)):
            raise Exception('p и q должны быть одинаковой разрядности в двоичном виде.')
        n = p * q
        r = (p - 1) * (q - 1)
        candidates = get_exponent_candidates(r)
    except Exception as e:
        error = e.__str__()
    response = jsonify(n=str(n), r=str(r), candidates=candidates, error=error)
    return response


@app.route('/rsa/calculate_edr/', methods=['POST'])
def calculate_edr():
    error = ''
    ed = ''
    edmodr = ''
    er_iscoprime = False
    ed_iscoprime = False
    try:
        json_data = request.get_json()
        e = int(json_data["e"])
        d = int(json_data["d"])
        r = int(json_data["r"])
        ed = str(e * d)
        edmodr = str((e * d) % r)
        er_iscoprime = is_coprime(e, r)
        ed_iscoprime = is_coprime(e, d)
    except Exception as e:
        error = e.__str__()
    response = jsonify(ed=str(ed),
                       edmodr=str(edmodr),
                       er_iscoprime=er_iscoprime,
                       ed_iscoprime=ed_iscoprime,
                       error=error)
    return response


@app.route('/rsa/encrypt_session_key/', methods=['POST'])
def encrypt_session_key():
    error = ''
    encrypted_session_key = ''
    try:
        json_data = request.get_json()
        e = int(json_data["e"])
        n = int(json_data["n"])
        session_key = int(json_data["session_key"])
        if session_key not in range(0, n):
            raise Exception('Сессионный ключ должен быть в диапазоне от 0 до ' + str(n))
        encrypted_session_key = encrypt(e, n, session_key)
    except Exception as e:
        error = e.__str__()
    response = jsonify(encrypted_session_key=str(encrypted_session_key),
                       error=error)
    return response


@app.route('/kuznechik/expand_text/', methods=['POST'])
def expand_text():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        text = str(json_data["text"])
        result = kuznechik.expand(text)
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/unexpand_text/', methods=['POST'])
def unexpand_text():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        text = str(json_data["text"])
        result = kuznechik.unexpand(text)
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/split_text/', methods=['POST'])
def split_text():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        text = str(json_data["text"])
        result = ', '.join(kuznechik.split(text))
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/generate_round_keys/', methods=['POST'])
def generate_round_keys():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        master_key = bytes(json_data["master_key"], 'utf-8')
        keys = [binascii.hexlify(key).decode('utf-8') for key in kuznechik.get_round_keys(master_key)]
        result = ', '.join(keys)
    except Exception as e:
        error = e.__str__()
    response = jsonify(round_keys=result,
                       error=error)
    return response


@app.route('/kuznechik/encrypt_block/', methods=['POST'])
def encrypt_block():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        master_key = bytes(json_data["master_key"], 'utf-8')
        block = bytes(json_data["block"], 'utf-8')
        result = binascii.hexlify(kuznechik.encrypt_block(block, master_key)).decode('utf-8')
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/decrypt_block/', methods=['POST'])
def decrypt_block():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        master_key = bytes(json_data["master_key"], 'utf-8')
        block = binascii.unhexlify(str(json_data["block"]))
        result = kuznechik.decrypt_block(bytes(block), master_key).decode('utf-8')
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/encrypt_text/', methods=['POST'])
def encrypt_text():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        master_key = bytes(json_data["master_key"], 'utf-8')
        text = str(json_data["text"])
        result = binascii.hexlify(kuznechik.encrypt_text(text, master_key)).decode('utf-8')
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


@app.route('/kuznechik/decrypt_text/', methods=['POST'])
def decrypt_text():
    error = ''
    result = ''
    try:
        json_data = request.get_json()
        master_key = bytes(json_data["master_key"], 'utf-8')
        text = binascii.unhexlify(str(json_data["text"]))
        result = kuznechik.decrypt_text(text, master_key)
    except Exception as e:
        error = e.__str__()
    response = jsonify(result=result,
                       error=error)
    return response


if __name__ == '__main__':
    app.run(debug=True)
