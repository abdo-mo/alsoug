document.addEventListener('DOMContentLoaded', function(){

    toggleButton = document.querySelector('.toggle-button')
    navMenu = document.querySelector('.nav-menu')

    toggleButton.onclick = () => {
        if (navMenu.style.display === 'none'){
            navMenu.style.display = 'flex';
        }
        else
        {
            navMenu.style.display = 'none';
        }
    }
});


