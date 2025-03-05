
# Dokumentacja aplikacji Energy Forecast

## Przegląd
Aplikacja Energy Forecast to narzędzie predykcyjne zaprojektowane do prognozowania przyszłych cen energii elektrycznej w różnych krajach europejskich. Posiada interaktywny interfejs webowy zbudowany w Streamlit, integruje model predykcyjny do precyzyjnego prognozowania oraz wykorzystuje sztuczną inteligencję do generowania praktycznych zaleceń na podstawie prognozowanych danych.

Niniejsza dokumentacja dostarcza szczegółowych informacji o funkcjonalności, strukturze oraz instrukcji użytkowania aplikacji.

---

## Funkcjonalności

### Interfejs użytkownika
- Interaktywny interfejs webowy umożliwiający wprowadzanie danych przez użytkownika.
- Wykres liniowy przedstawiający prognozowane ceny energii elektrycznej.

### Możliwości prognozowania
- Prognozowanie cen energii elektrycznej dla wybranego kraju i przedziału czasowego.
- Obsługa prognoz dla 24 krajów europejskich.

### Integracja AI
- Wykorzystanie modelu językowego OpenAI do generowania wniosków i rekomendacji na podstawie prognozowanych danych.

### Przetwarzanie danych
- Generowanie ramki danych (DataFrame) z miesięcznymi prognozami.
- Wizualizacja trendów za pomocą funkcji wykresów Streamlit.

---

## Przepływ aplikacji

![aplikcja](EneryForecastApp.jpg)

### Dane wejściowe użytkownika
Użytkownik wprowadza:
- Rok (od 2025).
- Miesiąc (lista rozwijana).
- Kraj (lista rozwijana).

### Przetwarzanie danych
- Obliczanie zakresów dat od stycznia 2015 do wybranego roku i miesiąca.
- Pobieranie prognozowanych cen dla wybranego kraju i zakresu czasowego.

### Wizualizacja
- Generowanie wykresu liniowego przedstawiającego prognozowane ceny energii elektrycznej.

### Wnioski AI
- Analiza prognozowanych cen w celu identyfikacji najniższych i najwyższych wartości.
- Generowanie zaleceń dotyczących rozwiązań energetycznych przez AI.

---

## Dokumentacja skryptów

### 1. `app.py`

#### Przegląd
Skrypt `app.py` pełni rolę głównego punktu wejścia do aplikacji Energy Forecast. Wykorzystuje Streamlit do zapewnienia interaktywnego interfejsu użytkownika, integruje moduł `predictor.py` do generowania prognoz oraz wykorzystuje model językowy OpenAI do generowania wniosków na podstawie prognoz.

#### Kluczowe funkcje

- **`get_month_number(month)`**: Konwertuje nazwę miesiąca na odpowiadającą jej wartość liczbową.
- **`is_leap_year(year)`**: Sprawdza, czy dany rok jest rokiem przestępnym.
- **`generate_monthly_dates(start, end)`**: Generuje listę miesięcznych dat pomiędzy dwoma obiektami datetime.
- **`run_llm(predicted_prices, country)`**: Używa modelu językowego OpenAI do generowania odpowiedzi na podstawie prognozowanych cen.

#### Logika aplikacji
1. **Wprowadzanie danych przez użytkownika**:
   - Użytkownicy wprowadzają rok (od 2025 wzwyż), miesiąc i kraj z predefiniowanych list.
2. **Prognozowanie**:
   - Wywołuje funkcję `run` z modułu `predictor.py`, aby uzyskać prognozy dla wybranego kraju i zakresu dat.
3. **Wizualizacja**:
   - Generuje wykres liniowy prognozowanych cen energii elektrycznej za pomocą Streamlit.
4. **Wnioski AI**:
   - Wywołuje `run_llm`, aby wygenerować zalecenia dotyczące oszczędności energii na podstawie prognoz.

#### Logowanie
- Konfiguruje logowanie za pomocą skryptu `logger.py` w celu rejestrowania zdarzeń i błędów aplikacji.

---

### 2. `logger.py`

#### Przegląd
Skrypt `logger.py` odpowiada za konfigurację logowania dla aplikacji. Zapewnia rejestrowanie wszystkich kluczowych zdarzeń, błędów i informacji zarówno w konsoli, jak i w pliku logów (`app.log`).

#### Funkcja

- **`configure_logging()`**:
  - Konfiguruje logowanie z następującymi ustawieniami:
    - Logi są formatowane w celu uwzględnienia znaczników czasu, poziomów logowania i komunikatów.
    - Logi są zapisywane zarówno w konsoli, jak i w pliku (`app.log`).
  - Funkcja jest wywoływana na początku działania aplikacji w celu zapewnienia spójnego logowania.

#### Użycie
Skrypt jest importowany i uruchamiany w `app.py`, aby skonfigurować logowanie w całej aplikacji.

---

### 3. `predictor.py`

#### Przegląd
Skrypt `predictor.py` obsługuje funkcjonalność modelowania predykcyjnego aplikacji. Wykorzystuje AutoGluon do ładowania wytrenowanych modeli i generowania prognoz cen energii elektrycznej na podstawie danych historycznych.

#### Kluczowe funkcje

