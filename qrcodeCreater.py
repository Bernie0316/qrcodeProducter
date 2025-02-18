# Wifi QR Code 生成程式碼

import qrcode
from PIL import Image, ImageColor

SSID = input("請輸入Wifi名稱: ")
Password = input("請輸入Wifi密碼: ")

wifi_data = f"WIFI:T:WPA;S:{SSID};P:{Password};;"

# Wi-Fi的QR Code格式
# wifi_data = "WIFI:T:WPA;S:etmore_B3;P:0933150808;;"

# 生成Wi-Fi QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高錯誤修正，以容納Logo
    box_size=10,
    border=4,
)
qr.add_data(wifi_data)
qr.make(fit=True)

# 設定 QR Code 顏色
fill_color = ImageColor.getrgb("#00B900")  # 轉換 HEX 為 RGB
qr_img = qr.make_image(fill_color=fill_color, back_color="white").convert("RGBA")

# 打開公司 Logo
logo = Image.open("logo.png").convert("RGBA")

# 設定 Logo 的最大尺寸（保持比例）
qr_size = qr_img.size[0]  # QR Code的寬度
max_logo_size = qr_size // 4  # Logo最大不超過QR Code的1/4

# 計算縮放比例（保持長寬比）
logo_ratio = min(max_logo_size / logo.width, max_logo_size / logo.height)
new_logo_size = (int(logo.width * logo_ratio), int(logo.height * logo_ratio))

# 縮放 Logo
logo = logo.resize(new_logo_size, Image.LANCZOS)

# 創建透明背景的方形圖層，確保 Logo 居中
square_size = max_logo_size  # 讓填充區域是正方形
logo_with_padding = Image.new("RGBA", (square_size, square_size), (255, 255, 255, 0))
logo_offset = ((square_size - new_logo_size[0]) // 2, (square_size - new_logo_size[1]) // 2)
logo_with_padding.paste(logo, logo_offset, logo)

# 計算 Logo 的放置位置（QR Code 中央）
offset = ((qr_size - square_size) // 2, (qr_size - square_size) // 2)

# 將 Logo 貼到 QR Code 上
qr_img.paste(logo_with_padding, offset, logo_with_padding)

# 顯示和保存
qr_img.show()
qr_img.save(f"{SSID}.png")
