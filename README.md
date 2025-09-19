# 📰 NewsDashboard

A streamlined dashboard for exploring and analyzing news content.  
Key features include bias detection, snippet finding, retrieval-augmented generation (RAG), and news summarization.

---

### 🎥 Demo

Click the image below to watch the demo:

<p align="center">
  <a href="https://www.youtube.com/watch?v=KnU6oNDmrB8">
    <img src="https://img.youtube.com/vi/KnU6oNDmrB8/hqdefault.jpg" alt="Watch the demo" width="720">
  </a>
</p>

---

### 🗺️ Feature Overview

**Frontend**
- Interactive dashboard with quick news snippets  
  → [`nextjs-app`](https://github.com/Lingotech-Davis/NewsDashboard/tree/main/nextjs-app)

**Backend**
- News scraping and extraction  
  → [`news.py`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/backend/src/router/news.py)
- Bias detection via fine-tuned DistilBERT  
  → [`bias.py`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/backend/src/router/bias.py)
- Snippet retrieval based on user queries  
  → [`db.py`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/backend/src/router/db.py)
- RAG: Reduce hallucinations with source-grounded prompts  
  → [`rag.py`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/backend/src/router/rag.py)
- NLP-based news summarization  
  → [`summarize.py`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/backend/src/router/summarize.py)

---

#### 📊 Practice Notebooks

**Classification & Analysis**
- Fake news detection  
  → [`FakeNews_Classifier.ipynb`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/practice/FakeNews_Classifier.ipynb)
- Political bias detection  
  → [`BiasDetection_Classifier.ipynb`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/practice/BiasDetection_Classifier.ipynb)
- Political bias EDA  
  → [`political_bias_eda.ipynb`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/practice/political_bias_eda.ipynb)

**Context Aware AI**
- Retrieval-Augmented Generation  
  → [`RAG.ipynb`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/practice/RAG.ipynb)

**Other Tools**
- Recursive web crawler  
  → [`Recursive_WebScraper.ipynb`](https://github.com/Lingotech-Davis/NewsDashboard/blob/main/practice/Recursive_WebScraper.ipynb)

---

### 📚 Learn More

Explore the repo for implementation details, model architecture, and backend API logic.  
Feedback is always welcomed!
