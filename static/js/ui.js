/*
  Minimal UI enhancements for mobile navigation and accessible modals.
  Load this file with defer in base.html.
*/

const navToggle = document.getElementById('navToggle');
const mobileMenu = document.getElementById('mobile-menu');

if (navToggle && mobileMenu) {
  navToggle.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    mobileMenu.hidden = expanded;
  });
}

const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
const modals = document.querySelectorAll('[data-modal]');

modalTriggers.forEach(trigger => {
  const target = document.querySelector(trigger.dataset.modalTrigger);
  if (!target) return;

  trigger.addEventListener('click', event => {
    event.preventDefault();
    target.hidden = false;
    target.querySelector('[data-modal-close]')?.focus();
  });
});

modals.forEach(modal => {
  modal.addEventListener('click', event => {
    if (event.target === modal) {
      modal.hidden = true;
    }
  });

  modal.querySelectorAll('[data-modal-close]').forEach(close => {
    close.addEventListener('click', () => {
      modal.hidden = true;
    });
  });
});
