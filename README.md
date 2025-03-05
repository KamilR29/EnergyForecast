# energyForecast

## Opis aplikacji
Aplikacja Energy Forecast to narzędzie do prognozowania cen energii elektrycznej w wybranych krajach europejskich. Wykorzystuje model predykcyjny oparty na AutoGluon oraz model językowy (LLM) do analizy wyników i generowania rekomendacji. Aplikacja obsługuje interaktywny interfejs użytkownika dzięki frameworkowi Streamlit.

## Funkcjonalności aplikacji:
### Prognozowanie cen energii:
- Użytkownik wprowadza rok, miesiąc i wybiera kraj.
- Aplikacja generuje prognozę cen energii do podanego okresu czasu.
### Wizualizacja wyników:
- Interaktywny wykres przedstawiający zmienność cen energii w czasie.
### Generowanie rekomendacji:
- Model językowy generuje sugestie dotyczące instalacji alternatywnych źródeł energii na podstawie prognozowanych cen.
### Obsługa wielu krajów:
- Prognozy można wygenerować dla 24 krajów europejskich.

## Uruchomienie:
### Wymagane oprogramowanie:
- Python: 3.8+
- Biblioteki: streamlit, pandas, dotenv, autogluon.tabular, langchain_openai
- Docker: Do uruchamiania aplikacji w kontenerze.
### Lokalnie:
ustawienie klucza API
```
export OPENAI_API_KEY=[YOUR_API_KEY]
```
uruchomienie aplikacji
```
streamlit run app.py

```
### Docker:
ustawienie klucza API
```
export OPENAI_API_KEY=[YOUR_API_KEY]
```
uruchomienie aplikacji 
```
docker run -p 8501:8501 -e OPENAI_API_KEY=$OPENAI_API_KEY streamlit-app
```
