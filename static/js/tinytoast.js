class TinyToast {
  constructor() {
    this.tinytoastContainer = document.createElement("div");
    this.tinytoastContainer.className = "tinytoast-container";
    document.body.appendChild(this.tinytoastContainer);
  }

  show(message, type = "info") {
    const tinytoast = document.createElement("div");
    tinytoast.className = `tinytoast ${type}`;

    const messageDiv = document.createElement("div");
    messageDiv.className = "toast-message";
    messageDiv.textContent = message;

    tinytoast.appendChild(messageDiv);

    tinytoast.addEventListener("click", () => {
      this.hideToast(tinytoast);
    });

    this.tinytoastContainer.appendChild(tinytoast);

    const timer = document.createElement("div");
    timer.className = "timer timer-animation";
    tinytoast.appendChild(timer);

    tinytoast.style.animation = "slide-in 0.3s forwards";

    setTimeout(() => {
      if (tinytoast.parentElement) {
        this.hideToast(tinytoast);
      }
    }, 4000);
  }

  hideToast(toast) {
    toast.style.animation = "fade-out 0.3s forwards";
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, 300);
  }

  success(message) {
    this.show(message, "success");
  }

  error(message) {
    this.show(message, "error");
  }

  info(message) {
    this.show(message, "info");
  }

  warning(message) {
    this.show(message, "warning");
  }

  debug(message) {
    this.show(message, "debug");
  }
}
