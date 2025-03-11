from flask import Flask, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    ssid = request.args.get('ssid')
    password = request.args.get('password')

    if not ssid or not password:
        return "缺少 Wi-Fi 名稱或密碼", 400

    wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
