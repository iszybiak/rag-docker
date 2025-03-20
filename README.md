# RAG (Retrieval-Augmented Generation) na Dockerze  

## **Opis projektu**
Ten projekt implementuje **system RAG (Retrieval-Augmented Generation)**, który łączy:  
**Bazę wektorową (ChromaDB)** do przechowywania dokumentów  
**Model LLM (GPT-4)** do generowania odpowiedzi na podstawie znalezionych informacji  
**Ręczne dodawanie tekstu i obsługę plików PDF** jako źródła wiedzy  

---

## **Technologie**  
* Python (FastAPI, SQLAlchemy)  
* PostgreSQL (baza dokumentów)  
* ChromaDB (baza wektorowa)  
* OpenAI GPT-4 (model LLM)  
* Docker (konteneryzacja)  

---

##  **Instalacja i uruchomienie**  

### **Klonowanie repozytorium**  
```
git clone https://github.com/twoj-projekt/rag-docker.git
cd rag-docker
```

## **Ustawienie zmiennych środowiskowych ** 
Stwórz plik .env i wypełnij go:
```
OPENAI_API_KEY="sk-***A"
DATABASE_URL=postgresql://user:password@db:5432/rag_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=rag_db
```
## **Uruchomienie projektu w Dockerze ** 
```
docker-compose up --build
```

## **Struktura projektu**
```
rag-docker/
│── app/
|   ├── database.py      # Połączenie z PostgreSQL
│   ├── embeddings.py    # Przetwarzanie tekstu i generowanie embeddingów
│   ├── main.py          # Główne API FastAPI
│   ├── models.py        # Modele ORM (SQLAlchemy)
|   │── requirements.txt # Lista zależności
│── .env                 # .env
│── docker-compose.yml   # Konfiguracja Docker
│── Dockerfile           # Definicja kontenera API
│── README.md            # Ten plik
```

## **Testowanie za pomocą Postmana** 
```
POST np. http://localhost:8000/add_document/?text=To jest nowa informacja, którą chcę dodać do bazy.
GET np. http://localhost:8000/ask/?question=Co to jest AI?
```







