      // Sous-titres
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.08, ease: "none" }, fin - 0.08);
      });

      // Passage plein cadre ⇄ médaillon (l'orateur en haut à droite)
      const versMedaillon = (t) => {
        tl.to("#degrade-bas", { opacity: 0, duration: 0.4 }, t);
        tl.to("#cadre-video", { clipPath: "circle(440px at 540px 800px)", scale: 0.35, x: 360, y: -550, duration: 0.8, ease: "power3.inOut" }, t);
        tl.to("#medaillon-anneau", { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, t + 0.7);
      };
      const versPleinCadre = (t) => {
        tl.to("#medaillon-anneau", { opacity: 0, scale: 0.6, duration: 0.25 }, t);
        tl.to("#cadre-video", { clipPath: "circle(2300px at 540px 800px)", scale: 1, x: 0, y: 0, duration: 0.7, ease: "power3.inOut" }, t);
        tl.to("#degrade-bas", { opacity: 1, duration: 0.5 }, t + 0.3);
      };
      tl.set("#medaillon-anneau", { scale: 0.6 }, 0);
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

      // ── SCÈNES 1 À 3 : le calendrier ─────────────────────────────
      const CAL = T.professionnels - 0.55;
      versMedaillon(CAL);
      tl.to("#mode-cal", { opacity: 1, duration: 0.4 }, CAL + 0.3);
      apparaitre("#calendrier", CAL + 0.3, { y: 300 });
      apparaitre("#c-rubrique-pros", CAL + 0.35, { x: -40 });
      apparaitre("#c-titre-pros", CAL + 0.5);
      // Les pros : un match tous les 3 jours, le compteur monte
      const nb = document.getElementById("nb-matchs"), pl = document.getElementById("pluriel");
      const compter = (v) => { const n = Math.round(v); nb.textContent = String(n); pl.textContent = n > 1 ? "s" : ""; };
      const compte = { v: 0 };
      PROS.forEach((jour, i) => {
        tl.fromTo(`#b-${jour}`, { opacity: 0, scale: 0.2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2.2)" }, T.jours - 0.6 + i * 0.1);
      });
      tl.fromTo(compte, { v: 0 }, { v: PROS.length, duration: PROS.length * 0.1, ease: "none", onUpdate: () => compter(compte.v) }, T.jours - 0.6);
      // Nous, les amateurs : tout s'éteint, le compteur retombe à 0
      tl.to(["#c-rubrique-pros", "#c-titre-pros"], { opacity: 0, x: -40, duration: 0.25 }, T.amateur - 0.7);
      apparaitre("#c-rubrique-amat", T.amateur - 0.5, { x: -40 });
      tl.to(PROS.map((j) => `#b-${j}`), { opacity: 0, scale: 0.2, duration: 0.18, stagger: 0.04, ease: "power2.in" }, T.mois - 0.9);
      tl.to(compte, { v: 0, duration: 0.6, ease: "power2.in", onUpdate: () => compter(compte.v) }, T.mois - 0.9);
      apparaitre("#c-titre-amat", T.mois - 0.5);
      // Coupe, trêves, reportés : trois tampons sur les week-ends
      [["#t-coupe", T.coupe], ["#t-treve", T.treves], ["#t-reporte", T.reportes]].forEach(([sel, t]) => {
        tl.fromTo(sel, { opacity: 0, scale: 2.2, rotation: -20, xPercent: -50, yPercent: -50 }, { opacity: 1, scale: 1, rotation: -8, xPercent: -50, yPercent: -50, duration: 0.22, ease: "power3.in" }, t - 0.35);
      });
      tl.to("#calendrier", { x: 8, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.reportes - 0.13);
      surligner("#sans-match", T.mois2 - 0.55);
      tl.to("#mode-cal", { opacity: 0, duration: 0.3 }, T.attendez - 0.6);
      versPleinCadre(T.attendez - 0.6);

      // ── SCÈNE 4 : la licence à 350 €, puis « la tête de ma mère, je vais jouer ! » ──
      apparaitre("#licence", T.attendez - 0.1, { y: -60 });
      const prix = { v: 0 }, elPrix = document.getElementById("prix");
      tl.fromTo(prix, { v: 0 }, { v: 350, duration: 0.9, ease: "power2.out", onUpdate: () => { elPrix.textContent = String(Math.round(prix.v)); } }, T["350"] - 0.9);
      tl.to("#licence", { scale: 1.06, duration: 0.12, yoyo: true, repeat: 1 }, T["350"]);
      tl.to("#licence", { opacity: 0, y: -40, duration: 0.25 }, T.mere - 0.95);
      tl.fromTo("#bulle-1", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.3, ease: "back.out(2)" }, T.mere - 0.8);
      tl.to("#bulle-1", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, T.jouer - 0.3);

      // ── SCÈNE 5 : « pourquoi pas un match amical ? » ──
      apparaitre("#s5-titre .ligne", T.amicaux - 1.1);
      surligner("#s5-titre", T.amicaux - 0.55);

      // ── SCÈNE 6 : les deux galères du coach ──
      apparaitre("#galere-equipe", T.equipe - 0.6, { x: -200 });
      apparaitre("#galere-orga", T.organiser - 0.6, { x: 200 });
      tl.to(["#galere-equipe .croix", "#galere-orga .croix"], { scale: 1.2, duration: 0.12, yoyo: true, repeat: 1 }, T.organiser);

      // ── SCÈNE 7 : FoundClub ──
      tl.fromTo("#logo .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, T.fond - 0.9);
      tl.fromTo("#logo .marque", { opacity: 0, y: 30, scale: 1.15 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, T.fond - 0.55);
      tl.fromTo("#logo .reflet", { x: 0 }, { x: 900, duration: 0.7, ease: "power2.inOut" }, T.fond);

      // ── SCÈNES 8 À 10 : le téléphone ─────────────────────────────
      const TEL = EXTRAITS[0].debut - 0.75;
      tl.to("#logo", { opacity: 0, duration: 0.3 }, TEL);
      versMedaillon(TEL);
      tl.to("#mode-tel", { opacity: 1, duration: 0.3 }, TEL + 0.3);
      tl.fromTo("#tel", { opacity: 0, y: 500, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, TEL + 0.45);
      // Les extraits de l'enregistrement d'écran, l'un après l'autre
      EXTRAITS.forEach((x, i) => {
        tl.fromTo(`#x-${i}`, { opacity: 0 }, { opacity: 1, duration: i === 0 ? 0.01 : 0.12 }, x.debut);
        tl.to(`#x-${i}`, { opacity: 0, duration: 0.01 }, x.debut + x.duree - 0.01);
      });
      apparaitre("#t-rubrique-1", TEL + 0.6, { x: -40 });
      apparaitre("#t1-l1", T.coach8 - 0.2);
      apparaitre("#t1-l2", T.disponible - 0.45);
      tl.set("#t-titre-1", { opacity: 1 }, T.coach8 - 0.2);
      etiquette("#tag-pres", T.chez - 0.4, -1);
      etiquette("#tag-deplace", T.deplace - 0.4, 1);
      etiquette("#tag-recoit", T.recoit - 0.4, -1);
      // « C'est tout. »
      tl.to(["#tag-pres", "#tag-deplace", "#tag-recoit"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, T.tout - 0.6);
      tl.fromTo("#cest-tout", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power3.in" }, T.tout - 0.45);
      tl.to("#tel", { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.tout - 0.23);
      tl.to("#cest-tout", { opacity: 0, duration: 0.25 }, T.tout + 0.5);
      tl.to(["#t-rubrique-1", "#t-titre-1"], { opacity: 0, x: -40, duration: 0.25 }, T.tout + 0.4);

      // Scène 10 : l'autre coach accepte → le match est au planning → la compo
      const montrer = (sel, t) => tl.fromTo(sel, { opacity: 0, x: 500 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }, t);
      const cacher = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.25 }, t);
      // les écrans avancent à leur rythme ; les étiquettes suivent ses mots
      montrer("#cap-proposition", T.tout + 0.55);
      apparaitre("#t-rubrique-2", T.tout + 0.65, { x: -40 });
      appuyer("#appui-accepter", T.treve - 0.05);
      cacher("#cap-proposition", T.treve + 0.4);
      montrer("#cap-accepter", T.treve + 0.4);
      appuyer("#appui-confirmer", T.treve + 1.1);
      cacher("#cap-accepter", T.treve + 1.5);
      montrer("#cap-planning", T.treve + 1.5);
      etiquette("#tag-treve", T.treve - 0.4, -1);
      etiquette("#tag-coupe", T.coupe10 - 0.4, 1);
      etiquette("#tag-annule", T.annule - 0.4, -1);
      etiquette("#tag-semaine", T.semaine - 0.4, 1);
      // la compo (planche des 5 sports), puis « continuer à jouer et garder le rythme »
      tl.to(["#tag-treve", "#tag-coupe", "#tag-annule", "#tag-semaine"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, T.preparer + 0.3);
      tl.to("#tel", { opacity: 0.18, scale: 0.94, duration: 0.4 }, T.preparer + 0.2);
      tl.fromTo("#compos", { opacity: 0, x: 700, rotation: 3 }, { opacity: 1, x: 0, rotation: 0, duration: 0.5, ease: "power3.out" }, T.preparer + 0.2);
      tl.to("#t-rubrique-2", { opacity: 0, duration: 0.2 }, T.jouer10 - 0.7);
      tl.set("#t-titre-2", { opacity: 1 }, T.jouer10 - 0.5);
      apparaitre("#t2-l1", T.jouer10 - 0.5);
      apparaitre("#t2-l2", T.rythme - 0.5);
      // Retour plein cadre
      const SORTIE = T.rythme + 0.15;
      tl.to(["#compos", "#t-titre-2"], { opacity: 0, duration: 0.25 }, SORTIE);
      tl.to("#tel", { opacity: 0, y: 500, duration: 0.45, ease: "power3.in" }, SORTIE);
      tl.to("#mode-tel", { opacity: 0, duration: 0.3 }, SORTIE + 0.25);
      versPleinCadre(SORTIE);

      // ── SCÈNE 11 : « envoie cette vidéo à ton coach… je vais jouer ! » ──
      tl.fromTo("#envoie .pastille", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, T.coach11 - 0.9);
      tl.to("#envoie .pastille", { opacity: 0, duration: 0.25 }, T["350b"] - 0.75);
      tl.fromTo("#bulle-2", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.3, ease: "back.out(2)" }, T["350b"] - 0.6);
      tl.to("#bulle-2", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, T.jouer2 - 0.3);

      // ── CARTON FINAL ──
      const FIN = 49.55;
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
