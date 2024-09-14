// Offcanvas Menu
const hamburger = document.getElementById("hamburger");
const offcanvas = document.getElementById("offcanvas");
const closeBtn = document.getElementById("close-btn");

if (hamburger && offcanvas && closeBtn) {
  hamburger.addEventListener("click", () => {
    offcanvas.classList.add("open");
  });

  closeBtn.addEventListener("click", () => {
    offcanvas.classList.remove("open");
  });

  document.addEventListener("click", (event) => {
    if (
      !offcanvas.contains(event.target) &&
      !hamburger.contains(event.target)
    ) {
      offcanvas.classList.remove("open");
    }
  });
}

// Typewriting Effect
const text = "Welcome To TEKNE CLUB";
const speed = 60;

function typeWriter(element, text, speed) {
  if (element) {
    let index = 0;
    function type() {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    }
    type();
  }
}

const textElement = document.getElementById("typewriter-text");
typeWriter(textElement, text, speed);
