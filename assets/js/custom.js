/* 半山 · 交互细节：阅读进度 + 入场动画 */
(function () {
    "use strict";

    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* 阅读进度条（只在文章页） */
    if (document.body.classList.contains("article-page")) {
        var bar = document.createElement("div");
        bar.className = "reading-progress";
        document.body.appendChild(bar);

        var ticking = false;
        var update = function () {
            var doc = document.documentElement;
            var total = doc.scrollHeight - window.innerHeight;
            var ratio = total > 0 ? window.scrollY / total : 0;
            bar.style.transform = "scaleX(" + Math.min(ratio, 1).toFixed(4) + ")";
            ticking = false;
        };

        window.addEventListener(
            "scroll",
            function () {
                if (!ticking) {
                    ticking = true;
                    window.requestAnimationFrame(update);
                }
            },
            { passive: true }
        );
        window.addEventListener("resize", update);
        update();
    }

    /* 列表入场 */
    if (!reduce && "IntersectionObserver" in window) {
        var items = document.querySelectorAll(".post-card, .shelf, .article-list article");
        if (items.length) {
            var io = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("is-in");
                            io.unobserve(entry.target);
                        }
                    });
                },
                { rootMargin: "0px 0px -6% 0px", threshold: 0.02 }
            );

            items.forEach(function (el, i) {
                el.classList.add("reveal");
                el.style.transitionDelay = Math.min(i * 55, 330) + "ms";
                io.observe(el);
            });
        }
    }
})();
