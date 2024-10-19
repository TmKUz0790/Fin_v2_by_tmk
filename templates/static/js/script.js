document.querySelectorAll('.bar').forEach((bar) => {
  let value = bar.getAttribute('data-value');
  bar.style.height = `${value}%`;
});
