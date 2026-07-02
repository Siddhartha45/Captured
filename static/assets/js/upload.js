/* =============================================
   CAPTURED — upload.js
   Handles: image preview, drag-and-drop,
   char count, submit button enable/disable
   ============================================= */

(function () {
  'use strict';

  const picker         = document.getElementById('uploadPicker');
  const pickerEmpty    = document.getElementById('pickerEmpty');
  const pickerPreview  = document.getElementById('pickerPreview');
  const previewImg     = document.getElementById('previewImg');
  const previewChangeBtn = document.getElementById('previewChangeBtn');
  const imageInput     = document.getElementById('imageInput');
  const titleInput     = document.getElementById('title');
  const submitBtn      = document.getElementById('submitBtn');
  const textarea       = document.getElementById('description');
  const charCount      = document.getElementById('charCount');

  // ── Show image preview ──
  function showPreview(file) {
  if (!file) return;

  const isHeic = file.type === 'image/heic'
    || file.type === 'image/heif'
    || file.name.toLowerCase().endsWith('.heic')
    || file.name.toLowerCase().endsWith('.heif');

  if (isHeic) {
    // Show a loading state while converting
    picker.classList.add('has-image');
    previewImg.src = '';
    previewImg.alt = 'Converting...';

    heic2any({ blob: file, toType: 'image/jpeg', quality: 0.8 })
      .then(function (convertedBlob) {
        previewImg.src = URL.createObjectURL(convertedBlob);
        previewImg.alt = 'Preview';
      })
      .catch(function () {
        // Conversion failed — still accept the file, just no preview
        previewImg.alt = 'Preview unavailable';
      });
  } else if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImg.src = e.target.result;
      previewImg.alt = 'Preview';
      picker.classList.add('has-image');
    };
    reader.readAsDataURL(file);
  }
}

  // File input change
  imageInput.addEventListener('change', function () {
    if (imageInput.files && imageInput.files[0]) {
      showPreview(imageInput.files[0]);
    }
    checkSubmit();
  });

  // "Change photo" button — re-triggers the file input
  previewChangeBtn.addEventListener('click', function (e) {
    e.stopPropagation();
    imageInput.click();
  });

  // ── Drag and drop ──
  picker.addEventListener('dragover', function (e) {
    e.preventDefault();
    picker.classList.add('drag-over');
  });

  picker.addEventListener('dragleave', function () {
    picker.classList.remove('drag-over');
  });

  picker.addEventListener('drop', function (e) {
    e.preventDefault();
    picker.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file) {
      // Assign dropped file to the input so it gets submitted with the form
      const dt = new DataTransfer();
      dt.items.add(file);
      imageInput.files = dt.files;

      showPreview(file);
      checkSubmit();
    }
  });

  // ── Character counter for description ──
  if (textarea && charCount) {
    textarea.addEventListener('input', function () {
      const len = textarea.value.length;
      charCount.textContent = len + ' / 1000';

      if (len >= 900) {
        charCount.style.color = '#e07070';
      } else {
        charCount.style.color = '';
      }
    });
  }

  // ── Enable submit only when image + title are present ──
  function checkSubmit() {
    const hasImage = imageInput.files && imageInput.files.length > 0;
    const hasTitle = titleInput.value.trim().length > 0;
    submitBtn.disabled = !(hasImage && hasTitle);
  }

  titleInput.addEventListener('input', checkSubmit);

})();
