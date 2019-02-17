function build_navbar() {   
    nav_items = document.getElementById('nav-items');
    acct_ctr = document.getElementById('acct-ctr');

    home = document.createElement('li');
    home.className="nav-item"
    home_a = document.createElement('a');
    home_a.className = 'nav-link';
    home_a.setAttribute('href', 'index.html');
    home_a.appendChild(document.createTextNode('Home'));
    home.appendChild(home_a);
    nav_items.appendChild(home);
    
    if (is_logged_in() == false) {
        login = document.createElement('li');
        login.className="nav-item"
        login_a = document.createElement('a');
        login_a.className = 'nav-link';
        login_a.setAttribute('href', 'login.html');
        login_a.appendChild(document.createTextNode('Login'));
        login.appendChild(login_a)
        acct_ctr.appendChild(login)

        register = document.createElement('li');
        register.className="nav-item"
        register_a = document.createElement('a');
        register_a.className = 'nav-link';
        register_a.setAttribute('href', 'register.html');
        register_a.appendChild(document.createTextNode('Register'));
        register.appendChild(register_a);
        acct_ctr.appendChild(register);

    } else {
        acct_ctr = document.getElementById('acct-ctr');

        sign_out = document.createElement('li');
        sign_out.className="nav-item"
        sign_out_a = document.createElement('a');
        sign_out_a.className = 'nav-link';
        sign_out_a.setAttribute('href', '#');
        sign_out_a.appendChild(document.createTextNode('Sign Out'));
        sign_out.appendChild(sign_out_a)
        acct_ctr.appendChild(sign_out)

        profile = document.createElement('li');
        profile.className="nav-item"
        profile_a = document.createElement('a');
        profile_a.className = 'nav-link';
        profile_a.setAttribute('href', 'profile.html');
        profile_a.appendChild(document.createTextNode('Profile'));
        profile.appendChild(profile_a);
        nav_items.appendChild(profile);

        sell = document.createElement('li');
        sell.className="nav-item"
        sell_a = document.createElement('a');
        sell_a.className = 'nav-link';
        sell_a.setAttribute('href', 'sell.html');
        sell_a.appendChild(document.createTextNode('Sell'));
        sell.appendChild(sell_a);
        nav_items.appendChild(sell);

        sign_out.addEventListener('click', e => logout(e, 'index.html'));
    }

    buy = document.createElement('li');
    buy.className="nav-item"
    buy_a = document.createElement('a');
    buy_a.className = 'nav-link';
    buy_a.setAttribute('href', 'buy.html');
    buy_a.appendChild(document.createTextNode('Buy'));
    buy.appendChild(buy_a);
    nav_items.appendChild(buy);
}