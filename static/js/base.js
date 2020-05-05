/*
 * Toggle the is-active class on the navbar burger and menu when the navbar
 * burger is clicked.
 */
function setupNavbarBurger() {
  const navbarBurger = document.querySelector(".navbar-burger");
  const navbarMenu = document.querySelector(".navbar-menu");
  navbarBurger.addEventListener("click", () => {
    navbarBurger.classList.toggle("is-active");
    navbarMenu.classList.toggle("is-active");
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupNavbarBurger);
} else {
  setupNavbarBurger();
}

