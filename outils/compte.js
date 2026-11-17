/* Compte (Supabase) : section « Compte » des Réglages — inscription, connexion par code, changement d'adresse,
   export, effacement de la progression, suppression du compte, paramètres du projet Supabase */
const SBK = k => "zh:" + k;   // clés distantes propres au palais chinois (le projet Supabase peut être partagé avec d'autres palais)
const INP = 'font:inherit;font-size:16px;flex:1;min-width:12em;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)';
function sbCfgHtml(open) {
  const c = ls.get("sbcfg", {}), fromFile = !!((window.PM_CONFIG || {}).supabaseUrl);
  return `<details id="sbCfgBox"${open ? " open" : ""}><summary style="cursor:pointer;font-weight:600">Paramètres Supabase</summary>
    <p class="pr" style="margin:8px 0">URL du projet et clé « anon public » (Supabase → Project Settings → API). Cette clé est faite pour être publique : les règles de sécurité de la table <code>progress</code> empêchent chacun de lire la progression des autres.${fromFile ? " Des paramètres sont déjà fournis par la page ; ceux saisis ici les remplacent sur cet appareil." : ""}</p>
    <div class="frow"><label for="sbUrl">URL</label><input id="sbUrl" type="url" autocomplete="off" placeholder="https://xxxx.supabase.co" style="${INP}" value="${esc(c.supabaseUrl || "")}"></div>
    <div class="frow"><label for="sbKey">Clé anon</label><input id="sbKey" type="text" autocomplete="off" spellcheck="false" placeholder="eyJhbGciOi…" style="${INP}" value="${esc(c.supabaseKey || "")}"></div>
    <div class="btns"><button class="btn alt" type="button" id="sbCfgSave">Enregistrer et recharger</button>${c.supabaseUrl ? '<button class="chip" type="button" id="sbCfgClear">Retirer ces paramètres</button>' : ""}</div>
  </details>`;
}
function renderAccount(step) {
  const b = $("#acctSet"); if (!b) return;
  if (store.kind === "claude") { b.innerHTML = `<p style="margin:0">Ta progression est enregistrée avec ton compte Claude et suit tes appareils.</p>`; return; }
  if (!store.sb) {
    b.innerHTML = `<p style="margin:0">La connexion n'est pas configurée : ta progression reste dans ce navigateur. Renseigne les paramètres de ton projet Supabase pour pouvoir créer un compte et retrouver ta progression sur tous tes appareils.</p>` + sbCfgHtml(true);
    return;
  }
  if (store.kind === "sb") {
    b.innerHTML = `<p style="margin:0">Connecté avec <b>${esc(store.email)}</b>. Ta progression est enregistrée sur ton compte et suit tes appareils.</p>
      <div class="btns"><button class="btn alt" type="button" id="sbOut">Se déconnecter</button><button class="btn alt" type="button" id="sbExport">Exporter mes données</button></div>
      <h3 style="margin:6px 0 0">Changer d'adresse e-mail</h3>
      <div class="frow"><label for="sbNewEmail">Nouvelle adresse</label><input id="sbNewEmail" type="email" autocomplete="email" placeholder="prenom@exemple.fr" style="${INP}"></div>
      <div class="btns"><button class="btn alt" type="button" id="sbChange">Changer d'adresse</button></div>
      <h3 style="margin:6px 0 0">Effacer ou supprimer</h3>
      <div class="btns"><button class="btn danger" type="button" id="sbWipe">Effacer ma progression du compte…</button><button class="btn danger" type="button" id="sbDelete">Supprimer mon compte…</button></div>
      <div id="sbConfirm"></div>
      <p class="pr" id="sbMsg" style="margin:0"></p>` + sbCfgHtml(false);
    return;
  }
  if (step === "code") {
    b.innerHTML = `<p style="margin:0">Un code à 6 chiffres a été envoyé à <b>${esc(store.email)}</b>. Il peut mettre une minute à arriver ; pense aux courriers indésirables.</p>
      <div class="frow"><label for="sbCode">Code</label><input id="sbCode" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="6" style="font:inherit;font-size:20px;letter-spacing:.3em;width:7em;padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)"></div>
      <div class="btns"><button class="btn" type="button" id="sbVerify">Valider</button><button class="btn alt" type="button" id="sbBack">Changer d'adresse</button></div><p class="pr" id="sbMsg" style="margin:0"></p>`;
    setTimeout(() => $("#sbCode") && $("#sbCode").focus(), 50); return;
  }
  b.innerHTML = `<p style="margin:0">Crée un compte ou connecte-toi pour retrouver ta progression sur tous tes appareils. Pas de mot de passe : tu reçois un code à 6 chiffres par e-mail.</p>
    <div class="frow"><label for="sbEmail">E-mail</label><input id="sbEmail" type="email" autocomplete="email" placeholder="prenom@exemple.fr" style="${INP}" value="${esc(store.email)}"></div>
    <div class="btns"><button class="btn" type="button" id="sbSignup">Créer un compte</button><button class="btn alt" type="button" id="sbSend">Se connecter</button></div>
    <p class="pr" id="sbMsg" style="margin:0"></p>` + sbCfgHtml(false);
}
const sbMsg = t => { const m = $("#sbMsg"); if (m) m.textContent = t; };
async function sbSend(create) {
  const email = ($("#sbEmail").value || "").trim(); if (!/^\S+@\S+\.\S+$/.test(email)) { sbMsg("Adresse e-mail invalide."); return; }
  sbMsg("Envoi…"); const { error } = await store.sb.auth.signInWithOtp({ email, options: { shouldCreateUser: !!create } });
  if (error) {
    if (!create && /signups? not allowed|not found|user/i.test(error.message)) { sbMsg("Aucun compte avec cette adresse : utilise « Créer un compte »."); return; }
    sbMsg(error.status === 429 ? "Trop d'envois rapprochés : réessaie dans quelques minutes." : "Envoi impossible : " + error.message); return;
  }
  store.email = email; renderAccount("code");
}
async function sbVerify() {
  const token = ($("#sbCode").value || "").replace(/\D/g, ""); if (token.length < 6) { sbMsg("Le code fait 6 chiffres."); return; }
  sbMsg("Vérification…"); const { data, error } = await store.sb.auth.verifyOtp({ email: store.email, token, type: "email" });
  if (error || !data.session) { sbMsg("Code incorrect ou expiré. Redemande un code."); return; }
  await useSession(data.session);
}
async function sbOut() { await store.sb.auth.signOut(); store.kind = null; store.uid = null; store.cache = {}; $("#accountBtn").textContent = "Compte"; renderAccount(); toast("Déconnecté : la progression reste aussi sur cet appareil"); }
async function sbChange() {
  const email = ($("#sbNewEmail").value || "").trim(); if (!/^\S+@\S+\.\S+$/.test(email)) { sbMsg("Adresse e-mail invalide."); return; }
  sbMsg("Envoi…"); const { error } = await store.sb.auth.updateUser({ email });
  sbMsg(error ? "Changement impossible : " + error.message : `Un lien de confirmation a été envoyé à ${email} : l'adresse changera une fois le lien ouvert.`);
}
async function sbExport() {
  sbMsg("Préparation…");
  const { data, error } = await store.sb.from("progress").select("key,data,updated_at").like("key", "zh:%");
  if (error) { sbMsg("Export impossible : " + error.message); return; }
  const blob = new Blob([JSON.stringify({ palais: "chinois", email: store.email, export: new Date().toISOString(), lignes: data }, null, 1)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "progression-palais-chinois.json"; document.body.appendChild(a); a.click(); a.remove();
  sbMsg("Fichier téléchargé.");
}
function sbAsk(kind) {
  const del = kind === "delete", w = del ? "SUPPRIMER" : "EFFACER";
  $("#sbConfirm").innerHTML = `<p class="warnbox">⚠ ${del
    ? "Ton compte et toute la progression qui y est enregistrée seront supprimés définitivement, pour ce palais comme pour les autres palais qui utilisent le même compte. La progression gardée dans ce navigateur n'est pas touchée."
    : "La progression du palais chinois enregistrée sur ton compte (révisions, historique, notes) sera effacée définitivement. Ton compte reste ouvert, et ce navigateur garde sa copie."}</p>
    <div class="frow"><label for="sbConfirmIn">Tape ${w} pour confirmer</label><input id="sbConfirmIn" type="text" autocomplete="off" style="${INP}"></div>
    <div class="btns"><button class="btn alt" type="button" id="sbCancel">Annuler</button><button class="btn danger" type="button" id="${del ? "sbDeleteGo" : "sbWipeGo"}">${del ? "Supprimer mon compte" : "Effacer"}</button></div>`;
  $("#sbConfirmIn").focus();
}
const sbConfirmed = w => (($("#sbConfirmIn") || {}).value || "").trim().toUpperCase() === w;
async function sbWipe() {
  if (!sbConfirmed("EFFACER")) { sbMsg("Tape EFFACER pour confirmer."); return; }
  for (const id in store.timers) clearTimeout(store.timers[id]);
  const { error } = await store.sb.from("progress").delete().like("key", "zh:%");
  if (error) { sbMsg("Effacement impossible : " + error.message); return; }
  store.cache = {}; $("#sbConfirm").innerHTML = ""; sbMsg("Progression effacée du compte.");
}
async function sbDelete() {
  if (!sbConfirmed("SUPPRIMER")) { sbMsg("Tape SUPPRIMER pour confirmer."); return; }
  for (const id in store.timers) clearTimeout(store.timers[id]);
  sbMsg("Suppression…");
  const { error } = await store.sb.rpc("delete_my_account");
  if (error) { sbMsg("Suppression impossible : " + error.message + " (la fonction delete_my_account doit être installée dans Supabase, voir supabase/schema.sql)."); return; }
  try { await store.sb.auth.signOut(); } catch (e) {}
  store.kind = null; store.uid = null; store.email = ""; store.cache = {}; ls.set("owner", null);
  $("#accountBtn").textContent = "Compte"; renderAccount(); toast("Compte supprimé");
}
function sbCfgSave(clear) {
  if (clear) ls.set("sbcfg", {}); else {
    const u = ($("#sbUrl").value || "").trim().replace(/\/+$/, ""), k = ($("#sbKey").value || "").trim();
    if (!/^https:\/\/\S+$/.test(u) || k.length < 20) { sbMsg("Renseigne l'URL (https://…) et la clé anon."); toast("URL ou clé invalide"); return; }
    ls.set("sbcfg", { supabaseUrl: u, supabaseKey: k });
  }
  toast("Paramètres enregistrés"); setTimeout(() => location.reload(), 500);
}
function wireAccount() {
  const b = $("#acctSet"); if (!b) return;
  b.addEventListener("click", e => {
    const id = e.target.id;
    if (id === "sbSignup") sbSend(true); if (id === "sbSend") sbSend(false); if (id === "sbVerify") sbVerify(); if (id === "sbBack") renderAccount();
    if (id === "sbOut") sbOut(); if (id === "sbChange") sbChange(); if (id === "sbExport") sbExport();
    if (id === "sbWipe") sbAsk("wipe"); if (id === "sbDelete") sbAsk("delete"); if (id === "sbCancel") $("#sbConfirm").innerHTML = "";
    if (id === "sbWipeGo") sbWipe(); if (id === "sbDeleteGo") sbDelete();
    if (id === "sbCfgSave") sbCfgSave(false); if (id === "sbCfgClear") sbCfgSave(true);
  });
  b.addEventListener("keydown", e => { if (e.key !== "Enter") return; if (e.target.id === "sbEmail") sbSend(false); if (e.target.id === "sbCode") sbVerify(); if (e.target.id === "sbNewEmail") sbChange(); });
  renderAccount();
}
