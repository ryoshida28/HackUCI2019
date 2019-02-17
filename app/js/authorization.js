function is_logged_in() {
    cookies = parse_cookies(document.cookie);
    if (cookies.hasOwnProperty('token')) {
        postRequest('/account', cookies, res=> {
            console.log(res)
            if (res.success) {
                return res.object;
            } else {
                return false;
            }
        });
    } else {
        return false;
    }
}

function logout(e, redirect) {
    cookies = parse_cookies(document.cookie);
    postRequest('/logout', cookies, res => {
        console.log(res);
        if (res.success) {
            document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            window.location.assign(redirect);
        }
    });
}

function signin(email, password, redirect) {
    params = {
        email: email,
        password: password
    };
    postRequest('/login', params, res => {
        console.log(res)
        if (res.success) {
            document.cookie = 'token='+res.object.tokens[0].token+'; path=/';
            document.cookie = 'id='+res.object.id+'; path=/';
            window.location.assign(redirect);
        }
    });
}

function signup(first_name, last_name, email, birthdate, password, confirm_password, redirect) {
    params = {
        first_name: first_name,
        last_name: last_name,
        email: email,
        birthdate: birthdate,
        password: password,
        confirm_password: confirm_password
    };
    postRequest('/register', params, res => {
        if (res.success) {
            document.cookie = 'token='+res.object.tokens[0].token+'; path=/;';
            document.cookie = 'id='+res.object.id+'; path=/;';
            window.location.assign(redirect)
        }
    });
}