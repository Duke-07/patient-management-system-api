# 🏥 Patient Management System API — *The FastAPI That Judges Your BMI*

> ⚠️ **WARNING:** This API knows your BMI before your doctor does. It calculates. It judges. It never lies. Enter at your own risk.

```
   _____ _____   _    _____ _____
  / ____|  __ \ | |  |_   _|  __ \
 | |    | |__) || |    | | | |  | |
 | |    |  _  / | |    | | | |  | |
 | |____| | \ \ | |____| |_| |__| |
  \_____|_|  \_\|______|_____|_____/

        [ patients loaded... beep boop ]
```

## 🤔 What IS this thing?

It's a **fully functional CRUD API** for managing patient records, built with FastAPI, and secretly obsessed with your **Body Mass Index**. You give it a height and a weight, and it will compute your `bmi` and hand you a `verdict` — `Underweight`, `Normal`, `Overweight`, or `Obese` — faster than you can say "I was going to start my diet Monday."

Data lives in a humble `patient.json` file, because we said "database" and then got scared and went with a JSON file instead. No regrets. 🗃️

## ⚡ Features That Will Change Your Life (Maybe)

- 🩺 **Full CRUD** — Create, Read, Update, Replace, Delete patients like a boss
- 🧮 **Auto-computed BMI + Verdict** — math so you don't have to
- 📊 **`/statistics`** — because someone in the office asked for "analytics"
- 🔍 **Filter, search, sort** — by city, gender, name, height, weight, BMI (asc/desc, we're fancy)
- 🌐 **CORS wide open** (`allow_origins=["*"]`) — anyone, anywhere, anytime. YOLO security model.
- 📁 **JSON file "database"** — enterprise-grade in spirit, `.json` in practice
- 💥 **Proper HTTP status codes** — 201s, 404s, 400s, flying everywhere like confetti

## 🗂️ Project Structure

```
├── app.py              # The chosen one. All the logic lives here.
├── patient.json         # Our "database" (don't tell the DBAs)
├── requirements.txt      # Summon these before the ritual
├── LICENSE
└── screenshots/          # Proof this thing actually works
    ├── hello.png
    ├── about.png
    ├── health.png
    ├── statistics.png
    ├── get-all-patients.png
    ├── get-patient.png
    ├── sort-patient.png
    ├── create-patient.png
    ├── replace-patient.png
    ├── update-patient.png
    ├── delete-patient.png
    └── swagger-home.png
```

## 🚀 Getting Started (Summoning Instructions)

```bash
# 1. Clone this magnificent piece of engineering
git clone <this-repo>
cd <this-repo>

# 2. Install the sacred dependencies
pip install -r requirements.txt

# 3. Awaken the API
uvicorn app:app --reload

# 4. Go stare at the docs like a proud parent
# http://127.0.0.1:8000/docs
```

## 🧪 Endpoints (a.k.a. "The Menu")

| Method | Endpoint | What it does |
|--------|----------|---------------|
| `GET` | `/` | Says hi. Very polite. |
| `GET` | `/about` | Explains itself, like a nervous intern |
| `GET` | `/health` | "Am I alive?" — yes, apparently |
| `GET` | `/statistics` | Number crunching, gender breakdowns, BMI verdicts galore |
| `GET` | `/patient` | Get ALL patients — with filters for city, gender, name, plus pagination |
| `GET` | `/patient/{id}` | Get one specific human |
| `GET` | `/sort` | Sort humans by height, weight, or BMI, asc or desc |
| `POST` | `/patient` | Create a new patient (and their permanent BMI verdict) |
| `PUT` | `/patient/{id}` | Full replace — out with the old, in with the new |
| `PATCH` | `/patient/{id}` | Partial update — surgical precision |
| `DELETE` | `/patient/{id}` | Poof. Gone. 204 No Content. No mourning period. |

## 📸 Receipts (Screenshots)

Yes, we have proof. Check the `screenshots/` folder for visual evidence that every single endpoint works, including the glorious Swagger UI home page where all this documentation-generating magic happens automatically because FastAPI is just built different.

## 🧠 The BMI Verdict Algorithm™

```
if bmi < 18.5:      "Underweight"    😰
elif bmi < 24.9:     "Normal"         😌
elif bmi < 29.9:     "Overweight"     😅
else:                "Obese"          😳
```

Computed live, every single time, via `@computed_field`. No caching. No mercy.

## ⚠️ Disclaimers (Read Before Panicking)

- This is **not** a real medical system. Please do not deploy this in an actual hospital.
- `allow_origins=["*"]` means literally any website on the internet can talk to this API. Great for a demo, terrifying for production.
- Storing patient data in a flat JSON file is *a choice*. A bold one.
- If two people hit `POST /patient` at the exact same millisecond, we make no promises.

## 🛠️ Tech Stack

- **FastAPI** — because Flask felt too 2015
- **Pydantic** — for yelling at you when your data is wrong
- **Uvicorn** — the engine under the hood
- **JSON** — the "database" that dares to dream

## 📜 License

See `LICENSE`. Use responsibly. Or irresponsibly. We're not your doctor.

## 🙌 Final Words

If this README made you laugh even once, the mission is complete. If it didn't, well — at least your BMI verdict is accurate. 🎯

---

*Built with FastAPI, mild chaos, and a JSON file pretending to be a database.*
