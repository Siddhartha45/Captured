(function () {
  'use strict';

  const lbActions   = document.getElementById('lbActions');
  const lbEditBtn   = document.getElementById('lbEditBtn');
  const lbDeleteBtn = document.getElementById('lbDeleteBtn');

  // Track the delete URL of the currently open photo
  let pendingDeleteUrl = '';

  // ── Build confirmation popup once, reuse it ──
  const confirmBackdrop = document.createElement('div');
  confirmBackdrop.className = 'confirm-backdrop';
  confirmBackdrop.innerHTML = `
    <div class="confirm-box">
      <button class="confirm-close" aria-label="Close">✕</button>
      <h3 class="confirm-title">Delete Photo</h3>
      <p class="confirm-message">Are you sure you want to delete this photo? This action cannot be undone.</p>
      <div class="confirm-actions">
        <button class="btn btn-ghost" id="confirmNo">No, keep it</button>
        <a href="#" class="btn btn-danger btn-sm" id="confirmYes">Yes, delete</a>
      </div>
    </div>
  `;
  document.body.appendChild(confirmBackdrop);

  const confirmYes   = document.getElementById('confirmYes');
  const confirmNo    = document.getElementById('confirmNo');
  const confirmClose = confirmBackdrop.querySelector('.confirm-close');

  function openConfirm() {
    confirmBackdrop.classList.add('active');
    confirmYes.href = pendingDeleteUrl;
  }

  function closeConfirm() {
    confirmBackdrop.classList.remove('active');
  }

  confirmNo.addEventListener('click', closeConfirm);
  confirmClose.addEventListener('click', closeConfirm);

  // Close on backdrop click
  confirmBackdrop.addEventListener('click', function (e) {
    if (e.target === confirmBackdrop) closeConfirm();
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && confirmBackdrop.classList.contains('active')) {
      closeConfirm();
    }
  });

  // ── Card click — show/hide owner actions ──
  const cards = document.querySelectorAll('.photo-card');

  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      const isOwner   = card.dataset.isOwner === 'true';
      const editUrl   = card.dataset.editUrl;
      const deleteUrl = card.dataset.deleteUrl;

      if (isOwner) {
        lbActions.classList.remove('hidden');
        lbEditBtn.href = editUrl;

        // Store delete URL but don't assign it to the button directly
        pendingDeleteUrl = deleteUrl;

        // Intercept delete button click to show confirmation first
        lbDeleteBtn.onclick = function (e) {
          e.preventDefault();
          openConfirm();
        };
      } else {
        lbActions.classList.add('hidden');
      }
    });
  });

})();