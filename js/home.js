import {displayNotice} from "./utils.js";

/**
 * Box which displays all of the user's shortened urls in rows.
 */
class UrlsBox {
  _box = document.querySelector("#urls");

  /**
   * @param {function} RenameModal - The class of the rename modal to be opened
   * when a rename button is clicked.
   * @param {function} DeleteModal - The class of the delete modal to be
   * opened when a delete button is clicked.
   */
  constructor(RenameModal, DeleteModal) {
    this._renameModal = new RenameModal();
    this._deleteModal = new DeleteModal();

    this._box.addEventListener("click", this._copyHandler);
    this._box.addEventListener("click", this._renameHandler.bind(this));
    this._box.addEventListener("click", this._deleteHandler.bind(this));
  }

  /**
   * Copy the the url associated with the clicked copy button to the clipboard.
   * @param {MouseEvent} event - The click event.
   * @private
   */
  async _copyHandler(event) {
    if (!event.target.classList.contains("copy-button")) {
      return;
    }

    const urlRow = UrlRow.fromChild(event.target);

    try {
      await navigator.clipboard.writeText(urlRow.dataset.url);
    } catch (error) {
      console.log(error);
    }

    displayNotice("URL has been copied.", "is-success");
  }

  /**
   * Open the rename modal.
   * @param {MouseEvent} event - The click event.
   * @private
   */
  _renameHandler(event) {
    if (event.target.classList.contains("rename-button")) {
      const urlRow = UrlRow.fromChild(event.target);
      this._renameModal.open(urlRow);
    }
  }

  /**
   * Open the delete modal.
   * @param {MouseEvent} event - The click event.
   * @private
   */
  _deleteHandler(event) {
    if (event.target.classList.contains("delete-button")) {
      const urlRow = UrlRow.fromChild(event.target);
      this._deleteModal.open(urlRow);
    }
  }
}

/**
 * A row in the urls box which contains information about a url and the
 * copy/rename/delete buttons associated with it.
 */
class UrlRow {
  /**
   * @param {HTMLElement} div - The url-row div.
   */
  constructor(div) {
    this._url = div.querySelector(".url");
    this.dataset = div.dataset;
  }

  /**
   * Instantiate a url row from one of its child elements.
   * @param {HTMLElement} child - A child element of the url row.
   * @returns {UrlRow} A UrlRow object.
   */
  static fromChild(child) {
    let current = child;
    while (!current.classList.contains("url-row")) {
      current = current.parentNode;
    }
    return new UrlRow(current);
  }

  /**
   * Set the url associated with this row.
   * @param {string} value
   */
  set url(value) {
    this._url.textContent = value;
    this._url.href = value;
    this.dataset.url = value;
  }
}

/**
 * Modal which can be closed by clicking either the close button or the
 * background.
 */
class Modal {
  /**
   * @param {string} id - The ID of the modal div element.
   */
  constructor(id) {
    this._div = document.getElementById(id);
    this._background = this._div.querySelector(".modal-background");
    this._closeButton = this._div.querySelector(".modal-close");

    this._background.addEventListener("click", this.close.bind(this));
    this._closeButton.addEventListener("click", this.close.bind(this));
    document.addEventListener("keydown", this._escapeHandler.bind(this));
  }

  /**
   * Close the modal when the escape key is pressed.
   * @param {KeyboardEvent} event - Keydown event.
   * @private
   */
  _escapeHandler(event) {
    if (event.code === "Escape") {
      this.close();
    }
  }

  /**
   * Whether the modal is open or not.
   * @returns {boolean} true or false.
   */
  get isOpen() {
    return this._div.classList.contains("is-active");
  }

  /**
   * Open the modal.
   */
  open() {
    this._div.classList.add("is-active");
  }

  /**
   * Close the modal.
   */
  close() {
    this._div.classList.remove("is-active");
  }
}

/**
 * Rename modal which has an input for a user to submit a new name for their
 * url.
 */
class RenameModal extends Modal {
  _input = document.querySelector("#rename-input");
  _help = document.querySelector("#rename-help");
  _confirmButton = document.querySelector("#rename-confirm-button");