- **`get_latest_model_path(directory)`**:
  - Pobiera ścieżkę do ostatnio modyfikowanego folderu modelu w określonym katalogu.

- **`load_model(model_path)`**:
  - Ładuje model predykcyjny ze wskazanej ścieżki przy użyciu AutoGluon.

- **`make_prediction(input_data, date_to, predictor)`**:
  - Generuje prognozy dla przyszłych dat do określonej daty.
  - Łączy dane historyczne i prognozowane w jeden zestaw danych.

- **`generate_future_data(date_to)`**:
  - Koordynuje ładowanie modeli i generowanie prognoz dla przyszłych dat do wskazanego celu.

- **`get_prices_for_country_predicted(country_name, data)`**:
  - Filtruje zestaw danych w celu uzyskania prognozowanych cen dla określonego kraju.

- **`run(year, month, day, country)`**:
  - Wykonuje cały przepływ pracy prognozowania dla określonej daty i kraju.

#### Przepływ pracy
1. **Obsługa modelu**:
   - Lokalizuje najnowszy wytrenowany model w katalogu `AutoGluonModels`.
   - Ładuje model za pomocą AutoGluon.
2. **Ładowanie danych**:
   - Odczytuje dane historyczne z pliku `data/electricity.csv`.
3. **Prognozowanie**:
   - Generuje prognozy dla przyszłych dat do określonej przez użytkownika daty.
4. **Prognozy dla konkretnego kraju**:
   - Filtruje prognozy w celu zwrócenia danych dla wybranego kraju.

#### Obsługa błędów
- Rejestruje błędy związane z brakującymi plikami danych lub niepowodzeniem ładowania modelu.

---

### 4. `train_model.py`

#### Przegląd
Skrypt `train_model.py` trenuje model machine learning do prognozowania cen energii elektrycznej na podstawie danych historycznych. Wykorzystuje AutoGluon do wydajnego trenowania i oceny modelu.

#### Kluczowe funkcje

- **`load_data(file_path)`**:
  - Ładuje dane cen energii elektrycznej z pliku CSV.
  - Obsługuje błędy, takie jak brakujące pliki, puste dane lub problemy z parsowaniem.

- **`clean_data(df)`**:
  - Czyści dane wejściowe poprzez:
    - Usuwanie wartości NaN i duplikatów.
    - Przycinanie wartości odstających na podstawie 1. i 99. percentyla.
    - Normalizację kolumn numerycznych za pomocą standaryzacji z-score.

- **`split_data(df)`**:
  - Dzieli zestaw danych na zbiory treningowy (80%) i testowy (20%).

- **`main()`**:
  - Koordynuje cały pipeline trenowania:
    1. Ładuje i czyści dane.
    2. Dzieli dane na zbiory treningowy i testowy.
    3. Trenuje model za pomocą `TabularPredictor` AutoGluon.
    4. Ocenia model przy użyciu RMSE jako metryki.

#### Przepływ pracy
1. **Ładowanie danych**:
   - Odczytuje dane historyczne z pliku `data/electricity.csv`.
   - Rejestruje wszelkie problemy napotkane podczas procesu ładowania.
2. **Czyszczenie danych**:
   - Usuwa nieistotne lub problematyczne dane w celu poprawy wydajności modelu.
3. **Podział danych**:
   - Dzieli dane na zbiory treningowy i testowy w celu oceny.
4. **Trenowanie modelu**:
   - Wykorzystuje `TabularPredictor` do trenowania modelu regresji na wyczyszczonych danych.
5. **Ewaluacja**:
   - Ocenia wydajność modelu na zbiorze testowym i rejestruje wyniki.

#### Obsługa błędów
- Rejestruje błędy związane z pustymi plikami, brakującymi danymi lub niepowodzeniem trenowania.

---

## Wymagane pliki i zmienne

### Pliki zewnętrzne
- **`predictor.py`**: Obsługuje model predykcyjny.
- **`train_model.py`**: Obsługuje trenowanie modelu.
- **`logger.py`**: Konfiguruje logowanie dla aplikacji.
- **`images/logo.png`**: Logo aplikacji.

### Zmienne środowiskowe
- Zarządzane za pomocą `.env` i `load_dotenv()`.

---

## Uruchamianie

### Lokalnie

Sklonuj repozytorium i zainstaluj zależności:
```bash
pip install -r requirements.txt
```

Ustaw klucz API:
```
export OPENAI_API_KEY=[YOUR_API_KEY]
```

Aby wytrenować nowy model, wykonaj skrypt treningowy:
```bash
python train_model.py
```

Uruchom aplikację za pomocą Streamlit:
```bash
streamlit run app.py
```

Po uruchomieniu aplikacji uzyskaj dostęp w przeglądarce pod adresem:
```plaintext
http://localhost:8501
```

---

### Dockeryzacja

#### Budowanie i uruchamianie kontenera
1. Ustaw klucz API
```
export OPENAI_API_KEY=[YOUR_API_KEY]
```
2. Uruchom aplikację 
```
docker run -p 8501:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY slowickipiotr/energy-forecast:latest
```
3. Uzyskaj dostęp do aplikacji pod adresem:
```
http://localhost:8501
```


