#!/bin/bash
# Ausführen mit: ./Push.sh dev  oder  ./Push.sh main
set -e

REPO_PATH="$(cd "$(dirname "$0")" && pwd)"
BRANCH="${1:-main}"

cd "$REPO_PATH" || exit 1

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Fehler: $REPO_PATH ist kein Git-Repository"
    exit 1
fi

if ! git remote get-url origin > /dev/null 2>&1; then
    echo "Fehler: Kein 'origin' Remote konfiguriert"
    exit 1
fi

echo "Repo:   $(git remote get-url origin)"
echo "User:   $(git config user.name) <$(git config user.email)>"
echo "Branch: $BRANCH"

# FIX: 'set -e' temporär umgehen, falls der Branch-Wechsel eine Warnung wirft
git switch "$BRANCH" 2>/dev/null || git switch -c "$BRANCH" || true

git add .
if git diff --cached --quiet; then
    echo "Keine Änderungen zum Committen."
else
    git commit -m "$(date '+%Y-%m-%d %H:%M:%S') - Featuress 1-5 + Bonus functional ==> GUI mit Differenzierungslogik (CEO sieht als einziger die Diagramm) & Abgabedoku und Code Kommentieren fehlt noch"
fi 

if git ls-remote --exit-code --heads origin "$BRANCH" > /dev/null 2>&1; then
    git pull origin "$BRANCH" --rebase
else
    echo "Remote-Branch '$BRANCH' existiert noch nicht - ueberspringe pull."
fi

git push -u origin "$BRANCH"