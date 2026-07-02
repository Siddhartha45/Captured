/* =============================================
   CAPTURED — home.js
   Handles: navbar scroll, lightbox, mobile nav
   ============================================= */

(function () {
  'use strict';

  // ── Navbar: add .scrolled class on scroll ──
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', function () {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }, { passive: true });

  // ── Mobile hamburger ──
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
    });
  }

  // ── Lightbox ──
  const backdrop   = document.getElementById('lightboxBackdrop');
  const closeBtn   = document.getElementById('lightboxClose');
  const lbImg      = document.getElementById('lightboxImg');
  const lbTitle    = document.getElementById('lbTitle');
  const lbDesc     = document.getElementById('lbDescription');
  const lbUsername = document.getElementById('lbUsername');
  const lbAvatar   = document.getElementById('lbAvatar');
  const lbDate     = document.getElementById('lbDate');

  function openLightbox(card) {
    const data = card.dataset;

    lbImg.src        = data.image;
    lbImg.alt        = data.title;
    lbTitle.textContent    = data.title;
    lbUsername.textContent = '@' + data.user;
    lbAvatar.textContent   = data.user.charAt(0).toUpperCase();
    lbDate.textContent     = data.date || '';

    if (data.description && data.description.trim() !== '') {
      lbDesc.textContent = data.description;
      lbDesc.style.display = '';
    } else {
      lbDesc.textContent = 'No description provided.';
      lbDesc.style.color = 'var(--text-muted)';
      lbDesc.style.fontStyle = 'italic';
    }

    backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Focus trap: focus the close button
    setTimeout(function () { closeBtn.focus(); }, 50);
  }

  function closeLightbox() {
    backdrop.classList.remove('active');
    document.body.style.overflow = '';
    lbImg.src = ''; // free memory
  }

  // Attach click handlers to all photo cards
  const cards = document.querySelectorAll('.photo-card');
  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      openLightbox(card);
    });

    // Keyboard: Enter or Space opens lightbox
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(card);
      }
    });
  });

  // Close on button click
  if (closeBtn) {
    closeBtn.addEventListener('click', closeLightbox);
  }

  // Close on backdrop click (but not on inner content)
  if (backdrop) {
    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop) {
        closeLightbox();
      }
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && backdrop.classList.contains('active')) {
      closeLightbox();
    }
  });

})();
