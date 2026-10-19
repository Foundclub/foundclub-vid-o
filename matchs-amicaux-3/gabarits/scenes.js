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

      // ── 1 : L'EXTRAIT — l'accroche « Pas de match ce week-end ? » ──
      tl.fromTo("#accroche .bulle", { opacity: 0, scale: 0.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.35, ease: "back.out(2)" }, 0.25);
      tl.to("#accroche .bulle", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, 1.15);
      tl.to("#accroche .bulle", { scale: 1.05, duration: 0.12, yoyo: true, repeat: 1 }, 3.1);
      tl.to("#accroche .bulle", { opacity: 0, scale: 0.8, duration: 0.2 }, VOLET);

      // ── LE VOLET BLEU « On a la solution ! » : il couvre le passage de l'extrait au joueur ──
      tl.fromTo("#volet", { xPercent: 110 }, { xPercent: 0, duration: 0.24, ease: "power3.out" }, VOLET);
      tl.fromTo("#volet .icone-fc", { opacity: 0, scale: 0.4, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(1.8)" }, VOLET + 0.1);
      tl.fromTo("#volet .phrase", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, VOLET + 0.15);
      tl.to("#volet", { xPercent: -110, duration: 0.26, ease: "power3.in" }, VOLET + 0.62);

      // ── 2 : LE JOUEUR — « tu cherches des matchs amicaux ? », puis FoundClub ──
      tl.set("#j-titre", { opacity: 1 }, T.cherches - 0.45);
      apparaitre("#j-titre .ligne", T.cherches - 0.45);
      surligner("#j-titre", T.amicaux - 0.55);
      tl.to("#j-titre", { opacity: 0, y: -30, duration: 0.25 }, T.club - 0.75);
      tl.set("#logo", { opacity: 1 }, T.club - 0.6);
      tl.fromTo("#logo .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, T.club - 0.6);
      tl.fromTo("#logo .marque", { opacity: 0, y: 30, scale: 1.15 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, T.club - 0.35);
      tl.fromTo("#logo .reflet", { x: 0 }, { x: 900, duration: 0.7, ease: "power2.inOut" }, T.club + 0.05);

      // ── 3 : LE TÉLÉPHONE — le joueur s'efface, l'appli prend tout l'écran ──
      tl.to("#logo", { opacity: 0, duration: 0.3 }, TEL);
      tl.to("#cadre-video", { scale: 0.86, opacity: 0, duration: 0.45, ease: "power2.in" }, TEL);
      tl.to("#degrades", { opacity: 0, duration: 0.3 }, TEL);
      tl.to("#mode-tel", { opacity: 1, duration: 0.3 }, TEL + 0.1);
      tl.fromTo("#tel", { opacity: 0, y: 500, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, TEL + 0.15);
      apparaitre("#t-rubrique", TEL + 0.45, { x: -40 });
      tl.set("#t-titre", { opacity: 1 }, TEL + 0.55);
      apparaitre("#t-l1", TEL + 0.55);
      apparaitre("#t-l2", TEL + 0.85);
      // les extraits de l'enregistrement d'écran, l'un après l'autre (le 2e finit sur l'écran « Créer un match amical », figé)
      EXTRAITS.forEach((x, i) => {
        tl.fromTo(`#x-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, x.debut);
        tl.to(`#x-${i}`, { opacity: 0, duration: 0.01 }, x.debut + x.duree - 0.01);
      });
      tl.set("#cap-creer", { opacity: 1 }, EXTRAITS[1].debut + EXTRAITS[1].duree - 0.02);
      tl.set("#cap-creer", { opacity: 0 }, EXTRAITS[2].debut + 0.01);
      // « tu pourras trouver des matchs amicaux et publier ta propre annonce »
      appuyer("#appui-amicaux", T.trouver - 0.3);
      etiquette("#tag-trouve", T.amicaux2 - 0.45, -1);
      etiquette("#tag-publie", T.publier - 0.35, 1);
      appuyer("#appui-creer", T.publier - 0.05);
      tl.to("#cap-creer", { scale: 1.03, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 52%" }, T.publier + 0.1);
      // puis, sans voix : on propose un match, et c'est envoyé
      tl.to(["#tag-trouve", "#tag-publie"], { opacity: 0, scale: 0.7, duration: 0.25, stagger: 0.04 }, EXTRAITS[2].debut - 0.15);
      etiquette("#tag-propose", EXTRAITS[2].debut + 0.15, -1);
      appuyer("#appui-proposer", EXTRAITS[3].debut - 0.2);
      tl.to("#tag-propose", { opacity: 0, scale: 0.7, duration: 0.25 }, EXTRAITS[4].debut - 0.1);
      etiquette("#tag-envoye", EXTRAITS[4].debut + 0.75, 1);   // quand « Félicitations » s'affiche
      tl.to("#tel", { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1 }, EXTRAITS[4].debut + 0.75);

      // ── CARTON FINAL ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
