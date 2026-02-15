# 🎓 EduSolve AI - Real-Time Student Doubt Solver

**Real-Time Student Doubt Solver using Machine Learning & Generative AI**

A full-stack web application that helps students resolve academic doubts instantly using ML-based question classification and Groq's Generative AI API.

---

## 📌 Project Overview

**EduSolve AI** is an intelligent study assistant designed by Subham. It demonstrates the practical integration of:

- **Machine Learning Models** for text classification
- **Natural Language Processing** for question preprocessing
- **Generative AI (Groq API)** for intelligent explanations
- **Full-Stack Web Development** with Flask + HTML/CSS/JS
- **Data Management** and model retraining workflows

### Key Features

✅ **Real-Time Question Processing** - Instant doubt resolution  
✅ **Smart Classification** - Automated subject and difficulty detection  
✅ **AI-Powered Explanations** - Step-by-step guidance from Groq API  
✅ **Data Storage** - JSON-based question and explanation archival  
✅ **Model Improvement** - Learn from stored data for better predictions  
✅ **Statistics Dashboard** - Track platform usage and metrics  
✅ **Download Feature** - Save explanations for offline access  

---

## 🎯 Real-World Problem Solved

- **Problem**: Students struggle with academic doubts and need instant accessible help
- **Solution**: EduSolve AI provides 24/7 intelligent explanation generation
- **Impact**: Improved learning outcomes, reduced study friction, data-driven insights

---

## 🧠 Key Concepts Demonstrated

### Machine Learning
- Text preprocessing and tokenization (NLTK)
- TF-IDF vectorization (Scikit-learn)
- Naive Bayes classification
- Model serialization (pickle)

### NLP
- Text cleaning and normalization
- Stop word removal
- Lemmatization
- Feature extraction

### Web Development
- Flask REST API design
- RESTful endpoint architecture
- CORS handling
- JSON data interchange

### Generative AI
- Third-party API integration
- Prompt engineering
- Response parsing
- Error handling

### Full-Stack Architecture
- Backend-frontend separation
- Asynchronous API calls
- State management
- Responsive UI design

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask 3.0 |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Machine Learning** | Scikit-learn 1.3 |
| **NLP Processing** | NLTK 3.8 |
| **Generative AI** | Groq API (Llama 3.1) |
| **Data Storage** | JSON files |
| **HTTP Client** | Requests library |
| **Environment** | Python 3.8+ |

---

## 📁 Project Structure

```
EduSolve-AI/
│
├── backend/                    # Flask backend
│   ├── app.py                 # Flask application factory
│   ├── routes.py              # API endpoints
│   ├── config.py              # Configuration & env variables
│   ├── groq_client.py         # Groq API integration
│   ├── preprocess.py          # NLP text preprocessing
│   └── ml_model.py            # ML model logic
│
├── frontend/                  # Web frontend
│   ├── templates/
│   │   └── index.html         # Main UI page
│   └── static/
│       ├── css/
│       │   └── style.css      # Modern styling
│       ├── js/
│       │   └── script.js      # Frontend logic
│       └── images/            # Assets
│
├── data/                      # Data storage
│   ├── training_data.json     # Stored Q&A records
│   └── labels.json            # Subject & difficulty labels
│
├── models/                    # Trained ML models
│   ├── subject_model.pkl      # Subject classifier
│   └── difficulty_model.pkl   # Difficulty classifier
│
├── .env                       # Environment variables (API keys)
├── requirements.txt           # Python dependencies
├── run.py                     # Application entry point
└── README.md                  # This file
```

---

## 🔄 Application Workflow

```
┌─────────────────────────────────────────────────────────┐
│  Student submits question via web interface            │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Flask Backend receives POST request                    │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  NLP Preprocessing:                                     │
│  • Text cleaning & lowercasing                         │
│  • Tokenization & stop word removal                    │
│  • Lemmatization                                       │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  ML Classification (Scikit-learn):                      │
│  • Predict subject (Math, Physics, etc.)               │
│  • Predict difficulty (Easy, Medium, Hard)             │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Groq API Request:                                      │
│  • Send question with classification context           │
│  • Construct optimized prompt                          │
│  • Receive AI-generated explanation                    │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Store Data (JSON):                                     │
│  • Question, classification, explanation saved         │
│  • Timestamp and metadata recorded                      │
└──────────────────┬──────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Return Response to Frontend                           │
│  • Display explanation with formatting                 │
│  • Show statistics dashboard                           │
│  • Enable download option                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (get free at https://console.groq.com)
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   cd EduSlove-AI
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify `.env` file has your Groq API key**
   ```
   GROQ_API_KEY=your_actual_api_key_here
   GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
   GROQ_MODEL=llama-3.1-8b-instant
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

---

## 📖 API Endpoints

