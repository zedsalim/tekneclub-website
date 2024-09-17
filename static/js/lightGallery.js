document.addEventListener("DOMContentLoaded", () => {
  const lightSliderImages = document.querySelector(".lightSlider-images");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");

  if (!lightSliderImages || !prevBtn || !nextBtn) return;

  const images = lightSliderImages.querySelectorAll("img");

  if (images.length === 0) return;

  let index = 0;

  function updateLightSlider() {
    const offset = -index * 100;
    lightSliderImages.style.transform = `translateX(${offset}%)`;
  }

  nextBtn.addEventListener("click", () => {
    index = (index + 1) % images.length;
    updateLightSlider();
  });

  prevBtn.addEventListener("click", () => {
    index = (index - 1 + images.length) % images.length;
    updateLightSlider();
  });
});
