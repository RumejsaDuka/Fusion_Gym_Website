/* ============================================================
   PLAN NAME UPDATE — jashtë DOMContentLoaded
   ============================================================ */
function updatePlanName(title) {
  const badge = document.querySelector('#planModal .text-danger.fw-bold');
  if (badge) badge.textContent = 'Paketa: ' + title;
  const input = document.querySelector('input[name="paketa"]');
  if (input) input.value = title;
}

document.addEventListener('DOMContentLoaded', function () {

  /* ── Register Modal (index.html) ── */
  const registrationForm = document.getElementById('registrationForm');
  if (registrationForm) {
    registrationForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;

      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(json => {
        if (json.status === 'success') {
          // Mbyll cilindo modal që është hapur
          ['registerModal', 'planModal'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
              const instance = bootstrap.Modal.getInstance(el);
              if (instance) instance.hide();
            }
          });

          const paketa = document.querySelector('input[name="paketa"]');
          document.getElementById('successMsg').textContent = paketa && paketa.value
            ? 'Regjistrimi për paketën "' + paketa.value + '" u krye me sukses! Do ju kontaktojmë së shpejti.'
            : 'Regjistrimi u krye me sukses! Do ju kontaktojmë së shpejti.';

          new bootstrap.Modal(document.getElementById('successModal')).show();
          registrationForm.reset();
        }
      })
      .catch(err => console.error(err))
      .finally(() => { if (btn) btn.disabled = false; });
    });
  }

  /* ── Review Modal (index.html) ── */
  const reviewForm = document.getElementById('reviewForm');
  if (reviewForm) {
    reviewForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;

      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(json => {
        if (json.status === 'success') {
          bootstrap.Modal.getInstance(document.getElementById('reviewModal')).hide();
          document.getElementById('successMsg').textContent =
            'Review-i juaj u dërgua! Do aprovohet nga admini së shpejti.';
          new bootstrap.Modal(document.getElementById('successModal')).show();
          reviewForm.reset();
        }
      })
      .catch(err => console.error(err))
      .finally(() => { if (btn) btn.disabled = false; });
    });
  }

  /* ── Contact Footer ── */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = this.querySelector('button[type="submit"]');
      if (btn) btn.disabled = true;

      fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(json => {
        if (json.status === 'success') {
          new bootstrap.Modal(document.getElementById('contactSuccessModal')).show();
          contactForm.reset();
        }
      })
      .catch(err => console.error(err))
      .finally(() => { if (btn) btn.disabled = false; });
    });
  }

});

// ============================================================
// UNIVERSAL FORM HANDLER — hap successModal pas çdo submit
// ============================================================
document.addEventListener('DOMContentLoaded', function () {

  function handleFormSubmit(form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const action = form.getAttribute('action') || window.location.href;

      fetch(action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // 1. Mbyll të gjithë modalet e hapura
          document.querySelectorAll('.modal.show').forEach(function (el) {
            bootstrap.Modal.getInstance(el)?.hide();
          });

          // 2. Vendos mesazhin
          var msg = document.getElementById('successMsg');
          if (msg) msg.textContent = data.msg || 'Faleminderit! Do ju kontaktojmë së shpejti.';

          // 3. Hap successModal
          setTimeout(function () {
            var el = document.getElementById('successModal');
            if (el) new bootstrap.Modal(el).show();
          }, 400);

          form.reset();
        }
      })
      .catch(err => console.error('Fetch error:', err));
    });
  }

  // ✅ Kap TË GJITHA format brenda çdo registerModal — me ose pa id
  document.querySelectorAll('#registerModal form, #planModal form, #reviewModal form, #contactForm').forEach(handleFormSubmit);

});