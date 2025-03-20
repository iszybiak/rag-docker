from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import Session, init_db, Document
from embeddings import add_document, search_documents, extract_text_from_pdf
from model import generate_answer

# Creating a FastAPI application
app = FastAPI()

# Database initialization
init_db()

# Downloading database session
def get_db():
    db = Session()
    try:
        yield db
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()


@app.post("/add_document/")
def add_doc(text: str, db: Session = Depends(get_db)):
    """Adding a document to PostgreSQL and ChromaDB."""
    try:
        new_document = Document(text=text)
        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        try:
            add_document(text, new_document.id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ChromaDB error: {str(e)}")

        return {"message": "Document added", "id": new_document.id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/ask/")
def ask(question: str):
    """Finding relevant documents and generating answer"""
    try:
        documents = search_documents(question)
        if not documents:
            raise HTTPException(status_code=404, detail="Document not found")
        context = " ".join(documents)

        try:
            answers = generate_answer(context, question)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

        return {"question": question, "answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Adding text from PDF to PostgreSQL and generating embedding in ChromaDB."""
    try:
        file_path = file.file.read()
        text = extract_text_from_pdf(file_path)
        new_document = Document(text=text)
        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        try:
            add_document(text, new_document.id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ChromaDB error: {str(e)}")

        return {"message": "PDF added", "id": new_document.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")




