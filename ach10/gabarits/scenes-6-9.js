      // ── SCÈNE 6a : « ne s'arrête pas seulement à la gestion de ton équipe » → les compos des 5 sports ──
      tl.to(["#s5-rubrique", "#s5-titre"], { opacity: 0, x: -40, duration: 0.3, ease: "power2.in" }, T.interessant - 0.3);
      tl.fromTo("#s6-rubrique", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.interessant - 0.1);
      tl.fromTo("#s6-l1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.seulement - 0.45);
      tl.fromTo("#s6-l2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.gestion - 0.4);
      tl.to("#tel", { opacity: 0.18, scale: 0.94, duration: 0.4, ease: "power2.out" }, T.gestion - 0.5);
      tl.fromTo("#compos", { opacity: 0, x: 700, rotation: 3 }, { opacity: 1, x: 0, rotation: 0, duration: 0.55, ease: "power3.out" }, T.gestion - 0.5);
      tl.to("#compos", { opacity: 0, x: -700, rotation: -3, duration: 0.45, ease: "power3.in" }, T.ambition - 0.55);
      tl.to(["#s6-rubrique", "#s6-titre"], { opacity: 0, x: -40, duration: 0.3, ease: "power2.in" }, T.ambition - 0.55);
      tl.to("#tel", { opacity: 1, scale: 1, duration: 0.4, ease: "power2.out" }, T.ambition - 0.25);

      // ── SCÈNE 6b : « faciliter la connexion entre les joueurs et les clubs » ──
      const appuyer = (id, t) => {
        tl.fromTo(id, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.22, ease: "power2.out" }, t);
        tl.to(id, { opacity: 0, scale: 1.25, duration: 0.3, ease: "power1.in" }, t + 0.32);
      };
      tl.fromTo("#s6b-rubrique", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.ambition - 0.2);
      tl.fromTo("#s6b-l1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.joueurs6 - 0.45);
      tl.fromTo("#s6b-l2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.clubs6 - 0.45);
      cacher("#cap-appel", T.ambition - 0.25);
      montrer("#cap-clubs", T.ambition - 0.25, "glisse");
      // la fiche du club, avec son numéro de téléphone flouté
      cacher("#cap-clubs", T.connexion - 0.35);
      montrer("#cap-fiche", T.connexion - 0.35, "fondu");
      montrer("#flou-tel", T.connexion - 0.35, "fondu");
      appuyer("#appui-rejoindre", T.connexion + 0.15);
      cacher(["#cap-fiche", "#flou-tel"], T.joueurs6 - 0.3);
      montrer("#cap-recrutement", T.joueurs6 - 0.3, "glisse");
      appuyer("#appui-postuler", T.joueurs6 + 0.25);
      // l'affiche de détection, avec le logo FC posé à la place de l'image cassée
      cacher("#cap-recrutement", T.clubs6 - 0.15);
      montrer("#cap-affiche", T.clubs6 - 0.15, "fondu");
      montrer("#logo-affiche", T.clubs6 - 0.15, "fondu");
      tl.to(["#s6b-rubrique", "#s6b-titre"], { opacity: 0, x: -40, duration: 0.3, ease: "power2.in" }, T.joueur - 0.6);

      // ── SCÈNE 7 : « que tu sois joueur, éducateur, président, dirigeant, parent » ──
      cacher(["#cap-affiche", "#logo-affiche"], T.joueur - 0.55);
      montrer("#cap-statut", T.joueur - 0.55, "glisse");
      tl.fromTo("#s7-rubrique", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.joueur - 0.5);
      // Ordonnées des 4 statuts de l'écran : Joueur·se, Entraîneur·e, Dirigeant·e, Parent
      const LIGNE_STATUT = { joueur: 0, educateur: 86, president: 173, dirigeant: 173, parent: 259 };
      tl.fromTo("#statut-cadre", { opacity: 0, scale: 1.1 }, { opacity: 1, scale: 1, duration: 0.2 }, T.joueur - 0.3);
      ["joueur", "educateur", "president", "dirigeant", "parent"].forEach((role, i) => {
        const cote = i % 2 === 0 ? -1 : 1;
        tl.fromTo(`#r-${role}`, { opacity: 0, x: cote * 160, scale: 0.8 }, { opacity: 1, x: 0, scale: 1, duration: 0.3, ease: "back.out(1.7)" }, T[role] - 0.35);
        if (i > 0) tl.to("#statut-cadre", { y: LIGNE_STATUT[role], duration: 0.22, ease: "power2.inOut" }, T[role] - 0.35);
      });

      // ── RETOUR PLEIN CADRE : le médaillon se rouvre sur ach10 ──
      const SORTIE = T.parent + 0.3;
      tl.to(["#s7-rubrique", "#statut-cadre", "#r-joueur", "#r-educateur", "#r-president", "#r-dirigeant", "#r-parent"], { opacity: 0, duration: 0.25 }, SORTIE - 0.1);
      tl.to("#tel", { opacity: 0, y: 500, rotation: 6, duration: 0.5, ease: "power3.in" }, SORTIE - 0.1);
      tl.to("#medaillon-anneau", { opacity: 0, scale: 0.6, duration: 0.25 }, SORTIE);
      tl.to("#cadre-video", { clipPath: "circle(2300px at 540px 700px)", scale: 1, x: 0, y: 0, duration: 0.7, ease: "power3.inOut" }, SORTIE);
      tl.to("#degrade-fond", { opacity: 1, duration: 0.5 }, SORTIE + 0.3);

      // ── SCÈNE 8 : la carte App Store recouvre sa bannière blanche (visible de 47,03 à 49,25 s) ──
      tl.fromTo("#carte-store", { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 0.16, ease: "power2.out" }, 46.85);
      tl.to("#carte-store", { opacity: 0, scale: 0.95, duration: 0.18, ease: "power2.in" }, 49.27);

      // ── SCÈNE 9 : « dis-moi en commentaire… encore WhatsApp, ou une application ? » ──
      tl.fromTo("#s9-sticker .pastille", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, Math.max(T.commentaire - 0.55, 49.35));
      tl.fromTo("#choix-whatsapp", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, T.whatsapp9 - 0.45);
      tl.fromTo("#choix-app", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, T.application9 - 0.55);
      tl.to("#choix-app", { scale: 1.05, duration: 0.15, yoyo: true, repeat: 1, ease: "power1.out" }, T.application9 - 0.1);
      tl.to(["#s9-sticker", "#choix-whatsapp", "#choix-app"], { opacity: 0, duration: 0.3 }, 53.95);

      // ── CARTON FINAL : « Ciao mes petits potes ! » ──
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, 54.0);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, 54.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 54.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, 54.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 54.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 55.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 55.3);
