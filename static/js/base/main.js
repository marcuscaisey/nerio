import {displayNotice} from "../utils.js";

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

/*
 * Display the messages passed to the template.
 */
function displayMessages() {
  const messagesJSON = document.getElementById("messages").textContent;
  const messages = JSON.parse(messagesJSON);

  for (const message of messages) {
    displayNotice(message.message, message.level_tag);
  }
}

setupNavbarBurger();
displayMessages();
