import {displayNotice} from "./utils.js";

/**
 * Navbar with a menu which appears on mobile when the burger icon is clicked.
 */
class Navbar {
  _burger = document.querySelector(".navbar-burger");
  _menu = document.querySelector(".navbar-menu");

  constructor() {
    this._burger.addEventListener("click", this._burgerHandler.bind(this));
  }

  /**
   * Toggles the menu and the burger icon.
   */
  _burgerHandler() {
    this._burger.classList.toggle("is-active");
    this._menu.classList.toggle("is-active");
  }
}

/**
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
