      // ── outils ──
      const apparaitre = (sel, t, de = { y: 40 }) => tl.fromTo(sel, { opacity: 0, ...de }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "power3.out" }, t);
      const coller = (sel, t, r) => tl.fromTo(sel, { opacity: 0, scale: 1.5, rotation: r * 2 }, { opacity: 1, scale: 1, rotation: r, duration: 0.14, ease: "power3.in" }, t);
      const montrer = (sel, t) => tl.set(sel, { opacity: 1 }, t);
      const cacher = (sel, t) => tl.set(sel, { opacity: 0 }, t);
      const zoom = (debut, fin, s, ox, oy) => {     // la caméra s'approche d'un endroit de l'écran, puis recule
        tl.fromTo("#camera", { scale: 1, transformOrigin: `${ox}px ${oy}px` }, { scale: s, duration: 0.45, ease: "power3.inOut" }, debut);
        tl.to("#camera", { scale: 1, duration: 0.3, ease: "power2.inOut" }, fin);
      };
      // Un titre d'étape : le carré du numéro tombe, les mots arrivent un par un, puis les sous-étapes
      const etape = (n, t) => {
        tl.set(`#et-${n}`, { opacity: 1, x: 0 }, t);
        tl.fromTo(`#et-${n} .num`, { scale: 2.2, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }, t);
        tl.fromTo(`#et-${n} .titre .mot`, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out", stagger: 0.06 }, t + 0.1);
        tl.fromTo(`#et-${n} .sous span`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: "power2.out", stagger: 0.05 }, t + 0.3);
      };
      const sortir = (n, t) => tl.to(`#et-${n}`, { opacity: 0, x: -80, duration: 0.2, ease: "power2.in" }, t);
      const actif = (sel, k, t) => {
        // (GSAP 3 ne pose plus de classe : on pose les couleurs de .actif à la main)
        tl.set(`${sel} span`, { color: "rgba(255,255,255,.45)", backgroundColor: "rgba(255,255,255,0)", borderColor: "rgba(255,255,255,.18)" }, t);
        tl.set(`${sel} span:nth-child(${k})`, { color: "#001218", backgroundColor: "#ffffff", borderColor: "#ffffff" }, t);
        tl.fromTo(`${sel} span:nth-child(${k})`, { scale: 1.15 }, { scale: 1, duration: 0.2, ease: "power2.out" }, t);
      };

      // ── ACCROCHE : un vrai match ──
      // L'ouverture frappe : éclair blanc, le plan arrive de très près en tournant, tremble, puis avance doucement
      montrer("#b-duel", 0);
      tl.fromTo("#eclair", { opacity: 1 }, { opacity: 0, duration: 0.28, ease: "power2.out" }, 0);
      tl.fromTo("#b-duel", { scale: 1.45, rotation: -4 }, { scale: 1.06, rotation: 0, duration: 0.32, ease: "power4.out" }, 0);
      tl.to("#b-duel", { x: 14, y: -8, duration: 0.035, yoyo: true, repeat: 5, ease: "none" }, 0.3);
      tl.to("#b-duel", { scale: 1, duration: T.tel - 0.5, ease: "none" }, 0.5);
      tl.to("#b-duel", { scale: 0.86, opacity: 0, duration: 0.4, ease: "power2.in" }, T.tel - 0.1);

      // ── LE TÉLÉPHONE ──
      tl.fromTo("#eclair-bleu", { opacity: 0.55 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, T.tel + 0.08);
      tl.fromTo("#tel", { opacity: 0, y: 900, rotation: 8 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, T.tel);
      etape(1, T.tel + 0.05);
      sortir(1, T.e2 - 0.1); etape(2, T.e2);
      sortir(2, T.e3 - 0.1); etape(3, T.e3);
      // Étape 2, « deux solutions » : la moitié du titre qui ne joue pas s'efface
      tl.set("#et-2 .b", { opacity: 0.3 }, T.creer); tl.set("#et-2 .a", { opacity: 1 }, T.creer);
      tl.set("#et-2 .a", { opacity: 0.3 }, T.chercher); tl.set("#et-2 .b", { opacity: 1 }, T.chercher);
      tl.set("#sous-2a", { opacity: 0 }, T.chercher); tl.set("#sous-2b", { opacity: 1 }, T.chercher);
      tl.fromTo("#sous-2b span", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, stagger: 0.05, immediateRender: false }, T.chercher);
      // Les écrans du téléphone : chacun reste jusqu'au suivant
      VUES.forEach((v, i) => {
        montrer(`#${v.id}`, v.debut);
        if (i + 1 < VUES.length) cacher(`#${v.id}`, VUES[i + 1].debut);
      });
      ZOOMS.forEach(z => zoom(z.debut, z.fin, z.s, z.ox, z.oy));
      ACTIFS.forEach(a => actif(a.sel, a.k, a.t));
      // Étape 3 : la notification tombe sur la discussion assombrie
      tl.set("#vue-disc", { filter: "brightness(0.35)" }, T.e3);
      tl.fromTo("#notif", { opacity: 0, y: -420 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.4)" }, T.notif);
      tl.to("#tel", { x: 8, duration: 0.045, yoyo: true, repeat: 9, ease: "none" }, T.notif);   // le téléphone vibre
      tl.to("#notif", { opacity: 0, scale: 0.85, y: -60, duration: 0.22, ease: "power2.in" }, T.ouvre);
      tl.to("#vue-disc", { filter: "brightness(1)", duration: 0.25 }, T.ouvre);
      tl.fromTo("#vue-plan", { scale: 1.06 }, { scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }, T.plan);

      // ── Les appuis du doigt (un rond, pas une étiquette) ──
      APPUIS.forEach((a, i) => {
        tl.fromTo(`#appui-${i}`, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.18, ease: "power2.out" }, a.t);
        tl.to(`#appui-${i}`, { opacity: 0, scale: 1.25, duration: 0.25, ease: "power1.in" }, a.t + 0.25);
        if (!a.bouton) return;
        // le bouton s'éclaire et s'enfonce quand le doigt touche, puis revient ; l'onde s'étale dans le bouton
        const b = `#bouton-${i}`, t = a.t + 0.12;
        tl.fromTo(b, { opacity: 0, scale: 1 }, { opacity: 1, scale: 0.95, duration: 0.08, ease: "power2.out" }, t);
        tl.to(b, { opacity: 0, scale: 1, duration: 0.3, ease: "power2.out" }, t + 0.14);
        tl.fromTo(`${b} .onde`, { scale: 0, opacity: 1 }, { scale: 14, opacity: 0, duration: 0.45, ease: "power2.out" }, t);
      });
      HALOS.forEach((h, i) => {
        tl.fromTo(`#halo-${i}`, { opacity: 0, scale: 1.12 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power2.out" }, h.t);
        tl.to(`#halo-${i}`, { opacity: 0.35, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }, h.t + 0.3);
        tl.to(`#halo-${i}`, { opacity: 0, duration: 0.2 }, T.creer - 0.15);
      });

      // ── FIN : on joue ──
      sortir(3, T.celeb - 0.15);
      tl.to("#tel", { y: 1000, rotation: -8, opacity: 0, duration: 0.35, ease: "power3.in" }, T.celeb - 0.2);
      montrer("#b-celeb", T.celeb);
      tl.fromTo("#eclair", { opacity: 0.8 }, { opacity: 0, duration: 0.25, ease: "power2.out", immediateRender: false }, T.celeb);
      tl.fromTo("#b-celeb", { scale: 1.25 }, { scale: 1, duration: 0.5, ease: "power3.out" }, T.celeb);

      STICKERS.forEach((s, i) => {
        if (i === 0) tl.fromTo(`#sticker-${i}`, { opacity: 0, scale: 2.6, rotation: s.penche * 4 }, { opacity: 1, scale: 1, rotation: s.penche, duration: 0.16, ease: "power4.in" }, s.debut);
        else coller(`#sticker-${i}`, s.debut, s.penche);
        tl.to(`#sticker-${i}`, { opacity: 0, y: -20, duration: 0.18, ease: "power2.in" }, s.fin - 0.18);
      });

      // ── CARTON FINAL ──
      const FIN = T.fin;
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, FIN + 0.15);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.3);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1500, duration: 0.8, ease: "power2.inOut" }, FIN + 0.75);
      apparaitre("#fin .phrase", FIN + 0.55);
      apparaitre("#fin .chemin", FIN + 0.75);
      apparaitre("#fin .badges", FIN + 0.95);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.3 }, FIN + 1.15);
