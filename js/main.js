/**
 * O Sopro de Sophia - main.js
 * JavaScript puro para interatividade, animações e efeitos visuais.
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initMobileMenu();
    initSmoothScroll();
    initScrollReveal();
    initActiveNavHighlight();
    initHeroParallax();
    initBookTiltEffect();
    initStarParticles();
    initBookLanguageTabs();
});

/**
 * 1. Efeito de scroll na navbar
 * Adiciona classe 'scrolled' quando rola mais de 50px
 */
function initNavbarScroll() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

/**
 * 2. Menu hamburger mobile
 * Toggle do menu e animação do ícone
 */
function initMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    if (!hamburger || !navMenu) return;

    const navLinks = navMenu.querySelectorAll('.nav-link');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Fecha o menu ao clicar num link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

/**
 * 3. Smooth scroll
 * Rolagem suave para links âncora com offset da navbar (80px)
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    const headerOffset = 80;

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (!targetElement) return;

            e.preventDefault();
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        });
    });
}

/**
 * 4. Scroll reveal
 * Intersection Observer para animar elementos com classe '.reveal'
 */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');
    if (reveals.length === 0) return;

    const observerOptions = {
        root: null,
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    reveals.forEach(reveal => {
        revealObserver.observe(reveal);
    });
}

/**
 * 5. Destaque do link ativo na navbar
 * Atualiza conforme a seção visível no scroll
 */
function initActiveNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    const headerOffset = 100;

    if (sections.length === 0 || navLinks.length === 0) return;

    window.addEventListener('scroll', () => {
        let currentSectionId = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - headerOffset) {
                currentSectionId = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSectionId}`) {
                link.classList.add('active');
            }
        });
    });
}

/**
 * 6. Parallax sutil no hero
 * Move o conteúdo e ajusta opacidade com base no scroll
 */
function initHeroParallax() {
    const heroContent = document.querySelector('.hero-content');
    const heroBgImg = document.querySelector('.hero-bg-img');

    if (!heroContent) return;

    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.scrollY;
                const vh = window.innerHeight;

                if (scrolled < vh) {
                    heroContent.style.transform = `translateY(${scrolled * 0.25}px)`;
                    heroContent.style.opacity = 1 - (scrolled / vh) * 1.2;

                    if (heroBgImg) {
                        heroBgImg.style.transform = `translateY(${scrolled * 0.15}px) scale(1.1)`;
                    }
                }
                ticking = false;
            });
            ticking = true;
        }
    });
}

/**
 * 7. Efeito tilt 3D nos cards de livros
 * Rotação baseada na posição do mouse
 */
function initBookTiltEffect() {
    const cards = document.querySelectorAll('.book-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -8;
            const rotateY = ((x - centerX) / centerX) * 8;

            card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            card.style.transition = 'transform 0.1s ease';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
            card.style.transition = 'transform 0.5s ease';
        });
    });
}

/**
 * 8. Partículas de estrelas no hero
 * Cria pontos de luz animados aleatoriamente
 */
function initStarParticles() {
    const heroStars = document.getElementById('heroStars');
    if (!heroStars) return;

    const count = 50;

    // Estilo do container
    heroStars.style.cssText = `
        position: absolute;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 1;
    `;

    const fragment = document.createDocumentFragment();

    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const size = Math.random() * 2.5 + 0.5;
        const duration = Math.random() * 3 + 2;
        const delay = Math.random() * 3;

        star.style.cssText = `
            position: absolute;
            left: ${x}%;
            top: ${y}%;
            width: ${size}px;
            height: ${size}px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            box-shadow: 0 0 ${size * 3}px rgba(255, 255, 255, 0.4);
            animation: starTwinkle ${duration}s ease-in-out ${delay}s infinite alternate;
            pointer-events: none;
        `;

        fragment.appendChild(star);
    }

    heroStars.appendChild(fragment);

    // Injeta keyframes se ainda não existir
    if (!document.getElementById('star-keyframes')) {
        const style = document.createElement('style');
        style.id = 'star-keyframes';
        style.textContent = `
            @keyframes starTwinkle {
                0% { opacity: 0.1; transform: scale(0.5); }
                100% { opacity: 1; transform: scale(1.2); }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * 9. Abas de idioma da biblioteca e tradução completa do site
 * Alterna a exibição dos livros e traduz todo o texto do site.
 */
function initBookLanguageTabs() {
    const tabs = document.querySelectorAll('.lang-tab');
    const tabContents = document.querySelectorAll('.books-tab-content');
    const navLangBtns = document.querySelectorAll('.lang-toggle .lang-btn');

    let currentLang = 'pt';

    function switchLanguage(targetLang) {
        currentLang = targetLang;

        // Atualiza abas da biblioteca
        tabs.forEach(t => {
            if (t.getAttribute('data-lang') === targetLang) {
                t.classList.add('active');
            } else {
                t.classList.remove('active');
            }
        });

        // Atualiza botões (bandeiras) da navbar
        navLangBtns.forEach(btn => {
            const btnLang = btn.getAttribute('data-lang');
            if (btnLang === targetLang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Atualiza exibição dos conteúdos de livros
        tabContents.forEach(content => {
            content.classList.remove('active');
            if (content.id === `tab-${targetLang}`) {
                content.classList.add('active');
            }
        });

        // Aplica traduções a todo o site
        if (typeof applyTranslations === 'function') {
            applyTranslations(targetLang);
        }

        // Re-inicializa efeito tilt nos novos cards visíveis
        initBookTiltEffect();
    }

    // Clique nas abas de livros
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetLang = tab.getAttribute('data-lang');
            switchLanguage(targetLang);
        });
    });

    // Clique nas bandeiras da navbar
    navLangBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const lang = btn.getAttribute('data-lang');
            if (['pt', 'es', 'en', 'fr', 'de', 'it'].includes(lang)) {
                switchLanguage(lang);
                // Não rola automaticamente para livros — apenas troca o idioma do site
            }
        });
    });
}
