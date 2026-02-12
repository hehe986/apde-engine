# APDE Engine — Automatic Parameter Discovery Engine

> Lightweight • Modular • Fast  
> Built for Authorized Security Testing & Research

APDE Engine is a lightweight and extensible parameter discovery framework designed to assist security researchers in identifying exposed or undocumented parameters in web applications.

Built with a modular architecture and a clean CLI interface, APDE Engine provides a structured and scalable approach to parameter analysis.

---

## 🚀 Why APDE Engine?

- ⚡ Fast concurrent scanning  
- 🧩 Modular engine design  
- 📄 Structured JSON reporting  
- 🗂 Extensible wordlist system  
- 🖥 Clean and intuitive CLI  
- 🔧 Easy to extend and customize  

---

## ✨ Features

- Automated parameter discovery
- Concurrent request handling
- Intelligent response analysis
- JSON export support
- Scalable project structure
- Clean separation of engine components

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/hehe986/apde-engine.git
cd apde-engine
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🛠 Usage

### 🔹 Basic Scan

```bash
python main.py --url https://example.com
```

### 🔹 Custom Wordlist

```bash
python main.py --url https://example.com --wordlist wordlists/custom.txt
```

### 🔹 Save JSON Report

```bash
python main.py --url https://example.com --output reports/result.json
```

### 🔹 Advanced Configuration

```bash
python main.py \
    --url https://example.com \
    --threads 10 \
    --timeout 15 \
    --output reports/example.json
```