### 1. Health Check
```
GET /api/health

Response:
{
    "status": "running",
    "message": "EduSolve AI Backend is operational",
    "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Ask Question (Main Endpoint)
```
POST /api/ask

Request Body:
{
    "question": "What is photosynthesis?"
}

Response:
{
    "status": "success",
    "question": "What is photosynthesis?",
    "subject": "Biology",
    "subject_confidence": 0.95,
    "difficulty": "Medium",
    "difficulty_confidence": 0.87,
    "explanation": "Step-by-step explanation from Groq AI...",
    "data_id": "2024-01-15T10:30:00.123456",
    "tokens_used": 256
}
```

### 3. Get History
```
GET /api/history

Response:
{
    "status": "success",
    "total_records": 42,
    "data": [
        {
            "id": "2024-01-15T10:30:00.123456",
            "question": "What is photosynthesis?",
            "subject": "Biology",
            "explanation": "..."
        },
        ...
    ]
}
```

### 4. Get Statistics
```
GET /api/stats

Response:
{
    "status": "success",
    "total_questions": 42,
    "subjects": {
        "Biology": 15,
        "Physics": 12,
        "Mathematics": 10,
        "Chemistry": 5
    },
    "difficulties": {
        "Easy": 18,
        "Medium": 16,
        "Hard": 8
    }
}
```

### 5. Clear Data (Development)
```
POST /api/clear-data

