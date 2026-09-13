document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.querySelector(".menu-toggle");
    const navMenu = document.querySelector(".nav-menu");
    const overlay = document.querySelector(".overlay");
    const factItems = document.querySelectorAll(".fact-item");
    const factResponse = document.querySelector(".fact-response");
    const heroVideo = document.querySelector("#hero-video");

    // Browsers block audible autoplay. Start muted, then enable audio after
    // the user's first interaction, which is an allowed playback gesture.
    if (heroVideo) {
        const startVideoAfterInteraction = () => {
            heroVideo.muted = false;
            heroVideo.volume = 1;
            heroVideo.play().catch(() => {
                // The visible controls remain available if autoplay is denied.
            });
            document.removeEventListener("pointerdown", startVideoAfterInteraction);
            document.removeEventListener("keydown", startVideoAfterInteraction);
        };

        document.addEventListener("pointerdown", startVideoAfterInteraction, { once: true });
        document.addEventListener("keydown", startVideoAfterInteraction, { once: true });
    }

    const factContent = {
        1: "It is okay to feel off. You may not have a clean explanation yet. Reaching for support is already a meaningful step.",
        2: "Putting a name to a feeling can make it less shapeless. Even saying 'I do not know yet' is a real starting point.",
        3: "You do not need to prove your pain before asking for help. Care is allowed before things feel extreme.",
        4: "Stress can show up through headaches, fatigue, restlessness, or shutdown. Your body is part of the story too.",
        5: "Not having the right words does not make the feeling less real. You can begin with a small clue and build from there.",
        6: "Reading, checking in, and trying one next step all count. Progress often looks quieter than people expect."
    };

    const closeMenu = () => {
        if (!menuToggle || !navMenu || !overlay) {
            return;
        }

        menuToggle.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
        navMenu.classList.remove("active");
        overlay.classList.remove("active");
        document.body.classList.remove("menu-open");
    };

    if (menuToggle && navMenu && overlay) {
        menuToggle.addEventListener("click", () => {
            const isOpen = navMenu.classList.toggle("active");
            menuToggle.classList.toggle("active", isOpen);
            menuToggle.setAttribute("aria-expanded", String(isOpen));
            overlay.classList.toggle("active", isOpen);
            document.body.classList.toggle("menu-open", isOpen);
        });

        overlay.addEventListener("click", closeMenu);
        navMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", closeMenu);
        });
    }

    factItems.forEach((item) => {
        item.addEventListener("click", () => {
            factItems.forEach((entry) => entry.classList.remove("selected"));
            item.classList.add("selected");

            if (factResponse) {
                factResponse.textContent = factContent[item.dataset.number] || "Support starts with noticing what feels true right now.";
            }
        });
    });
});
