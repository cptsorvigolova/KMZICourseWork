from flask import Flask, request, jsonify

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
    return jsonify(sum=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)
