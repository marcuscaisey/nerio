/**
 * Display a notice by fading it in and then out after some time.
 * @param {string} message - The message to display.
 * @param {...string} extraClasses - Extra classes to add to the notice div.
 * @returns {Promise<void>} A promise which resolves when then notice has faded.
 */
async function displayNotice(message, ...extraClasses) {
  const notice = createNotice(message, ...extraClasses);

  const notices = document.getElementById("notices");
  notices.insertBefore(notice, notices.firstChild);

  await fadeIn(notice, 500);
  await sleep(5000);
  await fadeOut(notice, 500);
  notice.remove();
}

/**
 * Create a new notice.
 * @param {string} message - The message to display.
 * @param {...string} extraClasses - Extra classes to add to the notice div.
 * @returns {HTMLDivElement} A new notice element.
 */
function createNotice(message, ...extraClasses) {
  const notice = document.createElement("div");
  notice.classList.add("notice", ...extraClasses);

  const deleteButton = document.createElement("button");
  deleteButton.classList.add("delete");
  deleteButton.addEventListener("click", () => notice.remove());

  notice.append(deleteButton, message);
  return notice;
}

/**
 * Fade a DOM element in or out.
 * @param {Element} element - The element to fade.
 * @param {number} duration - The number of ms the fade should take.
 * @param {number} direction - The direction of the fade: 1 for fade in, -1 for
 * fade out.
 * @returns {Promise<void>} A Promise which resolves once the element has
 * finished fading.
 */
function fade(element, duration, direction) {
  return new Promise(resolve => {
    const steps = 100;
    const increment = direction / steps;
    const interval = duration / steps;

    const initialOpacity = (1 - direction) / 2;
    element.style.opacity = initialOpacity;

    let intervalID = setInterval(() => {
      element.style.opacity = parseFloat(element.style.opacity) + increment;

      if (Math.abs(element.style.opacity - initialOpacity) >= 1) {
        clearInterval(intervalID);
        resolve();
      }
    }, interval);
  });
}

/**
 * Fade a DOM element in.
 * @param {Element} element - The element to fade.
 * @param {number} duration - The number of ms the fade should take.
 * @returns {Promise<void>} A Promise which resolves once the element has
 */
function fadeIn(element, duration) {
  return fade(element, duration, 1);
}

/**
 * Fade a DOM element in.
 * @param {Element} element - The element to fade.
 * @param {number} duration - The number of ms the fade should take.
 * @returns {Promise<void>} A Promise which resolves once the element has
 * finished fading.
 */
function fadeOut(element, duration) {
  return fade(element, duration, -1);
}

/**
 * Sleep for some time.
 * @param {number} duration - Number of milliseconds to sleep for.
 * @returns {Promise<void>} A Promise which resolves once the sleeping is done.
 */
function sleep(duration) {
  return new Promise(resolve => setTimeout(resolve, duration));
}

export {displayNotice};
