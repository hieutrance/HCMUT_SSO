document.addEventListener('DOMContentLoaded', function() {
    const images = [
        'bg1.jpg',
        'bg2.jpg',
        'bg3.jpg', 
        'bg4.jpg' 
    ];
    
    let currentIndex = 0;
    const intervalTime = 5000; // 5 giây

    if (typeof window.STATIC_IMAGE_URL === 'undefined') {
        console.error("Lỗi: Không tìm thấy đường dẫn ảnh (STATIC_IMAGE_URL).");
        return;
    }

    function changeBackground() {
        const imageUrl = window.STATIC_IMAGE_URL + images[currentIndex];
        
        console.log("Đang tải ảnh nền:", imageUrl); 
        const img = new Image();
        img.onload = function() {
            document.body.style.backgroundImage = `url('${imageUrl}')`;
        };
        img.onerror = function() {
            console.error("Không tải được ảnh:", imageUrl);
        };
        img.src = imageUrl;

        currentIndex = (currentIndex + 1) % images.length;
    }
    changeBackground();
    setInterval(changeBackground, intervalTime);
});
const params = new URLSearchParams(window.location.search);
document.getElementById('redirect_uri').value = params.get('redirect_uri') || '';
document.getElementById('scope').value = params.get('scope') || '';
document.getElementById('client_id').value = params.get('client_id') || '';
document.getElementById('redirect_uri').value = params.get('redirect_uri')

const loginForm = document.getElementById('login-form')