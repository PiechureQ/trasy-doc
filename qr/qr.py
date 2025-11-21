import qrcode
from qrcode.image.pil import PilImage
import os
import sys

def generate_qrs_from_file(input_file_path, output_folder):
    """
    Wczytuje linie w formacie 'nazwa,link' z pliku, generuje kody QR 
    i zapisuje je w podanym folderze.

    :param input_file_path: Ścieżka do pliku tekstowego z danymi 'nazwa,link'.
    :param output_folder: Ścieżka do folderu, gdzie zostaną zapisane PNG.
    """
    
    # 1. Sprawdzenie, czy plik wejściowy istnieje
    if not os.path.exists(input_file_path):
        print(f"Błąd: Nie znaleziono pliku wejściowego: '{input_file_path}'")
        return

    # 2. Utworzenie folderu wyjściowego
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Utworzono folder wyjściowy: '{output_folder}'")

    try:
        # 3. Wczytanie danych i ich parsowanie
        data_to_process = []
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue # Pomija puste linie
                
                # Oczekujemy formatu: nazwa_pliku,link
                if ',' not in line:
                    print(f"Ostrzeżenie (linia {line_number}): Pomijam. Brak przecinka (',') w linii. Oczekiwany format: nazwa,link.")
                    continue

                try:
                    # Dzielenie linii na dwie części po pierwszym przecinku
                    file_name_raw, link = line.split(',', 1)
                    
                    # Czyszczenie i normalizacja nazwy pliku
                    file_name = file_name_raw.strip().lower().replace(' ', '_')
                    if not file_name:
                         # Użycie domyślnej nazwy, jeśli część przed przecinkiem jest pusta
                        file_name = f"qr_link_{len(data_to_process) + 1}" 
                        
                    data_to_process.append((file_name, link.strip()))
                except ValueError:
                    print(f"Ostrzeżenie (linia {line_number}): Niepoprawny format. Pomijam.")
                    
    except Exception as e:
        print(f"Błąd podczas wczytywania pliku: {e}")
        return

    if not data_to_process:
        print("Plik wejściowy nie zawiera żadnych poprawnych danych do przetworzenia.")
        return

    print(f"Znaleziono {len(data_to_process)} pozycji do przetworzenia.")

    # 4. Generowanie i zapisywanie kodów QR
    for file_name, link in data_to_process:
        try:
            # Konfiguracja i dodanie danych
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H, 
                box_size=10, 
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            # Tworzenie obrazu
            img = qr.make_image(fill_color="black", back_color="white", image_factory=PilImage)
            
            # Pełna ścieżka do pliku wyjściowego PNG
            output_path = os.path.join(output_folder, f"{file_name}.png")
            
            # Zapisywanie pliku
            img.save(output_path)
            print(f"   -> Zapisano kod QR dla '{file_name}' jako '{os.path.basename(output_path)}'")

        except Exception as e:
            print(f"Błąd podczas generowania QR dla linku: '{link}' (Nazwa pliku: {file_name}). Błąd: {e}")
            continue

    print("--- Zakończono generowanie kodów QR ---")

# --- Główny blok uruchamiający skrypt ---
if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Użycie: python qr_generator_named.py <plik_z_danymi.txt> <folder_wyjściowy>")
        print("\nPrzykład: python qr_generator_named.py trasy.csv kody_qr")
        sys.exit(1)
    
    input_file = sys.argv[1] 
    output_dir = sys.argv[2] 
    
    generate_qrs_from_file(input_file, output_dir)
