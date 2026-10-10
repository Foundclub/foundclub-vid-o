      // ── SCÈNE 3 : « Mais aujourd'hui… une appli qui change ton club… c'est FoundClub » ──
      tl.fromTo("#s3-change .ligne", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.organisation1 - 0.45);
      tl.fromTo("#s3-change .fond", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, T.club1 - 0.4);
      tl.fromTo("#s3-change .mot", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, T.club1 - 0.3);
      tl.to("#s3-change", { opacity: 0, y: 50, duration: 0.3, ease: "power2.in", stagger: 0.05 }, T.app2 - 0.5);
      tl.fromTo("#s3-logo .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, T.foundclub - 1.0);
      tl.fromTo("#s3-logo .marque", { opacity: 0, y: 40, scale: 1.18 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, T.foundclub - 0.65);
      tl.fromTo("#s3-logo .reflet", { x: 0 }, { x: 1000, duration: 0.7, ease: "power2.inOut" }, T.foundclub - 0.1);
      tl.to("#s3-logo", { opacity: 0, scale: 0.85, duration: 0.3, ease: "power2.in" }, T.foundclub + 0.45);

      // ── PASSAGE EN « MODE ÉCRAN » : ach10 rétrécit en médaillon, le téléphone monte ──
      const ENTREE = T.foundclub + 0.5;
      tl.to("#degrade-fond", { opacity: 0, duration: 0.5 }, ENTREE);
      tl.fromTo("#cadre-video", { clipPath: "circle(2300px at 540px 700px)", scale: 1, x: 0, y: 0 },
        { clipPath: "circle(430px at 540px 700px)", scale: 0.35, x: 360, y: -450, duration: 0.8, ease: "power3.inOut" }, ENTREE);
      tl.fromTo("#medaillon-anneau", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, ENTREE + 0.75);
      tl.fromTo("#tel", { opacity: 0, y: 500, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, ENTREE + 0.6);

      // Les écrans de l'app : chacun remplace le précédent
      const montrer = (id, t, effet) => {
        const depart = effet === "glisse" ? { opacity: 0, x: 500 } : effet === "defile" ? { opacity: 0, y: 260 } : { opacity: 0 };
        tl.fromTo(id, depart, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power2.out" }, t);
      };
      const cacher = (id, t) => tl.to(id, { opacity: 0, duration: 0.25 }, t);
      montrer("#cap-accueil-haut", ENTREE + 0.6, "fondu");   // l'accueil d'abord (retour d'Adel)

      // ── SCÈNE 4 : « faciliter la communication et l'organisation entre le club, les joueurs… » ──
      tl.fromTo("#s4-rubrique", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.objectif - 0.3);
      tl.fromTo("#s4-l1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.communication - 0.45);
      tl.fromTo("#s4-l2", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.organisation2 - 0.45);
      [["#tag-club", T.club, -1], ["#tag-joueurs", T.joueurs, 1], ["#tag-dirigeants", T.dirigeants, -1], ["#tag-parents", T.parents, 1]].forEach(([id, t, cote]) => {
        tl.fromTo(id, { opacity: 0, x: cote * 160, scale: 0.8 }, { opacity: 1, x: 0, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, t - 0.4);
      });
      // Chaque étiquette affiche l'accueil correspondant
      cacher("#cap-accueil-haut", T.club - 0.4);       montrer("#cap-accueil-grille", T.club - 0.4, "defile");
      cacher("#cap-accueil-grille", T.joueurs - 0.4);  montrer("#cap-accueil-joueur", T.joueurs - 0.4, "glisse");
      cacher("#cap-accueil-joueur", T.dirigeants - 0.4); montrer("#cap-accueil-gerer", T.dirigeants - 0.4, "glisse");
      cacher("#cap-accueil-gerer", T.parents - 0.4); montrer("#cap-accueil-parent", T.parents - 0.4, "glisse");
      tl.to(["#s4-rubrique", "#s4-titre"], { opacity: 0, x: -40, duration: 0.3, ease: "power2.in" }, T.parents + 0.25);
      tl.to(["#tag-club", "#tag-joueurs", "#tag-dirigeants", "#tag-parents"], { opacity: 0, scale: 0.7, duration: 0.3, ease: "power2.in", stagger: 0.05 }, T.parents + 0.3);

      // ── SCÈNE 5 : les messages éparpillés… puis aspirés dans le téléphone ──
      cacher("#cap-accueil-parent", T.parents + 0.45);
      montrer("#cap-messagerie", T.parents + 0.45, "fondu");   // le canal du club remplace les groupes
      EPARPILLES.forEach((m, i) => {
        tl.fromTo(`#e-${i}`, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, m.t);
      });
      // Aspiration : chaque message file vers le centre de l'écran du téléphone
      EPARPILLES.forEach((m, i) => {
        tl.to(`#e-${i}`, { x: m.dx, y: m.dy, scale: 0.1, opacity: 0, duration: 0.45, ease: "power3.in" }, T.centraliser - 0.6 + i * 0.05);
      });
      tl.to("#tel", { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1, ease: "power1.out" }, T.centraliser + 0.05);
      cacher("#cap-messagerie", T.centraliser + 0.1);
      montrer("#cap-planning", T.centraliser + 0.1, "glisse");
      tl.fromTo("#s5-rubrique", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.centraliser - 0.4);
      tl.fromTo("#s5-l1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, T.endroit - 0.75);
      tl.fromTo("#s5-titre .fond", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, T.endroit - 0.45);
      tl.fromTo("#s5-titre .mot", { opacity: 0 }, { opacity: 1, duration: 0.2 }, T.endroit - 0.35);
      cacher("#cap-planning", T.endroit + 0.25);
      montrer("#cap-appel", T.endroit + 0.25, "glisse");
