      // Sous-titres
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.08, ease: "none" }, fin - 0.08);
      });

      // Passage plein cadre ⇄ médaillon (ach10 en haut à droite ; son visage est centré vers y = 860)
      const versMedaillon = (t) => {
        tl.to("#degrade-bas", { opacity: 0, duration: 0.4 }, t);
        tl.to("#cadre-video", { clipPath: "circle(440px at 540px 860px)", scale: 0.35, x: 360, y: -610, duration: 0.8, ease: "power3.inOut" }, t);
        tl.to("#medaillon-anneau", { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, t + 0.7);
      };
      const versPleinCadre = (t) => {
        tl.to("#medaillon-anneau", { opacity: 0, scale: 0.6, duration: 0.25 }, t);
        tl.to("#cadre-video", { clipPath: "circle(2300px at 540px 860px)", scale: 1, x: 0, y: 0, duration: 0.7, ease: "power3.inOut" }, t);
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
      // la coupure de presse tombe sur la table, puis le surligneur passe sur les mots qui comptent
      const plaquer = (sel, t, rot) => tl.fromTo(sel, { opacity: 0, scale: 1.4, rotation: rot * 3 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.28, ease: "power3.in" }, t);
      const marquer = (sel, t) => tl.fromTo(sel, { backgroundSize: "0% 100%" }, { backgroundSize: "100% 100%", duration: 0.35, ease: "power2.inOut", stagger: 0.3 }, t);

      // ── SCÈNE 1 : les pros se plaignent — deux vrais titres de presse ──
      const P0 = 0.15;
      versMedaillon(P0);
      tl.to("#mode-presse", { opacity: 1, duration: 0.3 }, P0 + 0.2);
      apparaitre("#p-rubrique", P0 + 0.3, { x: -40 });
      plaquer("#art-1", P0 + 0.35, -2.5);
      tl.to("#mode-presse", { x: 8, duration: 0.04, yoyo: true, repeat: 3, ease: "none" }, P0 + 0.63);
      marquer("#art-1 .mq", P0 + 0.8);
      tl.fromTo("#art-2", { opacity: 0, x: 760, rotation: 9 }, { opacity: 1, x: 0, rotation: 2, duration: 0.4, ease: "power3.out" }, T.plaignent - 0.5);
      marquer("#art-2 .mq", T.plaignent - 0.05);
      tl.fromTo("#p-titre .ligne", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", stagger: 0.35 }, T.jours - 0.85);

      // ── SCÈNES 2 ET 3 : le calendrier des amateurs, puis un vrai titre de presse locale ──
      const CAL = T.jours + 0.55;
      tl.to(["#art-1", "#art-2"], { opacity: 0, x: -760, rotation: -10, duration: 0.35, ease: "power3.in", stagger: 0.06 }, CAL - 0.15);
      tl.to(["#p-rubrique", "#p-titre"], { opacity: 0, x: -40, duration: 0.25 }, CAL - 0.15);
      tl.to("#mode-cal", { opacity: 1, duration: 0.3 }, CAL);
      apparaitre("#calendrier", CAL + 0.1, { y: 300 });
      apparaitre("#c-rubrique-amat", T.amateur - 0.75, { x: -40 });
      apparaitre("#c-titre-amat", T.mois - 0.55);
      tl.to("#calendrier .compteur", { scale: 1.3, duration: 0.12, yoyo: true, repeat: 1 }, T.mois - 0.1);
      // Coupe, reportés, trêve : trois tampons sur les week-ends
      [["#t-coupe", T.coupe], ["#t-reporte", T.reportes], ["#t-treve", T.treve]].forEach(([sel, t]) => {
        tl.fromTo(sel, { opacity: 0, scale: 2.2, rotation: -20, xPercent: -50, yPercent: -50 }, { opacity: 1, scale: 1, rotation: -8, xPercent: -50, yPercent: -50, duration: 0.22, ease: "power3.in" }, t - 0.35);
      });
      tl.to("#calendrier", { x: 8, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.treve - 0.13);
      // « des fois pendant un mois on joue pas » : la presse locale en parle
      plaquer("#art-3", T.mois2 - 1.25, -1.5);
      marquer("#art-3 .mq", T.mois2 - 0.85);
      surligner("#sans-match", T.mois2 - 0.4);
      const S4 = T.mois2 + 0.4;
      tl.to("#mode-cal", { opacity: 0, duration: 0.3 }, S4 - 0.1);
      versPleinCadre(S4 - 0.1);

      // ── SCÈNE 4 : la licence jusqu'à 550 €, puis « la vie de ma mère, je vais jouer ! » ──
      apparaitre("#licence", S4 + 0.3, { y: -60 });
      const prix = { v: 0 }, elPrix = document.getElementById("prix");
      tl.fromTo(prix, { v: 0 }, { v: 550, duration: 1.1, ease: "power2.out", onUpdate: () => { elPrix.textContent = String(Math.round(prix.v)); } }, T["550"] - 1.1);
      tl.to("#licence", { scale: 1.06, duration: 0.12, yoyo: true, repeat: 1 }, T["550"]);
      tl.to("#licence", { scale: 1.06, duration: 0.12, yoyo: true, repeat: 1 }, T.mere - 1.45);
      tl.to("#licence", { opacity: 0, y: -40, duration: 0.25 }, T.mere - 0.95);
      tl.fromTo("#bulle-1", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.3, ease: "back.out(2)" }, T.mere - 0.8);
      tl.to("#bulle-1", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, T.jouer - 0.3);

      // ── L'EXTRAIT DE RÉFÉRENCE (coupe franche, l'image d'ach10 s'arrête) ──
      tl.fromTo("#insert-cadre", { scale: 0.9 }, { scale: 1, duration: 0.25, ease: "power3.out" }, COUPE);

      // ── SCÈNE 5 : « mais c'est quoi la raison ? » ──
      apparaitre("#s5-titre .ligne", REPRISE_T + 0.05);
      surligner("#s5-titre", T.raison - 0.5);

      // ── SCÈNE 6 : toujours la même excuse ──
      tl.fromTo("#excuse-titre span", { opacity: 0, scale: 0.6, rotation: -5 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.35, ease: "back.out(1.8)" }, T.coachs - 0.35);
      tl.to("#excuse-titre span", { opacity: 0, y: -30, duration: 0.25 }, T.contre - 0.85);
      apparaitre("#galere-qui", T.contre - 0.6, { x: -200 });
      apparaitre("#galere-orga", T.organiser - 0.6, { x: 200 });
      apparaitre("#galere-lieu", T.exterieur - 1.2, { x: -200 });
      tl.to("#s6 .croix", { scale: 1.2, duration: 0.12, yoyo: true, repeat: 1, stagger: 0.06 }, T.exterieur);

      // ── SCÈNE 7 : « plus d'excuses » — elles sont rayées, puis FoundClub ──
      tl.fromTo("#s6 .barre-rouge", { scaleX: 0 }, { scaleX: 1, duration: 0.2, ease: "power2.out", stagger: 0.08 }, T.excuses - 0.8);
      tl.fromTo("#plus-excuses", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power3.in" }, T.excuses - 0.45);
      tl.to("#s6", { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.excuses - 0.23);
      tl.to(["#galere-qui", "#galere-orga", "#galere-lieu", "#plus-excuses"], { opacity: 0, y: -30, duration: 0.25, stagger: 0.03 }, T.outil + 0.3);
      tl.fromTo("#logo .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, T.found - 0.6);
      tl.fromTo("#logo .marque", { opacity: 0, y: 30, scale: 1.15 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, T.found - 0.3);
      tl.fromTo("#logo .reflet", { x: 0 }, { x: 900, duration: 0.7, ease: "power2.inOut" }, T.found + 0.15);

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
      tl.set("#t-titre-1", { opacity: 1 }, TEL + 0.8);
      apparaitre("#t1-l1", TEL + 0.8);
      apparaitre("#t1-l2", T.disponible - 0.45);
      etiquette("#tag-weekend", T.week - 0.35, -1);
      etiquette("#tag-domicile", T.domicile2 - 0.4, 1);
      etiquette("#tag-exterieur", T.exterieur2 - 0.4, -1);
      const FILE = EXTRAITS[EXTRAITS.length - 1];
      const APRES = FILE.debut + FILE.duree;
      tl.to(["#tag-weekend", "#tag-domicile", "#tag-exterieur"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, APRES - 0.6);
      tl.to(["#t-rubrique-1", "#t-titre-1"], { opacity: 0, x: -40, duration: 0.25 }, APRES - 0.5);

      // Scène 10 : l'autre coach accepte → le match est au planning ; les étiquettes suivent ses mots
      const montrer = (sel, t) => tl.fromTo(sel, { opacity: 0, x: 500 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }, t);
      const cacher = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.25 }, t);
      montrer("#cap-proposition", APRES);
      apparaitre("#t-rubrique-2", APRES + 0.1, { x: -40 });
      appuyer("#appui-accepter", T.coupe2 - 0.1);
      cacher("#cap-proposition", T.coupe2 + 0.35);
      montrer("#cap-accepter", T.coupe2 + 0.35);
      appuyer("#appui-confirmer", T.treve2 - 0.2);
      cacher("#cap-accepter", T.treve2 + 0.2);
      montrer("#cap-planning", T.treve2 + 0.2);
      etiquette("#tag-reporte", T.reporte2 - 0.4, -1);
      etiquette("#tag-coupe", T.coupe2 - 0.4, 1);
      etiquette("#tag-treve", T.treve2 - 0.4, -1);
      etiquette("#tag-semaine", T.semaine - 0.4, 1);
      // « continuer à jouer et garder le rythme »
      tl.to(["#tag-reporte", "#tag-coupe", "#tag-treve", "#tag-semaine"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, T.continuer - 0.6);
      tl.to("#t-rubrique-2", { opacity: 0, duration: 0.2 }, T.continuer - 0.7);
      tl.to("#tel", { opacity: 0.18, scale: 0.94, duration: 0.4 }, T.continuer - 0.6);
      tl.set("#t-titre-2", { opacity: 1 }, T.continuer - 0.5);
      apparaitre("#t2-l1", T.continuer - 0.5);
      apparaitre("#t2-l2", T.rythme - 0.5);
      // Retour plein cadre
      const SORTIE = T.rythme + 0.5;
      tl.to("#t-titre-2", { opacity: 0, duration: 0.25 }, SORTIE);
      tl.to("#tel", { opacity: 0, duration: 0.3 }, SORTIE);
      tl.to("#mode-tel", { opacity: 0, duration: 0.3 }, SORTIE + 0.25);
      versPleinCadre(SORTIE);

      // ── SCÈNE 11 : « envoie la vidéo à ton coach… la tête de ma mère, je vais jouer ! » ──
      tl.fromTo("#envoie .pastille", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, T.coach - 0.9);
      tl.to("#envoie .pastille", { opacity: 0, duration: 0.25 }, T.licence2 - 0.95);
      tl.fromTo("#bulle-2", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.3, ease: "back.out(2)" }, T.licence2 - 0.8);
      tl.to("#bulle-2", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, T.jouer2 - 0.3);

      // ── CARTON FINAL ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
