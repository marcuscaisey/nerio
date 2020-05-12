import {displayNotice} from "../utils.js";

/*
 * When the burger icon is clicked, the menu is shown/hidden.
 */
class Navbar {
  burger = document.querySelector(".navbar-burger");
  menu = document.querySelector(".navbar-menu");

  constructor() {
    this.burger.addEventListener("click", () => {
      this.burger.classList.toggle("is-active");
      this.menu.classList.toggle("is-active");
    });
  }
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

new Navbar();
displayMessages();
