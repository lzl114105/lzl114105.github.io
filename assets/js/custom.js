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

    /* 开场：head 里已经判定过「是不是首页、这个会话播过没有」,
       这里只负责按那个结论把幕布搭起来。文案走 meta,模板里改。 */
    var pending = document.documentElement.classList.contains("intro-pending");
    if (pending && reduce) {
        document.documentElement.classList.remove("intro-pending");
        pending = false;
    }

    if (pending) {
        var startIntro = function () {
            var meta = function (name) {
                var el = document.querySelector('meta[name="' + name + '"]');
                return el ? el.getAttribute("content") || "" : "";
            };

            var intro = document.createElement("div");
            intro.className = "home-intro";
            intro.setAttribute("aria-hidden", "true");

            var inner = document.createElement("div");
            inner.className = "home-intro__inner";

            var title = document.createElement("h1");
            title.className = "home-intro__title";
            title.textContent = meta("intro-text") || document.title || "";
            inner.appendChild(title);

            var tagline = meta("intro-tagline");
            if (tagline) {
                var sub = document.createElement("p");
                sub.className = "home-intro__tagline";
                sub.textContent = tagline;
                inner.appendChild(sub);
            }

            var left = document.createElement("div");
            left.className = "home-intro__panel home-intro__panel--left";
            var right = document.createElement("div");
            right.className = "home-intro__panel home-intro__panel--right";
            var cut = document.createElement("div");
            cut.className = "home-intro__cut";

            intro.appendChild(left);
            intro.appendChild(right);
            intro.appendChild(cut);
            intro.appendChild(inner);
            document.body.appendChild(intro);
            document.body.classList.add("intro-lock");

            /* 先记标记再播:中途刷新也不会重来一遍 */
            try {
                sessionStorage.setItem("bs-intro-played", "1");
            } catch (e) {
                /* 隐私模式下 sessionStorage 会抛错,忽略即可 */
            }
            document.documentElement.classList.remove("intro-pending");

            window.requestAnimationFrame(function () {
                intro.classList.add("is-running");
            });

            window.setTimeout(function () {
                document.body.classList.remove("intro-lock");
                if (intro.parentNode) intro.parentNode.removeChild(intro);
            }, 4200);
        };

        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", startIntro, { once: true });
        } else {
            startIntro();
        }
    }
})();
