#!/bin/bash
# Script de renommage des assets playstyles

echo "========================================="
echo "RENOMMAGE DES ASSETS PLAYSTYLES"
echo "========================================="
echo ""

# Dossier playstyles
echo "1. PLAYSTYLES (base)"
echo "---"
cd public/assets/playstyles

echo "   Renaming classe-de-loin.png → allonge.png"
mv 'classe-de-loin.png' 'allonge.png'

echo "   Renaming coup-de-pied-arrete.png → coups-de-pied-arretes.png"
mv 'coup-de-pied-arrete.png' 'coups-de-pied-arretes.png'

echo "   Renaming deflector.png → deviation.png"
mv 'deflector.png' 'deviation.png'

echo "   Renaming passe-en-profondeur.png → passe-tendue.png"
mv 'passe-en-profondeur.png' 'passe-tendue.png'

echo "   Renaming renversement.png → revolutionnaire.png"
mv 'renversement.png' 'revolutionnaire.png'

echo "   Renaming sortie-sur-les-centres.png → sorties-aeriennes.png"
mv 'sortie-sur-les-centres.png' 'sorties-aeriennes.png'

cd ..

# Dossier playstyles_plus
echo ""
echo "2. PLAYSTYLES+ (variants)"
echo "---"
cd playstyles_plus

echo "   Renaming classe-de-loin.png → allonge.png"
mv 'classe-de-loin.png' 'allonge.png'

echo "   Renaming coup-de-pied-arrete.png → coups-de-pied-arretes.png"
mv 'coup-de-pied-arrete.png' 'coups-de-pied-arretes.png'

echo "   Renaming deflector.png → deviation.png"
mv 'deflector.png' 'deviation.png'

echo "   Renaming passe-en-profondeur.png → passe-tendue.png"
mv 'passe-en-profondeur.png' 'passe-tendue.png'

echo "   Renaming sortie-sur-les-centres.png → sorties-aeriennes.png"
mv 'sortie-sur-les-centres.png' 'sorties-aeriennes.png'

cd ../../../

echo ""
echo "========================================="
echo "RENOMMAGES TERMINÉS ✓"
echo "========================================="
