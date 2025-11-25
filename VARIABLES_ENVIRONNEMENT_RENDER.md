# Variables d'environnement pour Render.com

## 📋 Copiez ces variables dans Render Dashboard

Allez dans: **Environment** → **Add Environment Variable**

```bash
# 1. Clé secrète Flask (GÉNÉRÉ - Utilisez celui-ci!)
FLASK_SECRET_KEY=77831fb56cc4f6dc5721c0a70bb6c84d7a825c511154820954612c7fa7e48613

# 2. Microsoft Client ID (Azure AD)
MICROSOFT_CLIENT_ID=0bf5e2d3-8bd8-4018-bb93-574036e9da92

# 3. Microsoft Client Secret (À RÉCUPÉRER dans Azure Portal)
MICROSOFT_CLIENT_SECRET=REMPLACEZ_PAR_VOTRE_SECRET_AZURE

# 4. Microsoft Tenant ID (Multi-tenant)
MICROSOFT_TENANT_ID=common
```

---

## 🔑 Comment obtenir MICROSOFT_CLIENT_SECRET?

1. Allez sur: https://portal.azure.com
2. **Azure Active Directory** → **App registrations**
3. Trouvez votre app: `0bf5e2d3-8bd8-4018-bb93-574036e9da92`
4. **Certificates & secrets** → **Client secrets**
5. Si vous n'en avez pas ou l'avez perdu:
   - **New client secret**
   - Description: `RegO Production`
   - Expires: `24 months`
   - **Add**
   - **COPIEZ LA VALEUR IMMÉDIATEMENT** (elle ne s'affiche qu'une fois!)
6. Remplacez `REMPLACEZ_PAR_VOTRE_SECRET_AZURE` ci-dessus

---

## ✅ Dans Render.com

Ajoutez chaque variable **une par une**:

### Variable 1:
- **Key**: `FLASK_SECRET_KEY`
- **Value**: `77831fb56cc4f6dc5721c0a70bb6c84d7a825c511154820954612c7fa7e48613`

### Variable 2:
- **Key**: `MICROSOFT_CLIENT_ID`
- **Value**: `0bf5e2d3-8bd8-4018-bb93-574036e9da92`

### Variable 3:
- **Key**: `MICROSOFT_CLIENT_SECRET`
- **Value**: `[Votre secret Azure récupéré]`

### Variable 4:
- **Key**: `MICROSOFT_TENANT_ID`
- **Value**: `common`

---

## 🎯 Ordre de Déploiement

1. ✅ Créer Web Service sur Render
2. ✅ Configurer Build & Start commands
3. ✅ **Ajouter ces 4 variables d'environnement**
4. ✅ Deploy!
5. ✅ Tester sur `https://[votre-app].onrender.com`
6. ✅ Ajouter domaine personnalisé
7. ✅ Configurer DNS GoDaddy
8. ✅ Configurer Azure AD redirect URI
9. ✅ Tester OAuth sur `https://ocean-factory.ca`

**Vous en êtes où?** 🚀
