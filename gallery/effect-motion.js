"use strict";

const effectDuration = 3.6;

window.AtlasEffectMotion = Object.freeze({
  duration: effectDuration,

  timelineFor(scene, spec, options = {}) {
    const plateA = scene.querySelector(".test-effect__plate--a");
    const plateB = scene.querySelector(".test-effect__plate--b");
    const grain = scene.querySelector(".test-effect__grain");
    const shade = scene.querySelector(".test-effect__shade");
    const sweep = scene.querySelector(".test-effect__sweep");
    const grid = scene.querySelector(".test-effect__grid");
    const caption = scene.querySelector(".test-effect__caption");
    const timeline = window.gsap.timeline({
      paused: true,
      repeat: options.repeat ?? 0,
      repeatDelay: options.repeatDelay ?? 0,
    });
    const transition = (from, to, target = plateB) => {
      timeline.fromTo(target, from, {
        ...to,
        duration: effectDuration,
        ease: "power2.inOut",
      }, 0);
    };

    switch (spec.mode) {
      case "blur":
        if (spec.transition) {
          window.gsap.set(plateB, { opacity: 1, clipPath: "inset(0 100% 0 0)" });
          timeline.to(plateA, {
            filter: "blur(18px)",
            scale: 1.08,
            duration: effectDuration / 2,
          }, 0);
          timeline.to(plateB, {
            clipPath: "inset(0 0% 0 0)",
            duration: effectDuration / 2,
            ease: "power2.inOut",
          }, effectDuration / 2);
        } else {
          transition(
            { filter: "blur(0px)", scale: 1 },
            { filter: "blur(18px)", scale: 1.08 },
            plateA,
          );
        }
        break;
      case "grain":
        transition({ opacity: 0.12, xPercent: -3 }, { opacity: 0.86, xPercent: 3 }, grain);
        break;
      case "vignette":
        transition({ opacity: 0.12 }, { opacity: 0.96 }, shade);
        break;
      case "pixel":
        transition({ opacity: 0.08, scale: 1.4 }, { opacity: 0.74, scale: 1 }, grid);
        if (spec.transition) {
          window.gsap.set(plateB, { opacity: 1 });
          timeline.fromTo(
            plateB,
            { clipPath: "inset(0 100% 0 0)", filter: "contrast(1.8)" },
            {
              clipPath: "inset(0 0% 0 0)",
              filter: "contrast(1)",
              duration: effectDuration,
              ease: "steps(10)",
            },
            0,
          );
        } else {
          timeline.to(plateA, {
            filter: "contrast(1.45) saturate(0.62)",
            duration: effectDuration,
            ease: "none",
          }, 0);
        }
        break;
      case "glitch":
        transition(
          { opacity: 0, xPercent: -6, clipPath: "inset(8% 0 76%)" },
          { opacity: 0.72, xPercent: 4, clipPath: "inset(62% 0 10%)" },
        );
        break;
      case "dissolve":
        transition({ opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)" });
        break;
      case "shatter":
        transition(
          { opacity: 0, scale: 1.24, clipPath: "polygon(0 0,0 0,0 0,0 0,0 0,0 0)" },
          {
            opacity: 1,
            scale: 1,
            clipPath: "polygon(0 0,100% 0,100% 100%,0 100%,0 60%,44% 48%)",
          },
        );
        break;
      case "push":
        window.gsap.set(plateB, { opacity: 1 });
        transition({ xPercent: 100 }, { xPercent: 0 });
        timeline.fromTo(
          plateA,
          { xPercent: 0 },
          { xPercent: -100, duration: effectDuration, ease: "power2.inOut" },
          0,
        );
        break;
      case "scale":
        transition({ opacity: 0, scale: 0.42 }, { opacity: 1, scale: 1 });
        break;
      case "rotate":
        scene.style.perspective = "1200px";
        transition(
          { opacity: 0, rotationY: 92, transformOrigin: "left center" },
          { opacity: 1, rotationY: 0 },
        );
        timeline.to(plateA, {
          rotationY: -92,
          transformOrigin: "right center",
          duration: effectDuration,
          ease: "power2.inOut",
        }, 0);
        break;
      case "warp":
        transition(
          { opacity: 0, scale: 0.72, skewX: 18, clipPath: "circle(0% at 50% 50%)" },
          { opacity: 1, scale: 1.08, skewX: 0, clipPath: "circle(76% at 50% 50%)" },
        );
        break;
      case "liquid":
        transition(
          { opacity: 1, clipPath: "ellipse(0% 0% at 50% 50%)", borderRadius: "50%" },
          { opacity: 1, clipPath: "ellipse(76% 82% at 50% 50%)", borderRadius: "0%" },
        );
        break;
      case "lens":
        transition(
          { opacity: 1, clipPath: "circle(0% at 58% 48%)", scale: 1.28 },
          { opacity: 1, clipPath: "circle(76% at 58% 48%)", scale: 1 },
        );
        break;
      case "burn":
        transition(
          { opacity: 1, clipPath: "circle(0% at 48% 52%)" },
          { opacity: 1, clipPath: "circle(78% at 48% 52%)" },
        );
        timeline.fromTo(
          shade,
          { opacity: 0 },
          { opacity: 0.82, duration: 1.4, yoyo: true, repeat: 1 },
          0.8,
        );
        break;
      case "light":
        transition({ opacity: 0, xPercent: -85 }, { opacity: 0.92, xPercent: 85 }, sweep);
        if (spec.transition) {
          timeline.fromTo(
            plateB,
            { opacity: 0, clipPath: "inset(0 100% 0 0)" },
            {
              opacity: 1,
              clipPath: "inset(0 0% 0 0)",
              duration: effectDuration,
              ease: "power2.inOut",
            },
            0,
          );
        }
        break;
      case "caption":
        timeline.fromTo(
          caption,
          { opacity: 0, yPercent: 130 },
          { opacity: 1, yPercent: 0, duration: 1.4, ease: "power3.out" },
          0.35,
        );
        break;
      case "code":
        transition({ opacity: 0.12, yPercent: -22 }, { opacity: 0.84, yPercent: 18 }, grid);
        break;
      case "data":
        transition(
          { opacity: 0, clipPath: "inset(100% 0 0)" },
          { opacity: 0.84, clipPath: "inset(0 0 0)" },
          grid,
        );
        break;
      case "camera":
        transition(
          { scale: 1, xPercent: -2, yPercent: 0 },
          { scale: 1.22, xPercent: 4, yPercent: -3 },
          plateA,
        );
        break;
      default:
        transition(
          { opacity: 1, clipPath: "inset(0 100% 0 0)" },
          { opacity: 1, clipPath: "inset(0 0% 0 0)" },
        );
    }

    timeline.set(scene, { opacity: 1 }, effectDuration);
    return timeline;
  },
});
