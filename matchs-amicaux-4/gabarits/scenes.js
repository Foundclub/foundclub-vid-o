      // Sous-titres
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.08, ease: "none" }, fin - 0.08);
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

      // ── 1 : « On est en 2026… des coachs qui galèrent pendant des heures à trouver un match amical » ──
      tl.fromTo("#annee", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.24, ease: "power3.in" }, T["2026"] - 0.45);
      tl.to("#annee", { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T["2026"] - 0.21);
      tl.to("#annee", { opacity: 0, y: -40, duration: 0.25 }, T.coachs - 0.7);
      tl.set("#galere", { opacity: 1 }, T.coachs - 0.6);
      apparaitre("#galere .ligne", T.coachs - 0.6);
      surligner("#galere", T.heures - 0.55);
      tl.to("#galere .surligne", { x: 8, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.amical - 0.3);
      tl.to("#galere", { opacity: 0, y: -30, duration: 0.25 }, T.tombe - 0.65);

      // ── 2 : « Ça tombe bien, les vacances de la Toussaint arrivent » ──
      pastille("#toussaint .pastille", T.toussaint - 0.75);
      tl.to("#toussaint .pastille", { opacity: 0, y: -30, duration: 0.25 }, T.arrivent + 0.45);

      // ── 3 : « on vient d'ouvrir une nouvelle fonctionnalité sur FoundClub » ──
      tl.fromTo("#nouveau .pastille", { opacity: 0, y: -30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, T.fonctionnalite - 0.75);
      tl.set("#logo", { opacity: 1 }, T.fonctionnalite - 0.35);
      tl.fromTo("#logo .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, T.fonctionnalite - 0.35);
      tl.fromTo("#logo .marque", { opacity: 0, y: 30, scale: 1.15 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, T.club - 0.45);
      tl.fromTo("#logo .reflet", { x: 0 }, { x: 900, duration: 0.7, ease: "power2.inOut" }, T.club - 0.05);

      // ── 4 : LE TÉLÉPHONE — les joueurs s'effacent, l'appli prend tout l'écran ──
      tl.to(["#logo", "#nouveau .pastille"], { opacity: 0, duration: 0.3 }, TEL);
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
      tl.set("#cap-creer", { opacity: 1 }, EXTRAITS[1].debut + EXTRAITS[1].duree - 0.02);
      tl.set("#cap-creer", { opacity: 0 }, EXTRAITS[2].debut + 0.01);
      // « tu peux directement trouver des matchs amicaux ou publier ta propre annonce pour trouver des adversaires »
      appuyer("#appui-amicaux", T.amicaux - 0.45);
      etiquette("#tag-trouve", T.amicaux - 0.5, -1);
      etiquette("#tag-publie", T.annonce - 0.6, 1);
      appuyer("#appui-creer", T.annonce - 0.25);
      tl.to("#cap-creer", { scale: 1.03, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 52%" }, T.annonce - 0.1);
      tl.to(["#tag-trouve", "#tag-publie"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, EXTRAITS[2].debut - 0.1);
      etiquette("#tag-propose", EXTRAITS[2].debut + 0.1, -1);
      appuyer("#appui-proposer", EXTRAITS[2].debut + EXTRAITS[2].duree - 0.3);
      // Retour aux joueurs : « donc si t'es coach… »
      tl.to("#tel", { opacity: 0, y: 400, duration: 0.35, ease: "power3.in" }, RETOUR);
      tl.to("#mode-tel", { opacity: 0, duration: 0.3 }, RETOUR + 0.1);
      tl.fromTo("#cadre-video", { scale: 0.86, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "power3.out", immediateRender: false }, RETOUR + 0.1);
      tl.to("#degrades", { opacity: 1, duration: 0.3 }, RETOUR + 0.2);

      // ── 5 : « si t'es coach, va sur FoundClub et trouve ton prochain match » ──
      tl.set("#coach-titre", { opacity: 1 }, T.coach - 0.5);
      apparaitre("#coach-titre .ligne", T.coach - 0.5);
      surligner("#coach-titre", T.match - 0.6);
      tl.to("#coach-titre", { opacity: 0, y: -30, duration: 0.25 }, T.joueur - 0.6);

      // ── 6 : « et si t'es joueur, envoie cette vidéo à ton coach » ──
      pastille("#envoie .pastille", T.video - 0.75);
      tl.to("#envoie .pastille", { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.coach2 - 0.2);

      // ── CARTON FINAL ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
