class MessageNotif {
  constructor() {
    this.toast = document.getElementById("msg-notif-toast");
    this.messageElement = document.getElementById("msg-notif-toast-message");
    this.closeButton = document.getElementById("msg-close-notif");

    if (this.toast && this.messageElement && this.closeButton) {
      this.closeButton.addEventListener("click", () => {
        this.closeToast();
      });
    }
  }

  notify(message, delay = 1000) {
    if (this.toast && this.messageElement) {
      setTimeout(() => {
        this.messageElement.textContent = message;
        this.toast.classList.remove("slide-out-notif");
        this.toast.classList.add("show-message-notif");
      }, delay);
    }
  }

  closeToast() {
    if (this.toast) {
      this.toast.classList.remove("show-message-notif");
      this.toast.classList.add("slide-out-notif");
    }
  }
}
