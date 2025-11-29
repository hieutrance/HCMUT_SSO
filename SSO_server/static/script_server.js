document.addEventListener('DOMContentLoaded', function() {
    // Danh sách ảnh nền
    const images = [
        'bg1.jpg',
        'bg2.jpg',
        'bg3.jpg', 
        'bg4.jpg' 
    ];
    
    let currentIndex = 0;
    const intervalTime = 5000; // 5 giây

    // Kiểm tra biến môi trường từ HTML
    if (typeof window.STATIC_IMAGE_URL === 'undefined') {
        console.error("Lỗi: Không tìm thấy đường dẫn ảnh (STATIC_IMAGE_URL).");
        return;
    }

    function changeBackground() {
        // Đường dẫn đã có dấu '/' từ HTML, chỉ cần nối tên file
        const imageUrl = window.STATIC_IMAGE_URL + images[currentIndex];
        
        console.log("Đang tải ảnh nền:", imageUrl); // Dòng này giúp bạn debug (nhấn F12 -> Console để xem)

        // Preload ảnh để tránh nháy
        const img = new Image();
        img.onload = function() {
            document.body.style.backgroundImage = `url('${imageUrl}')`;
        };
        img.onerror = function() {
            console.error("Không tải được ảnh:", imageUrl);
        };
        img.src = imageUrl;

        // Chuyển sang ảnh tiếp theo
        currentIndex = (currentIndex + 1) % images.length;
    }

    // Chạy ngay lập tức
    changeBackground();

    // Lặp lại mỗi 5 giây
    setInterval(changeBackground, intervalTime);
});

// const form = document.getElementById('myForm');

// form.addEventListener('submit', function(event) {
//     event.preventDefault(); // Ngăn việc form submit mặc định (reload page)
//     username = document.getElementById('username')
//     password = document.getElementById('username')


//     // Xử lý dữ liệu form ở đây
// });
