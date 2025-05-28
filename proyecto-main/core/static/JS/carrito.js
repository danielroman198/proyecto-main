document.addEventListener('DOMContentLoaded', function() {
    const carritoDesplegable = document.getElementById('carrito-desplegable');
    const carritoTrigger = document.querySelector('.carrito-trigger');
    const mainContent = document.getElementById('main-content');

    if (carritoTrigger) {
        carritoTrigger.addEventListener('click', function(event) {
            event.preventDefault(); // Evitar que el enlace "#" haga scroll
            carritoDesplegable.classList.toggle('abierto');
            mainContent.classList.toggle('carrito-abierto');
        });
    }
    
    // Aquí podrías agregar la lógica para cargar dinámicamente
    // los items del carrito usando AJAX si es necesario.
});