  constructor() {
    super("rename-modal");
    this._urlRow = null;
    this._helpText = this._help.textContent;

    this._confirmButton.addEventListener("click", this._confirmHandler.bind(this));
    document.addEventListener("keydown", this._enterHandler.bind(this));
  }

  /**
   * Open the modal and associate it with the url row who's rename button was
   * clicked.
   * @param {UrlRow} urlRow - Row which contains the clicked rename button.
   */
  open(urlRow) {
    this._urlRow = urlRow;
    this._input.value = "";
    this._input.placeholder = urlRow.dataset.name;
    this._resetHelpText();
    super.open();
    this._input.focus();
  }

  /**
   * Send a PATCH request to the modify endpoint. If the request is successful,
   * close the modal and change the url in the associated row. If not, set the
   * error message to the one received in the response.
   */
  async _confirmHandler() {
    let response;
    try {
      response = await fetch(this._urlRow.dataset.endpoint, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken(),
        },
        body: JSON.stringify({
          name: this._input.value,
        }),
      });

    } catch (error) {
      console.log(error);
      return;
    }

    const json = await response.json();
    if (json.error) {
      this._error = json.error;

    } else {
      this._urlRow.url = json.url;
      this._urlRow.dataset.name = json.name;
      this.close();
      displayNotice("URL has been renamed.", "is-success");
    }
  }

  /**
   * Submit the new url name if enter is pressed.
   * @param {KeyboardEvent} event - Keydown event.
   * @private
   */
  _enterHandler(event) {
    if (event.key === "Enter" && this.isOpen) {
      this._confirmHandler();
    }
  }

  /**
   * Set the error message.
   * @param {string} value
   * @private
   */
  set _error(value) {
    this._help.textContent = value;
    this._help.classList.add("is-danger");
  }

  /**
   * Reset the help text to its original state.
   * @private
   */
  _resetHelpText() {
    this._help.textContent = this._helpText;
    this._help.classList.remove("is-danger");
  }
}

/**
 * Delete modal which asks the user to confirm that they want to delete a their
 * url.
 */
class DeleteModal extends Modal {
  _confirmButton = document.querySelector("#delete-confirm-button");
  _cancelButton = document.querySelector("#delete-cancel-button");
  _url = document.querySelector("#delete-url");

  constructor() {
    super("delete-modal");
    this._urlRow = null;

    this._confirmButton.addEventListener("click", this._confirmHandler.bind(this));
    this._cancelButton.addEventListener("click", this.close.bind(this));
    document.addEventListener("keydown", this._enterHandler.bind(this));
  }

  /**
   * Open the modal and associate it with the url row who's delete button was
   * clicked.
   * @param {UrlRow} urlRow - Row which contains the clicked delete button.
   */
  open(urlRow) {
    this._urlRow = urlRow;
    this._url.textContent = urlRow.dataset.url;
    this._url.href = urlRow.dataset.url;
    super.open();
  }

  /**
   * Send a DELETE request to the modify endpoint. If the request is successful,
   * close the modal and delete the url box from the page. If not, display the
   * error message in a notice.
   */
  async _confirmHandler() {
    let response;
    try {
      response = await fetch(this._urlRow.dataset.endpoint, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken(),
        },
      });

    } catch (error) {
      console.log(error);
      return;
    }

    const json = await response.json();
    if (json.error) {
      displayNotice(json.error, "is-danger");

    } else {
      location.reload();
    }

    this.close();
  }

  /**
   * Delete the url if enter is pressed.
   * @param {KeyboardEvent} event - Keydown event.
   * @private
   */
  _enterHandler(event) {
    if (event.key === "Enter" && this.isOpen) {
      this._confirmHandler();
    }
  }
}

/**
 * Return the value of the user's csrf token cookie.
 * @returns {string} A csrf token.
 */
function csrfToken() {
  const cookies = document.cookie.split(";");
  for (const [key, value] of cookies.map(c => c.split("="))) {
    if (key === "csrftoken") {
      return value;
    }
  }
}

if (document.querySelector("#urls")) {
  new UrlsBox(RenameModal, DeleteModal);
}
