document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault(); // Ngăn reload trang
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    console.log(data);
});
