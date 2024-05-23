document.getElementById("topmovie").onclick = function() {
    window.location.href = "/topmovie";
};

document.getElementById("nowplaying").onclick = function() {
    window.location.href = "/nowplaying";
};

document.getElementById("register").onclick = function() {
    window.location.href = "/register";
};

document.getElementById("home").onclick = function() {
    window.location.href = "/home";
};

document.getElementById("settings").onclick = function() {
    window.location.href = "/update/user";
};

document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.getElementById("login");
    const profileButton = document.getElementById("profile");
    const profileContainer = document.getElementById("profile-container");
    const registerButton = document.getElementById("register");
    const settingButton = document.getElementById("settings");
    const homeButton = document.getElementById("home");
    const topupbutton = document.getElementById("topup")

    if (typeof sessionData !== 'undefined') {
        const isLoggedIn = sessionData.logged_in;

        function updateLoginButton() {
            if (isLoggedIn) {
                loginButton.textContent = "Logout";
                registerButton.style.display = "none";
                loginButton.onclick = function() {
                    fetch('/logout', { method: 'POST' })
                        .then(response => {
                            if (response.ok) {
                                window.location.href = "/home";
                            }
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
        updateLoginButton();

        profileButton.onclick = function() {
            if (isLoggedIn) {
                window.location.href = "/user";
            } else {    
                window.location.href = "/login";
            }
        };
    }

    if (homeButton) {
        homeButton.onclick = function() {
            window.location.href = "/home";
        };
    }
});
