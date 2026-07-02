/* =============================================
   CAPTURED — auth.js
   Handles: password visibility toggle
   ============================================= */

(function () {
  'use strict';

  // Toggle password visibility for all password fields
  document.querySelectorAll('.toggle-password').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = btn.closest('.input-wrap').querySelector('input');
      const isHidden = input.type === 'password';

      input.type = isHidden ? 'text' : 'password';

      // Swap icon — open eye vs closed eye
      btn.innerHTML = isHidden
        ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
            <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
            <line x1="1" y1="1" x2="23" y2="23"/>
           </svg>`
        : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
            <circle cx="12" cy="12" r="3"/>
           </svg>`;

      btn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
    });
  });

})();
