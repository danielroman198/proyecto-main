document.addEventListener('DOMContentLoaded', function() {
    const carritoDesplegable = document.getElementById('carrito-desplegable');
    const carritoTrigger = document.querySelector('.carrito-trigger');
    const mainContent = document.getElementById('main-content'); // Asegúrate de que este ID exista en tu HTML

    if (carritoTrigger && carritoDesplegable && mainContent) { // Añade mainContent a la verificación
        carritoTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Evitar que el enlace "#" haga scroll
            carritoDesplegable.classList.toggle('abierto');
            mainContent.classList.toggle('carrito-abierto');
        });
    }
});