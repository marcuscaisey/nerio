import {displayNotice} from "./utils.js";

/*
 * Box which displays all of the user's shortened urls in rows. Each row has a
 * copy/rename/delete button associated with each url. The copy button copies
 * the url to the user's clipboard and the rename/delete buttons open modals
 * for the user to interact with.
 */
class UrlsBox {
  _box = document.getElementById("urls");

  constructor() {
    this._box.addEventListener("click", this._copyHandler);
  }

  /*
   * Copy the the url associated with the clicked copy button to the clipboard.
   */
  async _copyHandler(event) {
    if (!event.target.classList.contains("copy-button")) {
      return;
    }

    const urlButtons = event.target.parentNode;
    const url = urlButtons.dataset.url;

    try {
      await navigator.clipboard.writeText(url);
    } catch (error) {
      console.log(error);
    }

    displayNotice("URL has been copied.", "is-success");
  }
}

new UrlsBox();
