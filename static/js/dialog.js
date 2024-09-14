var openBtns = document.querySelectorAll(".openDialogBtn");

var closeBtns = document.querySelectorAll(".dialog-close");

function openDialog(dialogId) {
  var dialog = document.getElementById(dialogId);
  if (dialog) {
    dialog.style.display = "block";
  }
}

function closeDialog(dialog) {
  if (dialog) {
    dialog.style.display = "none";
  }
}

openBtns.forEach(function (button) {
  button.addEventListener("click", function () {
    var targetId = this.getAttribute("data-target");
    openDialog(targetId);
  });
});

closeBtns.forEach(function (button) {
  button.addEventListener("click", function () {
    var dialog = this.closest(".dialog");
    closeDialog(dialog);
  });
});

window.addEventListener("click", function (event) {
  if (event.target.classList.contains("dialog")) {
    closeDialog(event.target);
  }
});
