
const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', function(event) {
    event.preventDefault();
    let formData = new FormData(loginForm);
    let formDataEntries = Object.fromEntries(formData);
    let bodyStr = JSON.stringify(formDataEntries);

    fetch('http://127.0.0.1:8000/api/token/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: bodyStr
    })
    .then(response=>{
        return response.json();
    })
    .then(authData => {
        let endpoint = 'http://127.0.0.1:8000/';
        handleLogin(authData, endpoint);
    })
    .catch(err=> {
        console.log('err', err)
    })
})

function handleLogin(authData, endpoint, url_method, url_body) {
    localStorage.setItem('access', authData.access);
    localStorage.setItem('refresh', authData.refresh);
    document.cookie = `access_token=${authData.access}; path=/`;
    window.location.href = endpoint;
}
