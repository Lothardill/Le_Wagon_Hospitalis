# Hospitalis RFID — Optimisation des achats médicaux & faisabilité RFID

**Projet de fin de bootcamp (Le Wagon)**, retravaillé en structure professionnelle.  
Objectif : analyser les achats hospitaliers, identifier les produits critiques et tester la faisabilité d’un suivi par **RFID** pour améliorer la traçabilité et réduire les coûts.  
Les données réelles sont protégées par NDA → ce repo contient un pipeline reproductible + un générateur de **données synthétiques**.

---

## Contexte

Hospitalis facilite le lien entre **laboratoires** et **hôpitaux/clinques** pour les dispositifs médicaux.  
Le défi :  
- Des données massives (~50 Go) issues de multiples fournisseurs,  
- Format hétérogène (Excel, colonnes en français, erreurs de saisie),  
- Pas de prix unitaire normalisé,  
- Besoin d’évaluer si la **technologie RFID** pouvait optimiser la gestion des stocks (dépôt DMI, traçabilité, ROI).

---

## 🛠️ Solution proposée

Un **pipeline de données** modulaire en Python :  

1. **Ingestion**  
   - Agrégation de dizaines de fichiers (Excel/CSV → Parquet).  
   - Gestion des volumes via chunking.

2. **Nettoyage & harmonisation**  
   - Renommage FR → EN (`Libellé Article` → `product_label`).  
   - Typage automatique (quantités → int, dates → datetime).  
   - Gestion des valeurs manquantes / NULL.

3. **Calculs métier**  
   - Reconstitution du **prix unitaire** même en cas de données partielles (`Prix HT`, `Montant TTC / Quantité`, etc.).  
   - Création d’indicateurs (scores produits/fournisseurs).

4. **Scoring RFID**  
   - Pondération des produits selon : volume × prix × dépôt.  
   - Identification des candidats prioritaires pour une implémentation RFID.

5. **Export**  
   - Résultats stockés en `data/processed` pour reporting ou intégration BI.

---

## 📂 Structure du projet

```hospitalis-rfid/
├─ README.md
├─ src/hospitalis/   # code source
│  ├─ __init__.py
│  ├─ config.py
│  ├─ io.py
│  ├─ cleaning.py
│  ├─ pricing.py
│  ├─ rfid_selection.py
│  └─ pipeline.py
