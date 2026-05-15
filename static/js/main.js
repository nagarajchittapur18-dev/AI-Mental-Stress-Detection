/**
 * MindWell AI — Main JavaScript
 * Handles counters, password toggles, animations
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─────────────────────────────────────
    // Counter Animation (Landing Page)
    // ─────────────────────────────────────
    const counters = document.querySelectorAll('.counter');
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.target);
                    animateCounter(el, target);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(c => observer.observe(c));
    }

    function animateCounter(el, target) {
        let current = 0;
        const step = Math.ceil(target / 40);
        const interval = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            el.textContent = current;
        }, 30);
    }

    // ─────────────────────────────────────
    // Active Nav Link Highlighting
    // ─────────────────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.style.color = '#fff';
            link.style.background = 'rgba(255,255,255,0.08)';
        }
    });

    // ─────────────────────────────────────
    // Auto-dismiss Flash Messages
    // ─────────────────────────────────────
    const alerts = document.querySelectorAll('.glass-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

    // ─────────────────────────────────────
    // Scroll Reveal Animation
    // ─────────────────────────────────────
    const revealElements = document.querySelectorAll('.glass-card, .feature-card, .stat-card');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        revealObserver.observe(el);
    });
});

// ─────────────────────────────────────
// Password Toggle (Global Function)
// ─────────────────────────────────────
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const eye = document.getElementById(fieldId + '-eye');
    if (field.type === 'password') {
        field.type = 'text';
        if (eye) { eye.classList.remove('fa-eye'); eye.classList.add('fa-eye-slash'); }
    } else {
        field.type = 'password';
        if (eye) { eye.classList.remove('fa-eye-slash'); eye.classList.add('fa-eye'); }
    }
}
