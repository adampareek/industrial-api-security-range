from fastapi import FastAPI
app = FastAPI(title="Internal Console")
@app.get("/")
def root():
    return {"service": "internal-console", "visibility": "docker-network-only"}
@app.get("/secret-status")
def secret_status():
    return {"service": "internal-console", "classification": "training-only", "diagnostic": "PLC synchronization healthy", "proof": "ssrf-reached-internal-console"}
