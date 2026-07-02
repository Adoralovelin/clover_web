(function () {
    'use strict';

    const PAGES = {
        home: 'index.html',
        gallery: 'gallery.html',
        diy: 'diy.html',
        about: 'about.html'
    };

    // --- Page transition overlay ---
    function createTransitionOverlay() {
        let overlay = document.querySelector('.page-transition');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'page-transition';
            overlay.setAttribute('aria-hidden', 'true');
            document.body.prepend(overlay);
        }
        return overlay;
    }

    function playPageEnter() {
        document.body.classList.remove('page-loading');
        const overlay = document.querySelector('.page-transition');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }

    // --- Page enter animation on load (links navigate normally) ---
    function initPageTransitions() {
        createTransitionOverlay();
        playPageEnter();
    }

    // --- Scroll reveal ---
    function initScrollReveal() {
        const targets = document.querySelectorAll('[data-animate], [data-stagger]');
        if (!targets.length) return;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
        );

        targets.forEach(el => observer.observe(el));
    }

    // --- Sticky nav shrink ---
    function initNavScroll() {
        const nav = document.querySelector('[data-nav]');
        if (!nav) return;

        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    if (window.scrollY > 20) {
                        nav.classList.add('py-2', 'shadow-2xl');
                        nav.classList.remove('py-4');
                    } else {
                        nav.classList.add('py-4');
                        nav.classList.remove('py-2', 'shadow-2xl');
                    }
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    // --- Mobile menu ---
    function initMobileMenu() {
        const toggle = document.querySelector('[data-menu-toggle]');
        const menu = document.querySelector('[data-mobile-menu]');
        const close = document.querySelector('[data-menu-close]');
        if (!toggle || !menu) return;

        const open = () => {
            menu.classList.add('open');
            document.body.style.overflow = 'hidden';
        };
        const shut = () => {
            menu.classList.remove('open');
            document.body.style.overflow = '';
        };

        toggle.addEventListener('click', open);
        close?.addEventListener('click', shut);
        menu.querySelectorAll('a').forEach(a => a.addEventListener('click', shut));
    }

    // --- Paint stroke animation on scroll ---
    function initPaintStrokes() {
        const fills = document.querySelectorAll('.paint-stroke-fill[data-width]');
        if (!fills.length) return;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const fill = entry.target;
                        fill.style.width = fill.dataset.width;
                        observer.unobserve(fill);
                    }
                });
            },
            { threshold: 0.5 }
        );

        fills.forEach(fill => {
            fill.style.width = '0%';
            observer.observe(fill);
        });
    }

    // --- Gallery card random tilt ---
    function initGalleryTilt() {
        document.querySelectorAll('.art-frame[data-random-tilt]').forEach(card => {
            const randomRotate = (Math.random() * 4 - 2).toFixed(1);
            card.style.transform = `rotate(${randomRotate}deg)`;
        });
    }

    // --- Hand-drawn card hover ---
    function initHandDrawnCards() {
        document.querySelectorAll('.hand-drawn-border[data-hover-tilt]').forEach(card => {
            const initial = card.dataset.initialRotate || '0deg';
            card.addEventListener('mouseenter', () => {
                const deg = (Math.random() * 4 - 2).toFixed(1);
                card.style.transform = `rotate(${deg}deg) scale(1.02)`;
                card.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = `rotate(${initial}) scale(1)`;
            });
        });
    }

    // --- Gallery filter buttons ---
    function initGalleryFilters() {
        const buttons = document.querySelectorAll('[data-filter]');
        const items = document.querySelectorAll('[data-category]');
        const comicSection = document.querySelector('[data-comic-storyline]');
        const craftsSection = document.querySelector('[data-crafts-section]');
        if (!buttons.length || !items.length) return;

        const applyFilter = (filter) => {
            buttons.forEach(b => {
                b.classList.remove('opacity-100', 'ring-2', 'ring-primary');
                b.classList.add('opacity-70');
            });
            const activeBtn = document.querySelector(`[data-filter="${filter}"]`);
            activeBtn?.classList.add('opacity-100', 'ring-2', 'ring-primary');
            activeBtn?.classList.remove('opacity-70');

            if (comicSection) {
                const showComics = filter === 'all' || filter === 'comics';
                comicSection.style.display = showComics ? '' : 'none';
            }
            if (craftsSection) {
                const showCraftsSection = filter === 'all' || filter === 'crafts' || filter === 'characters';
                craftsSection.style.display = showCraftsSection ? '' : 'none';
            }

            items.forEach(item => {
                const category = item.dataset.category;
                let show = filter === 'all';
                if (filter === 'comics') show = category === 'comics';
                if (filter === 'crafts') show = category === 'crafts';
                if (filter === 'characters') show = category === 'characters';

                item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                if (show) {
                    item.style.opacity = '1';
                    item.style.transform = 'scale(1)';
                    item.style.pointerEvents = 'auto';
                    item.style.display = '';
                } else {
                    item.style.opacity = '0.3';
                    item.style.transform = 'scale(0.95)';
                    item.style.pointerEvents = 'none';
                    if (filter !== 'all') item.style.display = 'none';
                }
            });
        };

        buttons.forEach(btn => {
            btn.addEventListener('click', () => applyFilter(btn.dataset.filter));
        });
    }

    // --- Parallax pins (DIY page) ---
    function initParallaxPins() {
        const pins = document.querySelectorAll('[data-parallax-pin]');
        if (!pins.length) return;

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            pins.forEach((pin, index) => {
                const speed = 0.05 * (index + 1);
                pin.style.transform = `translateY(${scrolled * speed}px)`;
            });
        }, { passive: true });
    }

    // --- Active nav highlight ---
    function highlightActiveNav() {
        const current = document.body.dataset.page;
        if (!current) return;
        document.querySelectorAll(`[data-nav-link="${current}"]`).forEach(link => {
            link.classList.add('active');
        });
    }

    // --- Init ---
    document.addEventListener('DOMContentLoaded', () => {
        initPageTransitions();
        initScrollReveal();
        initNavScroll();
        initMobileMenu();
        initPaintStrokes();
        initGalleryTilt();
        initHandDrawnCards();
        initGalleryFilters();
        initParallaxPins();
        highlightActiveNav();
    });
})();
