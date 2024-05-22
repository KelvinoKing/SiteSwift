// Hamburger Menu

document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger-menu");
  const mainMenu = document.getElementById("main-menu");

  hamburger.addEventListener("click", (event) => {
    event.stopPropagation();
    mainMenu.classList.toggle("active");
  });

  // Close the menu when clicking outside
  document.addEventListener("click", (event) => {
    if (!hamburger.contains(event.target) && !mainMenu.contains(event.target)) {
      mainMenu.classList.remove("active");
    }
  });
});

//Slider

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

//Admin
// main.js

function openSidebar() {
  document.getElementById("sidebar").classList.add("open");
}

function closeSidebar() {
  document.getElementById("sidebar").classList.remove("open");
}
