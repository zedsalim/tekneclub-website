const slides = document.querySelector(".testimonial-slide");
const totalSlides = document.querySelectorAll(".testimonial-item").length;

if (slides && totalSlides > 0) {
  let currentIndex = 0;
  let slideInterval;

  const nextSlide = () => {
    currentIndex = (currentIndex + 1) % totalSlides;
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
  };

  const prevSlide = () => {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
  };

  const startSlideLoop = () => {
    slideInterval = setInterval(nextSlide, 3000);
  };

  const pauseSlideLoop = () => {
    clearInterval(slideInterval);
  };

  const nextBtn = document.getElementById("next-btn");
  const prevBtn = document.getElementById("prev-btn");

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      pauseSlideLoop();
      nextSlide();
      startSlideLoop();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      pauseSlideLoop();
      prevSlide();
      startSlideLoop();
    });
  }

  startSlideLoop();
}
