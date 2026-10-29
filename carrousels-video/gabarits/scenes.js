      // Chaque page arrive de la droite et repart à gauche, comme quand on fait glisser un carrousel ; pendant qu'elle est
      // là, elle avance très doucement vers nous (1 → 1,035).
      const GLISSE = 0.38;
      PAGES.forEach((p, i) => {
        const sel = `#page-${i}`;
        if (i === 0) tl.fromTo(sel, { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power2.out" }, 0);
        else tl.fromTo(sel, { opacity: 1, x: 1080, rotation: 2.5 }, { x: 0, rotation: 0, duration: GLISSE, ease: "power3.out" }, p.debut);
        tl.fromTo(`${sel} .zoom`, { scale: 1 }, { scale: 1.035, duration: p.fin - p.debut, ease: "none", transformOrigin: "50% 50%" }, p.debut);
        if (i < PAGES.length - 1) tl.to(sel, { x: -1080, rotation: -2.5, duration: GLISSE, ease: "power3.out" }, p.fin);
        else tl.to(sel, { opacity: 0, scale: 0.96, duration: 0.35, ease: "power2.in" }, p.fin - 0.1);
        (p.appuis || []).forEach((a, k) => {
          const s = `#appui-${i}-${k}`, t = p.debut + a.a;
          tl.fromTo(s, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.2, ease: "power2.out" }, t);
          tl.to(`${sel} .appuyer`, { scale: 0.985, duration: 0.08, yoyo: true, repeat: 1, ease: "power1.inOut" }, t + 0.12);
          tl.to(s, { opacity: 0, scale: 1.25, duration: 0.3, ease: "power1.in" }, t + 0.3);
        });
        // la notification : la page vibre comme un téléphone posé sur la table
        if (p.vibre != null) tl.to(sel, { x: 7, duration: 0.04, yoyo: true, repeat: 7, ease: "none" }, p.debut + p.vibre);
      });

      // Stickers : plaqués comme à la main, un peu penchés ; ils partent avec leur page
      STICKERS.forEach((s, i) => {
        tl.fromTo(`#sticker-${i}`, { opacity: 0, scale: 1.5, rotation: s.penche * 2 }, { opacity: 1, scale: 1, rotation: s.penche, duration: 0.14, ease: "power3.in" }, s.debut);
        tl.to(`#sticker-${i}`, { opacity: 0, y: -20, duration: 0.2, ease: "power2.in" }, s.fin - 0.2);
      });

      // ── CARTON FINAL ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.2);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.4);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1500, duration: 0.8, ease: "power2.inOut" }, FIN + 0.85);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.7);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.95);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.2);
