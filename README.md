# Python Package Update Notifier for Telex

## Project Structure

.
├── app/
│ ├── init.py
│ └── main.py
├── tests/
│ └── test_main.py
├── requirements.txt
├── runtime.txt
└── render.yaml

## Setup

1. Clone repository:

   ```bash
   git clone https://github.com/yourusername/telex-python-updater.git
   cd telex-python-updater
   ```

## Install dependencies:

```bash

pip install -r requirements.txt
```

## Set environment variables:

```bash

echo "TELEX_API_KEY=your_secret_key" > .env
```

## Running Locally

```bash

uvicorn app.main:app --reload
```

## Deployment on Render

- Push code to GitHub

- Create new Web Service in Render dashboard

- Use provided render.yaml config

- Set environment variable API_KEY

## Testing

```bash

curl -X POST http://localhost:8000/check-updates \
     -H "x-api-key: your_secret_key"

```
