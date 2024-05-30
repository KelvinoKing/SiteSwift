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

document.addEventListener("DOMContentLoaded", function () {
  // Function to animate the counter
  function animateCounter(element, start, end, duration) {
    let startTime = null;

    function updateCounter(currentTime) {
      if (!startTime) startTime = currentTime;
      const progress = currentTime - startTime;
      const rate = Math.min(progress / duration, 1);
      const currentCount = Math.floor(rate * (end - start) + start);
      element.textContent = currentCount;

      if (rate < 1) {
        requestAnimationFrame(updateCounter);
      }
    }

    requestAnimationFrame(updateCounter);
  }

  // Function to start counter when the element comes into view
  function startCounters(entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const element = entry.target;
        const endValue = parseInt(element.textContent, 10);
        animateCounter(element, 0, endValue, 2000);
        observer.unobserve(element); // Stop observing once animation has started
      }
    });
  }

  // Set up the observer
  const observerOptions = {
    threshold: 0.5,
  };

  const observer = new IntersectionObserver(startCounters, observerOptions);

  // Observe elements with the data-toggle="counter-up" attribute
  const counters = document.querySelectorAll('[data-toggle="counter-up"]');
  counters.forEach((counter) => observer.observe(counter));
});
