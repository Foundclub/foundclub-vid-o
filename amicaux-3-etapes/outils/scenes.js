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
      const actif = (n, k, t) => {
        // (GSAP 3 ne pose plus de classe : on pose les couleurs de .actif à la main)
        tl.set(`#et-${n} .sous span`, { color: "rgba(255,255,255,.45)", backgroundColor: "rgba(255,255,255,0)", borderColor: "rgba(255,255,255,.18)" }, t);
        tl.set(`#et-${n} .sous span:nth-child(${k})`, { color: "#001218", backgroundColor: "#ffffff", borderColor: "#ffffff" }, t);
        tl.fromTo(`#et-${n} .sous span:nth-child(${k})`, { scale: 1.15 }, { scale: 1, duration: 0.2, ease: "power2.out" }, t);
      };

      // ── ACCROCHE : un vrai match ──
      montrer("#b-duel", 0);
      tl.fromTo("#b-duel", { scale: 1.08 }, { scale: 1, duration: 2.0, ease: "none" }, 0);
      tl.to("#b-duel", { scale: 0.86, opacity: 0, duration: 0.4, ease: "power2.in" }, T.tel - 0.1);

      // ── LE TÉLÉPHONE ──
      tl.fromTo("#tel", { opacity: 0, y: 900, rotation: 8 }, { opacity: 1, y: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, T.tel);
      etape(1, T.tel + 0.05);
      montrer("#vue-e1", T.e1);
      T.sous1.forEach((t, k) => actif(1, k + 1, t));
      zoom(T.e1 + 6.6, T.e2 - 0.05, 1.2, 280, 1174);       // « Publier l'annonce »

      // ── ÉTAPE 2 : une équipe propose ──
      sortir(1, T.e2 - 0.1);
      etape(2, T.e2);
      cacher("#vue-e1", T.e2); montrer("#vue-disc", T.e2);
      tl.set("#vue-disc", { filter: "brightness(0.35)" }, T.e2);
      tl.fromTo("#notif", { opacity: 0, y: -420 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.4)" }, T.notif);
      tl.to("#tel", { x: 8, duration: 0.045, yoyo: true, repeat: 9, ease: "none" }, T.notif);   // le téléphone vibre
      actif(2, 1, T.notif);
      tl.to("#notif", { opacity: 0, scale: 0.85, y: -60, duration: 0.22, ease: "power2.in" }, T.ouvre);
      tl.to("#vue-disc", { filter: "brightness(1)", duration: 0.25 }, T.ouvre);
      actif(2, 2, T.ouvre);
      zoom(T.ouvre + 0.3, T.e3 - 0.35, 1.3, 280, 820);       // la proposition, « Accepter » / « Refuser »

      // ── ÉTAPE 3 : accepter, le planning ──
      sortir(2, T.e3 - 0.1);
      etape(3, T.e3);
      cacher("#vue-disc", T.e3); montrer("#vue-acc", T.e3);
      actif(3, 1, T.e3);
      zoom(T.e3 + 0.2, T.plan - 0.3, 1.3, 280, 727);      // « Accepter cette proposition ? »
      cacher("#vue-acc", T.plan); montrer("#vue-plan", T.plan);
      tl.fromTo("#vue-plan", { scale: 1.06 }, { scale: 1, duration: 0.3, ease: "power2.out" }, T.plan);
      actif(3, 2, T.plan);
      zoom(T.plan + 0.35, T.celeb + 0.5, 1.22, 280, 600);     // la carte du match : Valbrune U13, samedi, 14:00, Stade du Moulin

      // ── Les appuis du doigt (un rond, pas une étiquette) ──
      APPUIS.forEach((a, i) => {
        tl.fromTo(`#appui-${i}`, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.18, ease: "power2.out" }, a.t);
        tl.to(`#appui-${i}`, { opacity: 0, scale: 1.25, duration: 0.25, ease: "power1.in" }, a.t + 0.25);
      });

      // ── FIN : on joue ──
      sortir(3, T.celeb - 0.15);
      tl.to("#tel", { y: 1000, rotation: -8, opacity: 0, duration: 0.35, ease: "power3.in" }, T.celeb - 0.2);
      montrer("#b-celeb", T.celeb);
      tl.fromTo("#b-celeb", { scale: 1.25 }, { scale: 1, duration: 0.5, ease: "power3.out" }, T.celeb);

      STICKERS.forEach((s, i) => {
        coller(`#sticker-${i}`, s.debut, s.penche);
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
