from flask import Flask, request, jsonify
import re

app = Flask(__name__)
web = "<!DOCTYPE html><html><head><title>Hoi!</title></head><body><p>hi</p></body></html>"
webcontent = ''
idx = -1
value = 0

def binary(value, idx):
    if idx == -1:
        return "00000000"
    value += 128  # the 8th bit
    return str(format(int(value) & 0xFF, '07b'))

def parse_html():
    titleweb = re.findall(r'<title[^>]*>(.*?)<\/title>', web, re.I | re.S)
    pgsweb = re.findall(r'<p[^>]*>(.*?)<\/p>', web, re.I | re.S)
    if not titleweb or not pgsweb:
        return "Default Content"
    return titleweb[0] + "     " + " ".join(pgsweb)

# Инициализация webcontent при старте
webcontent = parse_html()

@app.route('/', methods=['GET', 'POST'])
def main():
    global webcontent, idx, value
    if request.method == "GET":
        if not webcontent or idx < 0 or idx >= len(webcontent):
            idx = -1
            return jsonify({"value": "10000000"})

        char = webcontent[idx]
        if char == ' ':
            value = 0
        elif char.isdigit():
            num = int(char)
            value = 26 + num if 1 <= num <= 9 else 36
        elif char.isalpha():
            value = ord(char.lower()) - 96
        else:
            value = None

        if not isinstance(value, int):
            value = "11011101"
        else:
            if char.isupper():
                value += 64
            value = binary(value, idx)

        idx += 1
        return jsonify({"value": value})

    elif request.method == "POST":
        webcontent = parse_html()
        idx = -1  # Сброс индекса
        return jsonify({"value": "10000000"})

    return jsonify({"error": "Unknown method"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)