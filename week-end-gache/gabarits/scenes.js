      // Sous-titres
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.06, ease: "none" }, fin - 0.06);
      });

      const surligner = (sel, t) => {
        tl.fromTo(`${sel} .fond`, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, t);
        tl.fromTo(`${sel} .mot`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, t + 0.1);
      };
      const apparaitre = (sel, t, de = { y: 40 }) => tl.fromTo(sel, { opacity: 0, ...de }, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }, t);
      const etiquette = (sel, t, cote) => tl.fromTo(sel, { opacity: 0, x: cote * 160, scale: 0.8 }, { opacity: 1, x: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, t);
      const appuyer = (sel, t) => {
        tl.fromTo(sel, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.22, ease: "power2.out" }, t);
        tl.to(sel, { opacity: 0, scale: 1.25, duration: 0.3, ease: "power1.in" }, t + 0.32);
      };
      const pastille = (sel, t) => tl.fromTo(sel, { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, t);
      const tremble = (sel, t) => tl.to(sel, { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, t);

      // ── OUVERTURE : le mème (sur l'image fixe d'ach10, sans voix) ──
      tl.fromTo("#cadre-video", { scale: 1.12 }, { scale: 1.0, duration: 3.0, ease: "power1.out" }, 0);
      tl.to("#ouverture-voile", { opacity: 1, duration: 0.2 }, 0);
      tl.fromTo("#meme-vendredi", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.8)" }, 0.15);
      tl.fromTo("#meme-dimanche", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.8)" }, 1.45);
      tl.fromTo("#meme-dimanche .barre", { scaleX: 0 }, { scaleX: 1, duration: 0.25, ease: "power2.out" }, 2.15);
      tremble("#meme-dimanche", 2.35);
      tl.to(["#meme-vendredi", "#meme-dimanche", "#ouverture-voile"], { opacity: 0, duration: 0.2 }, T.a - 0.2);

      // ── 1 : tout ce qu'il a visualisé… et là : repos. ──
      pastille("#reve-but", T.but - 0.55);
      pastille("#reve-celebration", T.celebration - 0.75);
      pastille("#reve-post", T.reseaux - 1.4);
      tl.to("#reves .pastille", { opacity: 0, y: -20, duration: 0.2, stagger: 0.05 }, T.repos - 1.1);
      tl.set("#tampon", { opacity: 1 }, T.repos - 0.5);
      tl.fromTo("#tampon .repos", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.in" }, T.repos - 0.5);
      tremble("#tampon", T.repos - 0.3);
      // « Encore. » : le tampon retombe une deuxième fois
      tl.to("#tampon .repos", { opacity: 0, duration: 0.06 }, T.encore - 0.35);
      tl.fromTo("#tampon .encore", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.in" }, T.encore - 0.35);
      tremble("#tampon", T.encore - 0.15);
      tl.to("#tampon", { opacity: 0, y: -30, duration: 0.25 }, T.encore + 0.5);

      // ── 2 : meilleur pour préparer mon sac que pour frapper ──
      tl.set("#sac", { opacity: 1 }, T.sac - 1.2);
      apparaitre("#sac .ligne", T.sac - 1.2);
      surligner("#sac", T.frappes - 0.7);
      tl.to("#sac", { opacity: 0, y: -30, duration: 0.25 }, T.c + 0.1);

      // ── 3 : un match amical chaque week-end sans match ──
      tl.set("#amical", { opacity: 1 }, T.arreter + 0.6);
      apparaitre("#amical .ligne", T.arreter + 0.6);
      surligner("#amical", T.amical - 0.7);
      tl.to("#amical", { opacity: 0, y: -30, duration: 0.25 }, TEL - 0.3);

      // ── 4 : LE TÉLÉPHONE — ach10 s'efface, l'appli prend l'écran ──
      tl.to("#cadre-video", { scale: 0.86, opacity: 0, duration: 0.45, ease: "power2.in" }, TEL);
      tl.to("#degrades", { opacity: 0, duration: 0.3 }, TEL);
      tl.to("#mode-tel", { opacity: 1, duration: 0.3 }, TEL + 0.1);
      tl.fromTo("#tel", { opacity: 0, y: 500, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, TEL + 0.15);
      apparaitre("#t-rubrique", TEL + 0.45, { x: -40 });
      tl.set("#t-titre", { opacity: 1 }, TEL + 0.55);
      apparaitre("#t-l1", TEL + 0.55);
      apparaitre("#t-l2", TEL + 0.85);
      EXTRAITS.forEach((x, i) => {
        tl.fromTo(`#x-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, x.debut);
        tl.to(`#x-${i}`, { opacity: 0, duration: 0.01 }, x.debut + x.duree - 0.01);
      });
      tl.set("#cap-creer", { opacity: 1 }, EXTRAITS[2].debut + EXTRAITS[2].duree - 0.02);
      appuyer("#appui-amicaux", EXTRAITS[0].debut + EXTRAITS[0].duree - 0.45);
      etiquette("#tag-trouve", EXTRAITS[1].debut + 0.25, -1);
      etiquette("#tag-publie", EXTRAITS[2].debut, 1);
      appuyer("#appui-creer", T.creer - 0.3);
      tl.to("#cap-creer", { scale: 1.03, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 52%" }, T.creer - 0.15);
      // Retour à ach10 : « envoie-lui la vidéo… »
      tl.to(["#tag-trouve", "#tag-publie"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, RETOUR - 0.2);
      tl.to("#tel", { opacity: 0, y: 400, duration: 0.35, ease: "power3.in" }, RETOUR);
      tl.to("#mode-tel", { opacity: 0, duration: 0.3 }, RETOUR + 0.1);
      tl.fromTo("#cadre-video", { scale: 0.86, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, RETOUR + 0.1);
      tl.to("#degrades", { opacity: 1, duration: 0.3 }, RETOUR + 0.2);

      // ── 5 : « envoie-lui la vidéo » ──
      pastille("#envoie .pastille", T.video - 0.7);
      tremble("#envoie .pastille", T.jouer - 0.2);

      // ── CARTON FINAL ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