Response:
{
    "status": "success",
    "message": "All training data cleared"
}
```

---

## 🎓 Understanding the Code

### Backend Architecture

#### `config.py`
Centralizes all configuration including API keys, file paths, and model parameters. Loads from `.env` file for security.

#### `preprocess.py`
Implements the text preprocessing pipeline:
1. Remove URLs, special characters
2. Lowercase all text
3. Tokenization using NLTK
4. Stop word removal
5. Lemmatization (WordNet)

**Why?** Cleaned text improves ML model accuracy and consistency.

#### `ml_model.py`
Two Scikit-learn classifiers:
- **SubjectClassifier**: Predicts question subject (7 categories)
- **DifficultyClassifier**: Predicts difficulty level (3 levels)

Uses TF-IDF vectorization + Naive Bayes for fast, efficient classification.

#### `groq_client.py`
Communicates with Groq API:
- Constructs context-aware prompts
- Handles HTTP requests with error management
- Parses JSON responses
- Manages token usage

#### `routes.py`
Defines Flask REST API endpoints:
- Question processing pipeline
- Data persistence in JSON
- Statistics calculation
- Error handling with meaningful messages

#### `app.py`
Flask application factory:
- Initializes Flask app
- Configures CORS for cross-origin requests
- Registers blueprints
- Sets up static file serving

### Frontend Architecture

#### `index.html`
Semantic HTML structure with:
- Input section for questions
- Loading animation with progress steps
- Response cards for results
- Statistics dashboard
- Download functionality

#### `style.css`
Modern CSS with:
- CSS Grid for responsive layouts
- CSS Variables for theming
- Smooth animations and transitions
- Mobile-first responsive design
- Gradient backgrounds and cards

#### `script.js`
JavaScript logic:
- Fetch API for async requests
- Event handling and validation
- DOM manipulation and rendering
- Statistics loading
- File download generation

---

## 🔧 Configuration & Customization

### Adding New Subjects
Edit `backend/ml_model.py`:
```python
self.subjects = [
    'Mathematics', 'Physics', 'Chemistry', 'Biology',
    'English', 'History', 'Geography',
    'Computer Science'  # Add here
]
```

### Changing AI Model
Edit `.env`:
```
GROQ_MODEL=mixtral-8x7b-32768  # Change model
GROQ_MAX_TOKENS=1024           # Increase response length
GROQ_TEMPERATURE=0.5           # Control creativity (0-1)
```

### Adjusting ML Parameters
Edit `backend/config.py`:
```python
MIN_CONFIDENCE = 0.6        # Higher = stricter
RETRAINING_THRESHOLD = 5    # Retrain after N samples
```

---

## 📊 Data Flow & Persistence

### JSON Data Format
```json
{
    "id": "2024-01-15T10:30:00.123456",
    "timestamp": "2024-01-15T10:30:00.123456",
    "question": "What is photosynthesis?",
    "processed_text": "photosynthesis",
    "tokens": ["photosynthesis"],
    "subject": "Biology",
    "subject_confidence": 0.95,
    "difficulty": "Medium",
    "difficulty_confidence": 0.87,
    "explanation": "Photosynthesis is...",
    "model_used": "llama-3.1-8b-instant",
    "tokens_used": 256
}
```

### Model Retraining Workflow
1. Data accumulates in `data/training_data.json`
2. When threshold reached (10 samples), retrain triggers
3. ML models update in `models/` directory
4. Predictions improve with each iteration

---

## 🧪 Testing the Application

### Test Questions by Subject

**Mathematics:**
```
How do I solve a quadratic equation using the quadratic formula?
```

**Physics:**
```
What is the relationship between velocity and acceleration?
```

**Chemistry:**
```
Explain the structure of an atom.
```

**Biology:**
```
How does photosynthesis work in plants?
```

---

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution:** Verify `.env` file contains valid Groq API key
```bash
echo %GROQ_API_KEY%  # Windows
echo $GROQ_API_KEY   # Linux/Mac
```

### Issue: Backend not responding (Frontend error)
**Solution:** Start backend server
```bash
python run.py
```

### Issue: NLTK data not found
**Solution:** Download NLTK data manually
```bash
python -m nltk.downloader punkt stopwords wordnet
```

### Issue: Models not loading
**Solution:** Delete `.pkl` files in `models/` to retrain
```bash
rm models/*.pkl
```

---

## 📈 Performance Considerations

### Optimization Tips
- Questions < 5 sentences: Faster processing
- Pre-trained models: ~100ms classification
- Groq API: 1-3 second response typical
- JSON storage: Scales to 10K+ records without issues

### Scaling Suggestions
- **Database:** Replace JSON with SQLite/PostgreSQL
- **Caching:** Add Redis for frequent questions
- **Async Processing:** Use Celery for background tasks
- **Load Balancing:** Deploy multiple Flask instances

---

## 📚 Learning Resources

### For Understanding ML Models
- Scikit-learn Documentation: https://scikit-learn.org/
- TF-IDF Concept: https://en.wikipedia.org/wiki/Tf%E2%80%93idf

### For NLP
- NLTK Book: https://www.nltk.org/book/
- SpaCy Documentation: https://spacy.io/

### For Generative AI
- Groq API Docs: https://console.groq.com/docs/
- Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering

### For Web Development
- Flask Documentation: https://flask.palletsprojects.com/
- MDN Web Docs: https://developer.mozilla.org/

---

## 🎯 Viva Questions & Answers

### Q1: Difference between ML and LLM?
**A:** 
- **ML Models** (like our subject classifier): Learn patterns from labeled data, make discrete predictions, lightweight
- **LLMs** (like Groq): Pre-trained on massive text, generate human-like text, require API calls

### Q2: Why use Naive Bayes for classification?
**A:**
- Fast training and prediction
- Works well with text data
- Computationally efficient
- Easy to explain to stakeholders

### Q3: What does TF-IDF do?
**A:**
- Converts text to numerical features
- Emphasizes important words
- Removes common words (high-frequency)
- Essential for ML algorithms

### Q4: How does the preprocessing pipeline work?
**A:**
1. Remove noise (URLs, special chars)
2. Normalize (lowercase, remove punctuation)
3. Break into words (tokenization)
4. Remove common words (stopwords)
5. Reduce to base form (lemmatization)

### Q5: Why store data as JSON?
**A:**
- Human-readable format
- Easy to inspect during development
- No database setup required
- Beginner-friendly for learning

### Q6: How does retraining improve performance?
**A:**
- New data = better patterns
- More diverse examples = generalization
- Automatic learning from interactions
- Demonstrates concept of continuous improvement

---

## 🚀 Future Enhancements

- [ ] User authentication & profiles
- [ ] Question recommendation system
- [ ] Multi-language support
- [ ] Advanced visualizations (charts, graphs)
- [ ] Chatbot-style conversation
- [ ] Integration with educational platforms
- [ ] Mobile app version
- [ ] Real-time collaborative learning

---

## 📄 License & Attribution

This project is created for educational purposes as part of 2nd-year AIML curriculum.

### Credits
- **Groq AI**: Generative explanations
- **Scikit-learn**: ML models
- **NLTK**: NLP processing
- **Flask**: Web framework

---

## 👨‍💻 Author

**EduSolve AI Team**  
Created: February 2026  
Purpose: 2nd-Year AIML Academic Project  
GitHub Portfolio Project ⭐

---

## 📞 Support & Contact

For issues, questions, or improvements:
1. Check the Troubleshooting section
2. Review API endpoint documentation
3. Verify `.env` configuration
4. Check backend server logs

---

## 🎓 Viva Preparation Checklist

- [ ] Understand the complete application flow
- [ ] Know the purpose of each file
- [ ] Be able to explain ML vs LLM
- [ ] Understand the preprocessing pipeline
- [ ] Know how to train and save models
- [ ] Explain the API architecture
- [ ] Be familiar with the tech stack
- [ ] Understand error handling approaches
- [ ] Know how to scale this application
- [ ] Be prepared with optimization ideas

---

**Made with ❤️ for AIML Students**  
*Empowering knowledge through AI*

```
   ╔════════════════════════════════════╗
   ║     EduSolve AI - Learn Better!    ║
   ║     🎓 Your AI Study Buddy 🤖      ║
   ╚════════════════════════════════════╝
```
#   E d u S o l v e _ A i  
 