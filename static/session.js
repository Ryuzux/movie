document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById("login");
    const profileButton = document.getElementById("profile");
    const registerButton = document.getElementById("register");
    const settingButton = document.getElementById("settings");
    const homeButton = document.getElementById("home");

    function updateLoginButton(isLoggedIn) {
        if (isLoggedIn) {
            loginButton.textContent = "Logout";
            registerButton.style.display = "none";
            profileButton.style.display = "block";
            settingButton.style.display = "block";

            loginButton.onclick = function() {
                fetch('/logout', { method: 'POST' })
                    .then(response => {
                        if (response.ok) {
                            window.location.href = "/home";
                        } else {
                            throw new Error('Logout failed');
                        }
                    })
                    .catch(error => {
                        console.error('Error logging out:', error);
                    });
            };
        } else {
            loginButton.textContent = "Login";
            registerButton.style.display = "inline-block";
            profileButton.style.display = "none";
            settingButton.style.display = "none";

            loginButton.onclick = function() {
                window.location.href = "/login";
            };
        }
    }

    fetch('/check_session')
        .then(response => response.json())
        .then(data => {
            const isLoggedIn = data.logged_in;
            updateLoginButton(isLoggedIn);

            profileButton.onclick = function() {
                if (isLoggedIn) {
                    window.location.href = "/user";
                } else {
                    window.location.href = "/login";
                }
            };
        })
        .catch(error => {
            console.error('Error checking session:', error);
        });

    if (homeButton) {
        homeButton.onclick = function() {
            window.location.href = "/home";
        };
    }
});
