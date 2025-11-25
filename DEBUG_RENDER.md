# 🔧 Instructions pour voir les logs d'erreur Render

## Sur le Dashboard Render:

1. **Cliquez sur le service**: `rego-ocean-factory-wj6x`

2. **Menu gauche** → **Logs**

3. **Cherchez les lignes avec**:
   - ❌ `Error`
   - ❌ `Failed`
   - ❌ `ModuleNotFoundError`
   - ❌ `SyntaxError`

4. **Les dernières 10-20 lignes** contiennent l'erreur

---

## OU essayez un redéploiement manuel:

1. Sur la page du service
2. **Manual Deploy** (bouton en haut à droite)
3. **Deploy latest commit**

---

## Erreurs communes:

### Si vous voyez "ModuleNotFoundError: No module named 'authlib'":
→ Problème: authlib manquant dans requirements.txt

### Si vous voyez "Port already in use":
→ Problème: Configuration du port

### Si vous voyez "Application failed to start":
→ Problème: Erreur dans app_pro.py

---

**Montrez-moi le message d'erreur et je corrige!** 🚀
