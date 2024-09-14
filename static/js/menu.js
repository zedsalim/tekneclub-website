document.addEventListener("DOMContentLoaded", () => {
  const userMenuButton = document.getElementById("user-menu-btn");
  const userMenu = document.getElementById("user-menu");

  if (userMenuButton && userMenu) {
    userMenuButton.addEventListener("click", () => {
      userMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", (event) => {
      if (
        !userMenuButton.contains(event.target) &&
        !userMenu.contains(event.target)
      ) {
        userMenu.classList.add("hidden");
      }
    });
  }
});
