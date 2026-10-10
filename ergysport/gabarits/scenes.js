      // ── Outils communs ─────────────────────────────────────────────
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.08, ease: "none" }, fin - 0.08);
      });
      // une ligne de titre : elle glisse depuis le côté et se pose (la ligne orange arrive de l'autre côté)
      const ligne = (sel, t, cote = -1) => tl.fromTo(sel, { opacity: 0, x: cote * 120, skewX: cote * 8 },
        { opacity: 1, x: 0, skewX: 0, duration: 0.38, ease: "power4.out" }, t);
      const sortir = (sel, t) => tl.to(sel, { opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }, t);
      // une étiquette produit : elle surgit sous le produit tenu, la pointe vers le haut
      const etiquette = (sel, t) => {
        tl.fromTo(sel, { opacity: 0, y: 50, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.36, ease: "back.out(1.8)" }, t);
        tl.fromTo(`${sel} .barre`, { scaleY: 0 }, { scaleY: 1, duration: 0.3, ease: "power3.out", transformOrigin: "50% 100%" }, t + 0.12);
      };
      const sousLigne = (sel, t) => tl.fromTo(sel, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out" }, t);
      const quitter = (sel, t) => tl.to(sel, { opacity: 0, scale: 0.92, duration: 0.22, ease: "power2.in" }, t);

      // ── 1 · « le football, c'est pas seulement ce qui se passe sur le terrain » ──
      ligne("#t1 .b", T.football - 0.45, -1);
      ligne("#t1 .o", T.terrain - 0.6, 1);
      sortir("#t1 .l", T.terrain + 0.25);

      // ── 2 · « la préparation, l'hydratation et la récupération, c'est aussi important » ──
      [["#p-prep", T.preparation], ["#p-hydra", T.hydratation], ["#p-recup", T.recuperation]].forEach(([s, t], i) => {
        tl.fromTo(s, { opacity: 0, x: (i % 2 ? 1 : -1) * 140, scale: 0.85 }, { opacity: 1, x: 0, scale: 1, duration: 0.36, ease: "back.out(1.7)" }, t - 0.5);
        tl.fromTo(`${s} .ic`, { rotation: -90, scale: 0.4 }, { rotation: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }, t - 0.42);
      });
      tl.to(".pilier", { scale: 1.06, duration: 0.14, yoyo: true, repeat: 1, ease: "power1.out", stagger: 0.06 }, T.important - 0.35);
      sortir(".pilier", T.important + 0.25);

      // ── 3 · « je vais vous présenter Ergysport » : le logo est déjà dans la vidéo, on l'éclaire ──
      tl.fromTo("#eclat", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, T.ergysport - 0.75);
      tl.to("#eclat", { opacity: 0, duration: 0.6, ease: "power2.in" }, T.ergysport + 0.35);

      // ── 4 · « une gamme de nutrition sportive. On retrouve de la whey » ──
      ligne("#t2 .b", T.gamme - 0.2, -1);
      ligne("#t2 .o", T.nutrition - 0.35, 1);
      sortir("#t2 .l", T.retrouve);
      etiquette("#e-whey", T.retrouve + 0.15);
      quitter("#e-whey", T.whey + 0.45);

      // ── 5 · « de la créatine, des gélules pour accompagner la récupération sportive… » ──
      etiquette("#e-creatine", T.creatine - 0.6);
      quitter("#e-creatine", T.gelules - 0.45);
      etiquette("#e-gelules", T.gelules - 0.35);
      quitter("#e-gelules", T.courbatures + 0.15);

      // ── 6 · « mais aussi des multivitamines pour la vitalité » ──
      etiquette("#e-multi", T.multivitamines - 0.75);
      sousLigne("#e-multi-s", T.vitalite - 0.5);
      quitter("#e-multi", T.vitalite + 0.3);

      // ── 7 · « et pendant l'effort, des barres céréales et des boosts pour un plein d'énergie » ──
      ligne("#t3 .o", T.effort - 0.55, 1);
      etiquette("#e-barres", T.barres - 0.35);
      etiquette("#e-boost", T.boost - 0.4);
      sousLigne("#e-boost-s", T.energie - 0.5);
      sortir("#t3 .l", T.energie + 0.3);
      quitter(["#e-barres", "#e-boost"], T.energie + 0.3);

      // ── 8 · « parce que la performance sur le terrain, ça se prépare aussi dehors » ──
      ligne("#t4 .b", T.performance - 0.5, -1);
      ligne("#t4 .o", T.terrain2 - 0.5, 1);
      sortir("#t4 .l", T.prepare - 0.45);
      ligne("#t5 .b", T.prepare - 0.35, -1);
      ligne("#t5 .o", T.dehors - 0.4, 1);
      tl.to("#t5 .o", { scale: 1.07, duration: 0.16, yoyo: true, repeat: 1, ease: "power1.out" }, T.dehors - 0.02);

      // ── 9 · « …avec Ergysport » : carton final aux couleurs de la marque ──
      tl.fromTo("#fin-fond", { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power3.inOut" }, DEBUT_CARTON);
      tl.fromTo("#fin-courbe", { yPercent: 100 }, { yPercent: 0, duration: 0.55, ease: "power3.out" }, DEBUT_CARTON + 0.3);
      tl.fromTo("#fin-logo", { opacity: 0, scale: 0.7, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "back.out(1.6)" }, DEBUT_CARTON + 0.4);
      tl.fromTo("#fin-phrase", { opacity: 0, y: 40, skewX: -8 }, { opacity: 1, y: 0, skewX: 0, duration: 0.42, ease: "power4.out" }, DEBUT_CARTON + 0.8);
      tl.fromTo("#fin-site", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, DEBUT_CARTON + 1.1);
      tl.fromTo("#fin-nutergia", { opacity: 0 }, { opacity: 1, duration: 0.35, ease: "power2.out" }, DEBUT_CARTON + 1.3);
