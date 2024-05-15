let currentSlide = 0;
const slides = document.querySelectorAll(".single-slider");
const totalSlides = slides.length;

function showSlide(index) {
  slides.forEach((slide) => {
    slide.style.display = "none";
  });
  slides[index].style.display = "block";
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  showSlide(currentSlide);
}

function startSlider() {
  setInterval(nextSlide, 5000); // Change slide every 3 seconds (3000 milliseconds)
}

showSlide(currentSlide);
startSlider();
