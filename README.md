# AI Threat Analytics

AI Threat Analytics is an advanced cyber threat detection and mitigation system powered by machine learning. It analyzes network traffic data to predict and recommend mitigation strategies for potential cyber threats using AI-driven analytics.

## 📌 Features
- **Threat Detection & Prediction:** Uses AI models to analyze network traffic and detect threats.
- **Neural Network-Based Classification:** Employs an MLPClassifier for cyber threat classification.
- **AI-Driven Mitigation Suggestions:** Recommends countermeasures for detected threats.
- **FastAPI Web Interface:** Provides an easy-to-use web UI for interaction.
- **Scalable & Efficient:** Uses optimized data processing and sparse matrices for memory efficiency.

---

## 🚀 Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Virtual environment tool (venv or conda)
- Required Python libraries (see `requirements.txt`)

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/your-repo/AI_Threat_Analytics.git
cd AI_Threat_Analytics

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠 Usage

### 1️⃣ Data Preprocessing
Ensure your dataset (CICIDS2018) is preprocessed and stored as `.npy` files in the `processed_data/` directory.

### 2️⃣ Training the AI Model
To train the neural network model:
```bash
python3 src/train_nn.py
```
- The trained model is saved in the `models/` directory.
- Logs are stored in `models/nn_training.log`.

### 3️⃣ Running the Web Interface (FastAPI)
Start the FastAPI web UI for cyber threat analytics:
```bash
uvicorn src.app:app --reload
```
Visit `http://127.0.0.1:8000/docs` to access API endpoints.

---

## 📂 Project Structure
```
AI_Threat_Analytics/
│── src/
│   ├── train_nn.py       # Neural network training script
│   ├── app.py            # FastAPI web application
│   ├── preprocess.py     # Data preprocessing module
│── processed_data/       # Preprocessed dataset (.npy files)
│── models/               # Trained models & logs
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## 📊 Model Details
- **Algorithm:** Multi-Layer Perceptron (MLPClassifier)
- **Input:** Network traffic features
- **Output:** Threat class label
- **Optimization:** Uses OneHotEncoding with `sparse_output=True` for efficiency

---

## 📄 License


---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m "Added feature XYZ"`)
4. Push to the branch (`git push origin feature-xyz`)
5. Submit a Pull Request

---

## 📧 Contact
For questions or support, reach out at: [viditmanishshah@gmail.com](mailto:viditmanishshah@gmail.com)

