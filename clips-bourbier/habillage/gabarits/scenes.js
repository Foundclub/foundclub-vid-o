      // Accroche : la ligne blanche glisse, la ligne jaune claque juste après
      tl.fromTo("#etiquettes", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, 0.05);
      tl.fromTo("#titre .l1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.1);
      tl.fromTo("#titre .l2", { opacity: 0, scale: 0.6, rotation: -4 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.4, ease: "back.out(2.2)" }, 0.35);
      tl.to("#titre .l2", { scale: 1.06, duration: 0.15, yoyo: true, repeat: 1, ease: "power1.out" }, 1.0);
      // Barre de progression sous la vidéo
      tl.fromTo("#progression", { scaleX: 0 }, { scaleX: 1, duration: DUREE_VIDEO, ease: "none" }, 0);
      // Sous-titres : la phrase apparaît, chaque mot passe en jaune quand il est dit (répartition au nombre de lettres)
      PHRASES.forEach(([debut, fin, poids], i) => {
        const sel = "#st-" + i;
        tl.fromTo(sel, { opacity: 0, y: 16, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.12, ease: "power2.out" }, debut);
        tl.to(sel, { opacity: 0, duration: 0.06, ease: "none" }, Math.max(debut + 0.2, fin - 0.06));  // éteinte avant que la suivante arrive : pas de chevauchement
        const total = poids.reduce((a, b) => a + b, 0);
        let t = debut;
        poids.forEach((p, k) => { tl.set(sel + "-" + k, { className: "m dit" }, t); t += (fin - debut) * p / total; });
      });
      // Carton final : l'appel, puis la vignette de l'épisode qui monte, le bouton lecture qui bat
      tl.fromTo("#fin", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, DEBUT_FIN);
      tl.fromTo("#fin-appel .a1", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, DEBUT_FIN + 0.1);
      tl.fromTo("#fin-appel .a2", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, DEBUT_FIN + 0.3);
      tl.fromTo("#fin-appel .a3", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, DEBUT_FIN + 0.5);
      tl.fromTo("#fin-vignette", { opacity: 0, y: 160, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "power3.out" }, DEBUT_FIN + 0.6);
      tl.fromTo("#fin-play", { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(2.4)" }, DEBUT_FIN + 0.95);
      tl.to("#fin-play", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, DEBUT_FIN + 1.45);
      tl.fromTo(["#fin-titre", "#fin-chaine"], { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.12, ease: "power2.out" }, DEBUT_FIN + 1.0);
