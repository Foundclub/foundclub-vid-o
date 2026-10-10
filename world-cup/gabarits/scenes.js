      // ── Outils communs ─────────────────────────────────────────────
      SOUS_TITRES.forEach(([debut, fin], i) => {
        tl.fromTo(`#st-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.08, ease: "none" }, debut);
        tl.to(`#st-${i}`, { opacity: 0, duration: 0.08, ease: "none" }, fin - 0.08);
      });
      tl.set("#medaillon-anneau", { scale: 0.6 }, 0);
      const versMedaillon = (t) => {
        tl.to("#degrade-bas", { opacity: 0, duration: 0.4 }, t);
        tl.to("#degrade-haut", { opacity: 0, duration: 0.4 }, t);
        tl.to("#cadre-video", { clipPath: "circle(470px at 540px 760px)", scale: 0.33, x: 360, y: -510, duration: 0.8, ease: "power3.inOut" }, t);
        tl.to("#medaillon-anneau", { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, t + 0.7);
      };
      const versPleinCadre = (t) => {
        tl.to("#medaillon-anneau", { opacity: 0, scale: 0.6, duration: 0.25 }, t);
        tl.to("#cadre-video", { clipPath: "circle(2300px at 540px 760px)", scale: 1, x: 0, y: 0, duration: 0.7, ease: "power3.inOut" }, t);
        tl.to(["#degrade-bas", "#degrade-haut"], { opacity: 1, duration: 0.5 }, t + 0.3);
      };
      const entrer = (sel, t, de = { y: 40 }) => tl.fromTo(sel, { opacity: 0, ...de }, { opacity: 1, x: 0, y: 0, duration: 0.35, ease: "power3.out" }, t);
      const sortir = (sel, t) => tl.to(sel, { opacity: 0, duration: 0.25, ease: "power2.in" }, t);
      const titre = (sel, tLigne, tSurligne) => {   // un titre plein cadre : la ligne, puis le mot surligné
        tl.set(sel, { opacity: 1 }, tLigne);
        tl.fromTo(`${sel} .ligne`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, tLigne);
        if (tSurligne !== undefined) {
          tl.fromTo(`${sel} .fond`, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, tSurligne);
          tl.fromTo(`${sel} .mot`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, tSurligne + 0.1);
        }
      };
      const etiquette = (sel, t, cote) => tl.fromTo(sel, { opacity: 0, x: cote * 160, scale: 0.8 }, { opacity: 1, x: 0, scale: 1, duration: 0.32, ease: "back.out(1.7)" }, t);
      const appuyer = (sel, t) => {
        tl.fromTo(sel, { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 0.85, duration: 0.22, ease: "power2.out" }, t);
        tl.to(sel, { opacity: 0, scale: 1.25, duration: 0.3, ease: "power1.in" }, t + 0.32);
      };
      const montrer = (sel, t, effet = "glisse") => tl.fromTo(sel, effet === "glisse" ? { opacity: 0, x: 500 } : effet === "monte" ? { opacity: 0, y: 300 } : { opacity: 0 },
        { opacity: 1, x: 0, y: 0, duration: 0.32, ease: "power2.out" }, t);
      const puces = (sel, temps) => temps.forEach((t, i) => tl.fromTo(`${sel} > :nth-child(${i + 1})`, { opacity: 0, y: 30, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, t));

      // ── SCÈNE 1 : « dans pile un an, notre première Coupe du monde de football amateur » ──
      tl.fromTo("#j365", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.an - 0.45);
      titre("#s1-titre", T.coupe - 0.55, T.amateur - 0.5);
      sortir(["#j365", "#s1-titre"], T.participer + 0.5);

      // ── SCÈNE 2 : « avec ton club, ou simplement avec tes potes » ──
      puces("#s2-rang", [T.club - 0.4, T.potes - 0.4]);
      sortir("#s2-rang > *", T.potes + 0.6);

      // ── SCÈNE 3 : « un défi un peu fou… ouvert à tous, peu importe ton niveau » ──
      titre("#s3-titre", T.defi - 0.45, T.fou - 0.35);
      sortir("#s3-titre", T.mondial - 0.75);
      titre("#s3b-titre", T.mondial - 0.6, T.tous - 0.45);
      puces("#s3-niveaux", [T.niveau - 0.7, T.niveau - 0.55, T.niveau - 0.4, T.niveau - 0.25]);
      sortir(["#s3b-titre", "#s3-niveaux > *"], T.niveau + 0.65);

      // ── SCÈNES 4 À 7 : médaillon ───────────────────────────────────
      const ECRAN1 = T.simple - 1.05;
      versMedaillon(ECRAN1);
      tl.to("#ecran1", { opacity: 1, duration: 0.3 }, ECRAN1 + 0.3);
      // Scène 4 : la carte du monde en points, les pays qui s'allument, le tableau qui se resserre
      entrer("#c-rub", ECRAN1 + 0.45, { x: -40 });
      tl.fromTo("#carte-points", { opacity: 0 }, { opacity: 1, duration: 0.6 }, ECRAN1 + 0.4);
      entrer("#c-l1", T.qualification - 0.6);
      entrer("#c-l2", T.pays - 0.4);
      HUBS.forEach((h, i) => tl.to(`.h${i}`, { opacity: 1, fill: "#ffffff", duration: 0.2 }, T.qualification - 0.3 + i * ((T.pays - T.qualification + 0.6) / HUBS.length)));
      tl.fromTo("#tableau .equipe", { opacity: 0, scale: 0.6, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.25, stagger: 0.05 }, T.affronter - 0.6);
      tl.fromTo("#tableau .tour1", { strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, T.affronter - 0.1);
      tl.fromTo("#tableau .tour2", { strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, T.tours - 0.3);
      tl.fromTo("#tableau .tour3", { strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, T.meilleur - 0.5);
      tl.fromTo("#tableau .vainqueur", { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, T.chaque - 0.1);
      // Scène 5 : « en France pour disputer les phases finales »
      sortir(["#c-rub", "#c-l1", "#c-l2", "#tableau"], T.france - 0.9);
      tl.to("#carte-points circle", { opacity: 0.12, duration: 0.5 }, T.france - 0.8);
      tl.to("#carte", { scale: 4.2, y: 140, transformOrigin: "507px 171px", duration: 1.0, ease: "power3.inOut" }, T.france - 0.8);
      tl.to("#france-fine", { opacity: 1, duration: 0.5 }, T.france - 0.3);
      tl.fromTo("#epingle", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, y: 140, duration: 0.35, ease: "back.out(2)" }, T.france);
      entrer("#f-rub", T.france - 0.6, { x: -40 });
      entrer("#f-l1", T.finales - 0.6);
      entrer("#f-l2", T.finales - 0.3);
      // Scène 6 : « bonne nouvelle : les inscriptions sont déjà ouvertes »
      tl.fromTo("#tampon-ouvert", { opacity: 0, scale: 2.4, rotation: -18, xPercent: -50, yPercent: -50 },
        { opacity: 1, scale: 1, rotation: -7, xPercent: -50, yPercent: -50, duration: 0.25, ease: "power3.in" }, T.ouvertes - 0.45);
      tl.to("#carte", { x: 10, duration: 0.05, yoyo: true, repeat: 3, ease: "none" }, T.ouvertes - 0.2);
      // Scène 7 : le téléphone — la page World Cup (maquette), l'inscription de l'équipe, la création d'équipe
      const TEL = T.ouvertes + 0.55;
      sortir(["#f-rub", "#f-l1", "#f-l2", "#tampon-ouvert", "#epingle", "#carte"], TEL);
      tl.fromTo("#tel", { opacity: 0, y: 500, rotation: 6 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "power3.out" }, TEL + 0.1);
      montrer("#m-wc", TEL + 0.1, "fondu");
      // le compte à rebours de la page World Cup démarre à 365 jours
      const cd = { s: 0 }, el = (id) => document.getElementById(id), deux = (n) => String(n).padStart(2, "0");
      const afficherCompte = () => {
        const reste = 365 * 86400 - Math.floor(cd.s);
        el("cd-j").textContent = String(Math.floor(reste / 86400));
        el("cd-h").textContent = deux(Math.floor((reste % 86400) / 3600));
        el("cd-m").textContent = deux(Math.floor((reste % 3600) / 60));
        el("cd-s").textContent = deux(reste % 60);
      };
      tl.fromTo(cd, { s: 0 }, { s: 6, duration: 6, ease: "none", onUpdate: afficherCompte }, TEL + 0.9);
      entrer("#i-rub", TEL + 0.3, { x: -40 });
      etiquette("#tag-rejoins", T.equipe - 0.5, -1);
      // « ton coach peut directement inscrire ton équipe… et inviter tous ses joueurs »
      entrer("#i-l1", T.coach - 0.3);
      entrer("#i-l2", T.inscrire2 - 0.3);
      etiquette("#tag-coach", T.coach - 0.2, 1);
      appuyer("#appui-inscrire", T.inscrire2 - 0.55);
      montrer("#m-choix", T.inscrire2 - 0.2, "monte");
      appuyer("#appui-choix", T.inscrire2 + 0.25);
      appuyer("#appui-valider", T.joueurs - 1.0);
      sortir(["#m-wc", "#m-choix"], T.joueurs - 0.6);
      montrer("#m-ok", T.joueurs - 0.6, "fondu");
      etiquette("#tag-invite", T.joueurs - 0.4, -1);
      appuyer("#appui-inviter", T.joueurs + 0.1);
      // « si tu préfères jouer avec tes potes, tu peux aussi créer ta propre équipe » : les vrais écrans de création
      sortir(["#tag-rejoins", "#tag-coach", "#tag-invite", "#i-l1", "#i-l2"], T.potes2 - 0.5);
      etiquette("#tag-potes", T.potes2 - 0.4, 1);
      entrer("#i-l3", T.creer - 0.4);
      entrer("#i-l4", T.equipe2 - 0.4);
      const etapes = ["#cap-nom", "#cap-section", "#cap-sport", "#cap-categorie", "#cap-niveau"];
      const debutCreation = T.creer - 0.6, pasCreation = Math.max(0.42, (T.maintenant - 0.5 - debutCreation) / etapes.length);
      etapes.forEach((sel, i) => {
        montrer(sel, debutCreation + i * pasCreation);
        if (i > 0) sortir(etapes[i - 1], debutCreation + i * pasCreation + 0.3);
      });
      // « inscris-toi, fais inscrire ton équipe, et partage cette vidéo »
      sortir(["#tag-potes", "#i-l3", "#i-l4"], T.maintenant - 0.4);
      sortir(etapes[etapes.length - 1], T.inscris + 0.2);
      tl.fromTo("#m-ok", { opacity: 0, x: 500 }, { opacity: 1, x: 0, duration: 0.32, ease: "power2.out", immediateRender: false }, T.inscris - 0.1);
      etiquette("#tag-inscris", T.inscris - 0.4, -1);
      etiquette("#tag-equipe", T.equipe3 - 0.4, 1);
      etiquette("#tag-partage", T.partage - 0.4, -1);
      const SORTIE1 = T.participer3 + 0.15;
      sortir(["#tag-inscris", "#tag-equipe", "#tag-partage", "#i-rub"], SORTIE1);
      tl.to("#tel", { opacity: 0, y: 500, duration: 0.45, ease: "power3.in" }, SORTIE1);
      tl.to("#ecran1", { opacity: 0, duration: 0.3 }, SORTIE1 + 0.3);
      versPleinCadre(SORTIE1);

      // ── SCÈNES 8 ET 9 : « mais pourquoi ? » ─────────────────────────
      tl.set("#s8-titre", { opacity: 1 }, T.pourquoi - 0.55);
      tl.fromTo("#s8-titre .ligne", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }, T.pourquoi - 0.55);
      sortir("#s8-titre", T.pourquoi + 0.6);
      titre("#s9-titre", T.accessible - 1.1, T.accessible - 0.55);
      sortir("#s9-titre", T["365"] - 1.2);
      titre("#s9b-titre", T["365"] - 0.7, T.besoin - 0.6);
      sortir("#s9b-titre", T.besoin + 0.7);

      // ── SCÈNES 10 ET 11 : médaillon ────────────────────────────────
      const ECRAN2 = T.equipes - 0.95;
      versMedaillon(ECRAN2);
      tl.to("#ecran2", { opacity: 1, duration: 0.3 }, ECRAN2 + 0.3);
      entrer("#b-rub", ECRAN2 + 0.4, { x: -40 });
      entrer("#b-l1", ECRAN2 + 0.5);
      entrer("#b-l2", ECRAN2 + 0.65);
      ["equipes", "terrains", "arbitres", "partenaires", "communaute"].forEach((mot, i) => {
        tl.fromTo(`#besoin-${i}`, { opacity: 0, y: -120, rotation: i % 2 ? 4 : -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.35, ease: "back.out(1.6)" }, T[mot] - 0.45);
      });
      tl.fromTo("#besoin-4 .sous", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.entier - 0.6);
      sortir(["#besoins", "#b-rub", "#b-l1", "#b-l2"], T.prochaine - 0.9);
      entrer("#e-rub", T.prochaine - 0.7, { x: -40 });
      tl.fromTo("#episode", { opacity: 0, y: 200, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }, T.prochaine - 0.6);
      entrer("#e-l1", T.etape - 0.9);
      entrer("#e-l2", T.etape - 0.4);
      tl.fromTo("#episode .trait", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.25, stagger: 0.18 }, T.etape - 0.5);
      tl.to("#episode .pt", { backgroundColor: "#01b3f4", duration: 0.12, stagger: 0.18 }, T.etape - 0.35);
      const SORTIE2 = T.etape + 0.35;
      tl.to("#ecran2", { opacity: 0, duration: 0.3 }, SORTIE2 + 0.3);
      versPleinCadre(SORTIE2);

      // ── SCÈNES 12 ET 13 : « envoie cette vidéo… à vous de jouer » ──
      tl.fromTo("#envoie .pastille", { opacity: 0, scale: 0.6, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(1.8)" }, T.coach3 - 1.0);
      puces("#s12-rang", [T.coach3 - 0.4, T.coequipiers - 0.4, T.potes3 - 0.4]);
      tl.to("#envoie .pastille", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, T.maximum - 0.3);
      sortir(["#envoie .pastille", "#s12-rang > *"], T.maximum + 0.5);
      titre("#s13-titre", T.mondial4 - 0.9, T.jouer - 0.6);

      // ── CARTON FINAL ──
      const FIN = T.jouer + 0.25;
      tl.fromTo("#fin-voile", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power2.out" }, FIN);
      tl.fromTo("#fin .icone-fc", { opacity: 0, scale: 0.3, rotation: -12 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, FIN + 0.25);
      tl.fromTo("#fin .marque", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, FIN + 0.45);
      tl.fromTo("#fin .reflet", { x: 0 }, { x: 1100, duration: 0.8, ease: "power2.inOut" }, FIN + 0.9);
      tl.fromTo("#fin .phrase", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 0.8);
      tl.fromTo("#fin .badges", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, FIN + 1.05);
      tl.fromTo("#fin .site", { opacity: 0 }, { opacity: 1, duration: 0.4 }, FIN + 1.3);
