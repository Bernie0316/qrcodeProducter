const canvas = document.querySelector('.qr-canvas');
const ctx = canvas.getContext('2d');

const ssidInput = document.querySelector('.ssid');
const passwordInput = document.querySelector('.password');
const button = document.querySelector('button');

const logoSrc = 'logo.png'; // 你的 Logo 圖片路徑
const qrSize = 300; // QR Code 大小
const logoSize = 61; // Logo 大小

canvas.width = qrSize;
canvas.height = qrSize;

function generateQRCodeWithLogo() {
    const ssid = encodeURIComponent(ssidInput.value);
    const password = encodeURIComponent(passwordInput.value);
    if (!ssid) return; // 沒有 SSID 時，不生成 QR Code

    const wifiData = `WIFI:T:WPA;S:${ssid};P:${password};;`;
    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=${qrSize}x${qrSize}&data=${wifiData}&color=00B900`;

    const qrImg = new Image();
    qrImg.crossOrigin = "anonymous"; // 避免 CORS 問題
    qrImg.src = qrUrl;

    qrImg.onload = function () {
        ctx.clearRect(0, 0, qrSize, qrSize);
        ctx.drawImage(qrImg, 0, 0, qrSize, qrSize);

        // 加上 Logo
        const logoImg = new Image();
        logoImg.src = logoSrc;
        logoImg.onload = function () {
            const centerX = (qrSize - logoSize) / 2;
            const centerY = (qrSize - logoSize) / 2;

            // 畫白色底，避免 Logo 影響 QR Code 可讀性
            ctx.fillStyle = "white";
            ctx.beginPath();
            ctx.arc(qrSize / 2, qrSize / 2, logoSize / 2 + 5, 0, Math.PI * 2);
            ctx.fill();

            // 畫 Logo
            ctx.drawImage(logoImg, centerX, centerY, logoSize, logoSize);
        };
    };
}

// 監聽 SSID & Password 的變更，及時更新 QR Code
ssidInput.addEventListener('input', generateQRCodeWithLogo);
passwordInput.addEventListener('input', generateQRCodeWithLogo);

// 點擊列印
button.addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png'); // 轉成 PNG 圖片
    link.download = 'wifi-qrcode.png'; // 設定下載檔名
    link.click(); // 自動觸發下載
});

// 預設載入時先生成一次
generateQRCodeWithLogo();
