# Package Update Notifier - Telex Integration

This is a Telex Interval Integration that tracks dependency updates for `npm`, `pip`, and `cargo`, sending update notifications to a Telex channel.

## Features

- Checks package versions at set intervals.
- Supports `npm`, `pip`, and `cargo` package managers.
- Sends update notifications to Telex.

## Setup & Installation

### 1. Clone the Repository

```sh
git clone https://github.com/telex_integrations/package-update-notifier.git
cd package-update-notifier
```

2. Install Dependencies

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the Server Locally

```sh
uvicorn main:app --reload
```

4. Test the Integration

- Use curl to trigger an interval check:

```
curl --location 'http://localhost:8000/tick' \
--header 'Content-Type: application/json' \
--data '{
    "channel_id": "test-channel",
    "return_url": "https://mock.telex.im/v1/return/test-channel",
    "settings": [
        {
            "label": "tracked_packages",
            "type": "json",
            "required": true,
            "default": "{\"pip\": [\"requests\"], \"npm\": [\"react\"], \"cargo\": []}"
        }
    ]
}'
```

5. Deploy to Render

   Deploy using:

or

git push heroku main # If using Heroku

6. Activate the Integration in Telex

   Go to your Telex organization.
   Add your hosted /integration.json URL.
   Configure the interval and package managers.

7. Screenshots

✅ **Fixes Applied:**

- ✅ **Clear setup instructions**.
- ✅ **Telex activation steps**.
- ✅ **Includes deployment details**.

---

### **Final Checklist**

✅ `/tick` now correctly calls `return_url`.  
✅ `tracked_packages` default JSON is fixed.  
✅ Tests now include `return_url` behavior.  
✅ README updated with setup, testing, and deployment.
