document.addEventListener('DOMContentLoaded', function() {
  // Get all "navbar-burger" elements
  var $navbarBurgers = Array.prototype.slice.call(
      document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {
    // Make each of them function
    $navbarBurgers.forEach(function($el) {
      // Get the target from the "data-target" attribute
      const $target = document.getElementById($el.dataset.target);

      // If target is main nav, add highlight
      if ($target.id == 'mainNav') {
        var bodyId = document.body.id.toString();
        bodyId = bodyId.substring(0, bodyId.length - 5);
        document.getElementById(bodyId).classList.add('is-active')
      }

      // Add a click event
      $el.addEventListener('click', function() {
        // Toggle "navbar-burger" and "navbar-menu"
        $el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });

      $el.addEventListener('onfocus', function () {
        // Toggle "navbar-burger" and "navbar-menu"
        $el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });
    });
  }
});
