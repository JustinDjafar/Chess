const glow = document.getElementById('glow');

window.addEventListener('mousemove', (e) => {
  glow.style.left = e.clientX + 'px';
  glow.style.top = e.clientY + 'px';
});

const githubBtn = document.getElementById('github-btn');

githubBtn.addEventListener('click', () => {
  window.open('https://github.com/JustinDjafar', '_blank');
});

githubBtn.addEventListener('mouseenter', () => {
  githubBtn.style.transform = 'translate(-50%, -50%) scale(1.1)';
});

githubBtn.addEventListener('mouseleave', () => {
  githubBtn.style.transform = 'translate(-50%, -50%) scale(1)';
});
document.body.style.cursor = "url('cursor.png') 16 16, auto";
