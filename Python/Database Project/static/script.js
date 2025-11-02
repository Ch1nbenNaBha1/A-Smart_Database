document.addEventListener("DOMContentLoaded", () => {
  // Fade-in animations
  const fadeElems = document.querySelectorAll(".fade-in, .slide-up");
  fadeElems.forEach((el, i) => {
    setTimeout(() => el.classList.add("visible"), i * 100);
  });

  // Button ripple effect
  document.querySelectorAll("button, .btn").forEach(btn => {
    btn.addEventListener("click", e => {
      const ripple = document.createElement("span");
      ripple.classList.add("ripple");
      btn.appendChild(ripple);
      const rect = btn.getBoundingClientRect();
      ripple.style.left = `${e.clientX - rect.left}px`;
      ripple.style.top = `${e.clientY - rect.top}px`;
      setTimeout(() => ripple.remove(), 600);
    });
  });
});
