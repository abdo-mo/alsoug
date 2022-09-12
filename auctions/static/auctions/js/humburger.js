document.addEventListener('DOMContentLoaded', function(){

    toggleButton = document.querySelector('.toggle-button')
    navMenu = document.querySelector('.nav-menu')

    toggleButton.onclick = () => {
        if (navMenu.style.height === '0px'){
            navMenu.style.height = '270px';
        }
        else
        {
            navMenu.style.height = '0px';
        }
    }

    /* Styling humburger elements */

    /* The media query object */
    let x = window.matchMedia("(max-width: 900px)");

    /* The navlink element and it's classes */
    navlink = document.querySelectorAll('.navlink');
    loginLink = document.querySelector('#login-link');

    /* The function that removes unwanted classes when it's a humburger */
    function clear(x){

        navlinkClasses = navlink[0].classList;

        if (x.matches) {
            loginLink.style.display = 'block';
            if (navlinkClasses.length === 3) {
                for (let i = 0; i < navlink.length; i++) {
                    navlink[i].classList.remove('major-link', 'underline')
                }
            }
        }
        else {
            loginLink.style.display = 'none';
            if (navlinkClasses.length === 1) {
                for (let i = 0; i < navlink.length; i++) {
                    navlink[i].classList.add('major-link', 'underline')
                }
            }

        }
    }

    x.addEventListener('change', clear);

    clear(x);
});


