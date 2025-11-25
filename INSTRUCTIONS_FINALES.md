# 📧 RegO - Instructions finales de configuration

## ⚠️ IMPORTANT: Configuration Azure AD requise

Pour que RegO fonctionne, vous devez **obligatoirement** effectuer les modifications suivantes dans Azure AD Portal:

### 🔧 Étapes à suivre MAINTENANT:

1. **Allez sur https://portal.azure.com**
2. **Naviguez vers votre application "RegO"** (ID: 0bf5e2d3-8bd8-4018-bb93-574036e9da92)

### ✅ Vérifier les Permissions (CRITIQUE)

1. Cliquez sur **"API permissions"** dans le menu de gauche
2. Vous devez avoir ces permissions **Application** (pas Delegated):
   - ✅ **Mail.Read** (Application)
   - ✅ **User.Read.All** (Application)

3. **SI CE N'EST PAS LE CAS:**
   - Supprimez toutes les permissions existantes
   - Cliquez sur "+ Add a permission"
   - Sélectionnez "Microsoft Graph"
   - Choisissez "Application permissions" (PAS Delegated)
   - Ajoutez `Mail.Read`
   - Ajoutez `User.Read.All`
   - Cliquez sur "Add permissions"

4. **CRUCIAL:** Cliquez sur **"Grant admin consent for [Votre organisation]"**
   - Confirmez en cliquant "Yes"
   - Attendez que les coches vertes apparaissent

### 📧 Configurer votre email

Dans le fichier `.env`, remplacez:
```
USER_EMAIL=votre.email@votreentreprise.com
```

Par votre **vrai email professionnel**, exemple:
```
USER_EMAIL=morel.stevensndong@votreentreprise.com
```

## 🧪 Tester l'installation

Une fois les étapes ci-dessus complétées:

```bash
# Test automatique complet
python test_server.py
```

Si tout fonctionne, vous verrez:
```
✅ TOUS LES TESTS ONT RÉUSSI!
```

## 🚀 Utilisation normale

```bash
python main.py
```

Menu interactif:
1. S'authentifier
2. Récupérer vos emails
3. Voir les statistiques
4. Voir la liste
5. Exporter en PDF

## 📊 Structure des fichiers

```
RegO/
├── .env                    ← Vos identifiants (À CONFIGURER)
├── main.py                 ← Lancer l'application
├── test_server.py         ← Script de test
├── data/
│   └── email_registry.json  ← Registre des emails
└── exports/
    └── *.pdf               ← PDF générés
```

## 🔒 Checklist de sécurité

- [x] CLIENT_ID configuré
- [x] CLIENT_SECRET configuré
- [x] TENANT_ID configuré
- [ ] **USER_EMAIL à configurer** (VOTRE email)
- [ ] **Permissions Azure AD vérifiées**
- [ ] **Admin consent accordé**

## ❓ Problèmes courants

### Erreur "400 Bad Request"
→ Les permissions ne sont pas configurées en mode "Application"
→ Allez dans Azure AD et changez les permissions

### Erreur "Insufficient privileges"
→ Vous n'avez pas cliqué sur "Grant admin consent"
→ Retournez dans Azure AD > API permissions > Grant admin consent

### "No emails found"
→ Vérifiez que USER_EMAIL est correct dans .env
→ Vérifiez que votre boîte mail contient des emails

## 📞 Support

Consultez les fichiers:
- `README.md` - Documentation complète
- `CONFIGURATION.md` - Guide Azure AD détaillé
- `DEPLOIEMENT_SERVEUR.md` - Pour déployer sur serveur

## ✨ Résumé rapide

1. ✅ **Permissions Azure:** Mail.Read + User.Read.All (Application)
2. ✅ **Admin consent:** Accordé
3. ✅ **USER_EMAIL dans .env:** Votre email professionnel
4. ✅ **Test:** `python test_server.py`
5. ✅ **Lancer:** `python main.py`

---

**Une fois ces étapes complétées, RegO sera 100% fonctionnel! 🎉**
