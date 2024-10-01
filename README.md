# CIS Benchmark Parser

This Flask application parses CIS Benchmark PDF files and converts them to CSV format.

## Run With Docker
1. Start docker service:
```
docker compose up -d --build
```

2. Open a web browser and go to `http://localhost:5000`
3. Choose File To Web HTML
4. Click Upload and Parse

## Installation & Run without docker

1. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate 
   ```

2. Start the Flask application:
   ```
   python run.py
   ```
3. Open a web browser and go to `http://localhost:5000`

