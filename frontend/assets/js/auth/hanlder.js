function userLoginRedirectHandler() {
    if (!ACCESS_TOKEN) {
        if (window.location.href == LOGIN_FRONTEND_URL) {
        } else {
            window.location.href = LOGIN_FRONTEND_URL;
        }
    }
}

userLoginRedirectHandler();