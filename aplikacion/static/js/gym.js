/* ============================================================
   FUSION GYM — gym.js
   ============================================================
   1. updatePlanName   → membership.html onclick
   2. showSuccessModal → helper global
   3. Universal Form Handler → të gjitha format
   4. FAQ accordion
   5. Navbar scroll effect
   ============================================================ */


/* ============================================================
   1. PLAN NAME UPDATE
   (thirret nga onclick në membership.html)
   ============================================================ */
function updatePlanName(title) {
  const badge = document.querySelector('#planModal .text-danger.fw-bold');
  if (badge) badge.textContent = 'Paketa: ' + title;
  const input = document.querySelector('input[name="paketa"]');
  if (input) input.value = title;
}


/* ============================================================
   2. HELPER — hap successModal me titull + mesazh dinamik
   ============================================================ */
function showSuccessModal(msg) {

  // Mbyll të gjitha modalet e hapura
  document.querySelectorAll('.modal.show').forEach(function (el) {
    const instance = bootstrap.Modal.getInstance(el);
    if (instance) instance.hide();
  });

  // Vendos titullin dinamik
  const title = document.getElementById('successTitle');
  if (title) {
    const m = (msg || '').toLowerCase();
    if (m.includes('review')) {
      title.textContent = 'Review u Dërgua!';
    } else if (m.includes('mesazh') || m.includes('kontakt')) {
      title.textContent = 'Mesazhi u Dërgua!';
    } else {
      title.textContent = 'Regjistrimi u Krye!';
    }
  }

  // Vendos mesazhin
  const msgEl = document.getElementById('successMsg');
  if (msgEl) msgEl.textContent = msg || '';

  // Hap successModal pas 400ms
  setTimeout(function () {
    const el = document.getElementById('successModal');
    if (el) new bootstrap.Modal(el).show();
  }, 400);
}


/* ============================================================
   3. UNIVERSAL FORM HANDLER
   Trajton: #registerModal form, #planModal form,
            #reviewModal form, #contactForm
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {

  function handleFormSubmit(form) {
    if (form.dataset.handlerAttached) return;
    form.dataset.handlerAttached = 'true';

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const btn = form.querySelector('button[type="submit"]');
      const originalHTML = btn ? btn.innerHTML : null;

      // Loading state
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Duke dërguar...';
      }

      const action = form.getAttribute('action') || window.location.href;

      fetch(action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(function (res) {
        if (!res.ok) throw new Error('Server error: ' + res.status);
        return res.json();
      })
      .then(function (data) {
        if (data.status === 'success') {
          showSuccessModal(data.msg);
          form.reset();
        } else {
          console.warn('Form error:', data.msg || 'E panjohur');
        }
      })
      .catch(function (err) {
        console.error('Fetch error:', err);
      })
      .finally(function () {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = originalHTML;
        }
      });
    });
  }

  document.querySelectorAll(
    '#registerModal form, #planModal form, #reviewModal form, #contactForm'
  ).forEach(handleFormSubmit);


  /* ============================================================
     4. FAQ ACCORDION
     ============================================================ */
  document.querySelectorAll('.sp-faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const id     = this.getAttribute('data-fid');
      const answer = document.getElementById(id);
      if (!answer) return;

      const isOpen = answer.classList.contains('open');

      document.querySelectorAll('.sp-faq-a').forEach(function (a) { a.classList.remove('open'); });
      document.querySelectorAll('.sp-faq-q').forEach(function (b) { b.classList.remove('active'); });

      if (!isOpen) {
        answer.classList.add('open');
        this.classList.add('active');
      }
    });
  });


  /* ============================================================
     5. NAVBAR SCROLL EFFECT
     ============================================================ */
  var navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
  }

});

/* ============================================================
     STAR RATING — #reviewModal
     Shto këtë bllok brenda DOMContentLoaded në fund të gym.js
     ============================================================ */
  const starBtns = document.querySelectorAll('#reviewModal .review-star-btn');
  const ratingInput = document.getElementById('ratingValue');
  if (starBtns.length && ratingInput) {
    let currentRating = 5;

    starBtns.forEach(function(btn) {
      btn.addEventListener('mouseenter', function() {
        const val = +this.dataset.val;
        starBtns.forEach(function(b) {
          b.classList.toggle('active', +b.dataset.val <= val);
        });
      });

      btn.addEventListener('click', function() {
        currentRating = +this.dataset.val;
        ratingInput.value = currentRating;
        starBtns.forEach(function(b) {
          b.classList.toggle('active', +b.dataset.val <= currentRating);
        });
      });
    });

    document.querySelector('#reviewModal .review-stars-input')
      .addEventListener('mouseleave', function() {
        starBtns.forEach(function(b) {
          b.classList.toggle('active', +b.dataset.val <= currentRating);
        });
      });
  }