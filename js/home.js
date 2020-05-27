import {displayNotice} from "./utils.js";

/*
 * Copy a URL to the clipboard when its copy button is clicked.
 */
function setupCopyButtons() {
  const box = document.getElementById("urls");

  box.addEventListener("click", async event => {
    if (!event.target.classList.contains("copy")) {
      return;
    }

    const button = event.target;
    const url = button.dataset.url;

    try {
      await navigator.clipboard.writeText(url);
    } catch (error) {
      console.log(error);
    }

    displayNotice("URL has been copied.", "is-success");
  });
}

setupCopyButtons();