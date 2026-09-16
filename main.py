from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import shutil
import os
from transformer import transform_to_ml_matrix

app = FastAPI(title="ML Matrix Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-dataset")
async def process_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")
    
    temp_path = f"temp_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        if os.path.getsize(temp_path) == 0:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        raw_df = pd.read_csv(temp_path)
        if raw_df.empty:
            raise HTTPException(status_code=400, detail="CSV contains no readable data.")

        # Transform raw data directly to numerical ML Matrix
        ml_df = transform_to_ml_matrix(raw_df)
        
        ml_csv_path = f"ml_matrix_{file.filename}"
        ml_df.to_csv(ml_csv_path, index=False)

        # Calculate quick quality score
        score_text = "N/A"
        if len(ml_df.columns) > 1 and len(ml_df) >= 5:
            X = ml_df.iloc[:, :-1]
            y = ml_df.iloc[:, -1]
            
            if y.nunique() > 1:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestClassifier(n_estimators=10, random_state=42)
                model.fit(X_train, y_train)
                acc = model.score(X_test, y_test)
                score_text = f"{round(acc * 100, 2)}%"

        return {
            "status": "success",
            "download_url": f"/download/{ml_csv_path}",
            "rows": len(ml_df),
            "features": len(ml_df.columns),
            "quality_score": score_text,
            "preview": ml_df.head(5).to_dict(orient="records")
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/download/{filename}")
async def download_file(filename: str):
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path=filename, filename=filename, media_type='text/csv')

app.mount("/", StaticFiles(directory="Frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)