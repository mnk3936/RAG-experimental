# RAG Experimental System

This project is an experimental **Retrieval-Augmented Generation (RAG)** system that leverages language models to generate responses using both model knowledge and relevant provided context.  
The system is designed for flexibility, allowing you to modify the context and experiment with different API keys and models.

---

## Features

- **Retrieval-Augmented Generation:** Enhances language model outputs using custom or external knowledge.
- **OpenRouter API Integration:** Easily switch or insert your own model API keys via environment variables.
- **Editable Context:** Manually edit or replace the context with your own data for tailored experiments.
- **Simple Setup:** Minimal requirements for quick experimentation.

---

## Getting Started

### Prerequisites

- Python 3.8+ installed
- Access to OpenRouter or supported model API
- (Optional) Your own data or knowledge base for custom context

### Installation

Clone the repository and install dependencies:
``
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
pip install -r requirements.txt
``

### Configuration

#### 1. API Key Setup

Set your API key as an environment variable.

**On Linux/Mac:**
``
export OPENROUTER_API_KEY=<your_key_here>
``

**On Windows:**
``
set OPENROUTER_API_KEY=<your_key_here>
``

#### 2. Context Configuration

You may edit the `context.txt` or relevant section in the configuration file to input your own data or context for the RAG system.

> **Note:** Be careful not to include sensitive personal information in your context.

---

## Usage

Run the main script (modify the filename as needed):


``
python main.py
``

- The system will prompt for a query and return a response from the language model, enhanced by your provided context.

---

## Customization

- **Switching Models:** Change the model used by editing the configuration file or environment variable if you wish to test different models supported by OpenRouter.
- **Updating Context:** Replace or modify the context file to test how the model performs with your own data.

---

## Security and Privacy

- Be cautious with your API keys. **Never share them publicly.**
- Do not add personally identifiable information or sensitive data to your context file, especially if sharing the system.

---

## License

This project is for experimental and educational use. Adapt or extend it as you wish.

---

## Acknowledgments

- [OpenRouter](https://openrouter.ai/) for API and model access.

---

Feel free to adapt, extend, and contribute!



