import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import sys
import os 

def generate_elevation_plot(gpx_file_path, output_png_path):
    """
    Parsuje plik GPX podany w ścieżce i generuje wykres wysokości 
    względem dystansu, zapisując go do pliku PNG o proporcjach 17:6.

    :param gpx_file_path: Ścieżka do pliku GPX.
    :param output_png_path: Ścieżka do pliku PNG, do którego zostanie zapisany wykres.
    """
    
    # 1. Sprawdzenie, czy plik GPX istnieje
    if not os.path.exists(gpx_file_path):
        print(f"Błąd: Nie znaleziono pliku GPX pod ścieżką: '{gpx_file_path}'")
        return

    try:
        # 2. Wczytanie i parsowanie pliku GPX
        with open(gpx_file_path, 'r', encoding='utf-8') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
    except Exception as e:
        print(f"Błąd podczas parsowania pliku GPX: {e}")
        return

    # Inicjalizacja list na dane
    distances = []  # Dystans od startu (w km)
    elevations = [] # Wysokość (w m)
    
    # Iteracja przez segmenty i punkty
    current_distance = 0.0
    previous_point = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                
                if previous_point:
                    distance_change = point.distance_3d(previous_point) 
                    
                    if distance_change is None:
                         distance_change = point.distance_2d(previous_point)
                         
                    current_distance += distance_change / 1000.0
                
                distances.append(current_distance)
                
                if point.elevation is not None:
                    elevations.append(point.elevation)
                else:
                    elevations.append(elevations[-1] if elevations else 0)
                    
                previous_point = point
                
    # 3. Wygenerowanie wykresu
    
    if not distances or not elevations:
        print("Błąd: Plik GPX nie zawiera wystarczających danych o punktach trasy lub wysokości.")
        return

    # Tworzenie wykresu z określonymi proporcjami (np. 17x6 cali)
    # Możesz dostosować wartości (17, 6) aby uzyskać większy/mniejszy obraz, 
    # zachowując proporcje.
    plt.figure(figsize=(17, 6)) 
    plt.plot(distances, elevations, color='blue', linewidth=2)
    
    plt.title('Profil Wysokości Trasy')
    plt.xlabel('Dystans [km]')
    plt.ylabel('Wysokość [m]')
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.fill_between(distances, elevations, min(elevations) - 10, color='skyblue', alpha=0.3)
    
    # Upewniamy się, że cały wykres (wraz z etykietami) mieści się w figurze
    plt.tight_layout()

    # Zapisanie wykresu do pliku PNG zamiast wyświetlania
    try:
        plt.savefig(output_png_path, dpi=300) # dpi=300 dla dobrej jakości obrazu
        print(f"Wykres został zapisany do: '{output_png_path}'")
    except Exception as e:
        print(f"Błąd podczas zapisywania wykresu do pliku: {e}")
    finally:
        plt.close() # Ważne: zamyka figurę Matplotlib, aby zwolnić pamięć

# --- Główny blok uruchamiający skrypt ---
if __name__ == "__main__":
    
    # Oczekujemy teraz dwóch argumentów: pliku GPX i nazwy pliku wyjściowego PNG
    if len(sys.argv) < 3:
        print("Użycie: python nazwa_skryptu.py <ścieżka_do_pliku.gpx> <ścieżka_do_pliku_wyjsciowego.png>")
        print("\nPrzykład: python gpx_profiler.py moja_trasa.gpx profil_wysokosci.png")
        sys.exit(1)
    
    gpx_file_input = sys.argv[1] 
    output_file_name = sys.argv[2] # Pobieramy nazwę pliku wyjściowego
    
    generate_elevation_plot(gpx_file_input, output_file_name)
