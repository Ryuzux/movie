
document.getElementById("register").onclick = function() {
    window.location.href = "/register";
};

document.getElementById("home").onclick = function() {
    window.location.href = "/admin";
};

document.getElementById("settings").onclick = function() {
    window.location.href = "/update/user";
};

document.getElementById("add-movie").onclick = function() {
    window.location.href = "/admin/add/movie";
};

document.getElementById("update-movie").onclick = function() {
    window.location.href = "/admin/update/movie";
};

document.getElementById("add-schedule").onclick = function() {
    window.location.href = "/admin/add/schedule";
};

document.getElementById("update-schedule").onclick = function() {
    window.location.href = "/admin/update/schedule";
};

document.getElementById("confirm-topup").onclick = function() {
    window.location.href = "/admin/confirm/topup";
};

document.getElementById("report").onclick = function() {
    window.location.href = "/admin/report";
};

document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.getElementById("login");
    const profileButton = document.getElementById("profile");
    const profileContainer = document.getElementById("profile-container");
    const registerButton = document.getElementById("register");
    const settingButton = document.getElementById("settings");
    const homeButton = document.getElementById("admin");
    const topupbutton = document.getElementById("topup");

    if (typeof sessionData !== 'undefined') {
        const isLoggedIn = sessionData.logged_in;

        function updateLoginButton() {
            if (isLoggedIn) {
                loginButton.textContent = "Logout";
                registerButton.style.display = "none";
                profileButton.style.display = "none";
                loginButton.onclick = function() {
                    fetch('/logout', { method: 'POST' })
                        .then(response => {
                            if (response.ok) {
                                window.location.href = "/admin";
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
            window.location.href = "/admin";
        };
    }
});
