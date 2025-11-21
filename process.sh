#!/bin/bash

# --- Ustawienia ---

# Ścieżka do folderu zawierającego pliki GPX.
# Zmień tę wartość na ścieżkę do Twojego folderu.
GPX_FOLDER="./trasy_gpx"

# Nazwa Twojego skryptu Python. Upewnij się, że ta ścieżka jest poprawna.
PYTHON_SCRIPT="./plot_gpx.py"

# Folder, w którym mają być zapisane wygenerowane pliki PNG.
# Zostanie utworzony, jeśli nie istnieje.
OUTPUT_FOLDER="./profile_png"

# --- Funkcja Główna ---

echo "--- Rozpoczęcie generowania profili wysokości ---"

# 1. Sprawdzenie i utworzenie folderu wyjściowego
if [ ! -d "$OUTPUT_FOLDER" ]; then
    mkdir -p "$OUTPUT_FOLDER"
    echo "Utworzono folder wyjściowy: $OUTPUT_FOLDER"
fi

# 2. Iteracja po wszystkich plikach GPX w wskazanym folderze
# Używamy find i pętli, co jest bezpieczniejsze dla nazw plików zawierających spacje.
find "$GPX_FOLDER" -maxdepth 1 -type f -name "*.gpx" | while IFS= read -r GPX_FILE
do
    echo "Przetwarzanie pliku: $GPX_FILE"

    # Pobranie samej nazwy pliku (bez ścieżki)
    FILENAME=$(basename "$GPX_FILE")
    
    # Usunięcie rozszerzenia ".gpx" i dodanie nowego rozszerzenia ".png"
    # To jest kluczowy krok do tworzenia identycznej nazwy
    BASE_NAME="${FILENAME%.gpx}"
    PNG_FILE="${BASE_NAME}.png"

    # Pełna ścieżka do pliku wyjściowego PNG
    OUTPUT_PATH="$OUTPUT_FOLDER/$PNG_FILE"

    # 3. Uruchomienie skryptu Python
    # Przekazujemy GPX_FILE jako pierwszy argument i OUTPUT_PATH jako drugi
    python3 "$PYTHON_SCRIPT" "$GPX_FILE" "$OUTPUT_PATH"
    
    if [ $? -eq 0 ]; then
        echo "--> Sukces! Zapisano jako: $OUTPUT_PATH"
    else
        echo "--> BŁĄD! Nie udało się wygenerować wykresu dla $GPX_FILE."
    fi

    echo "---"

done

echo "--- Zakończono przetwarzanie wszystkich plików GPX ---"
