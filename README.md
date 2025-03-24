# 🧠 Novita AI Article Generator (PyQt)

Generate high-quality articles automatically using the Novita AI LLMs via a clean and responsive Python PyQt5 GUI. This tool allows you to enter a list of topics, titles, and anchor keywords and bulk generate `.txt` article files with full logging and a progress bar.

---

## 🚀 Features

- ✅ Beautiful GUI built with PyQt5
- ✅ API Key validation
- ✅ Title, topic, and keyword input
- ✅ Set number of articles to generate
- ✅ Multi-threaded article generation (UI won’t freeze)
- ✅ Save each article as `.txt` file
- ✅ Real-time progress bar and logs
- ✅ Supports [Novita AI](https://novita.ai/referral?invited_code=2HWJHB) LLMs (compatible with OpenAI SDK)

---

## 🔧 Requirements

- Python 3.8+
- `PyQt5`
- `openai>=1.0.0`

Install dependencies:

```bash
pip install PyQt5 'openai>=1.0.0'
```

---

## 📦 How to Use

1. Clone this repository or download the source.
2. Run the app:

```bash
python artbot.py
```

3. In the GUI:
   - Paste your **Novita AI API key**  
     ➤ Get FREE API credits here: [Claim API Credits on Novita](https://novita.ai/referral?invited_code=2HWJHB)
   - Enter your **topics**, **titles**, and **anchor keywords** (one per line)
   - Choose how many articles to generate
   - Set the output folder
   - Click **Start**

4. Each generated article will be saved as `article_1.txt`, `article_2.txt`, ... in your output folder

---

## 🧠 Powered by Novita AI

This app uses Novita’s OpenAI-compatible API:

- Base URL: `https://api.novita.ai/v3/openai`
- Supported Model: `meta-llama/llama-3.1-8b-instruct`
- Docs: https://novita.ai/guides/quickstart
- API Key: [Get yours here](https://novita.ai/referral?invited_code=2HWJHB)

---

## 💬 Example Prompt Format

```
Title: The Future of Robotics
Topic: Robotics
Anchor Text Keywords: AI, automation, bionics

Please generate an article based on the above information.
```

---

## 🛠 Customize / Extend

- 💡 Add support for Markdown or .docx export
- 💡 Support more models via dropdown menu
- 💡 Option to enable streaming or retry failed requests

---

## 🙌 Contribute

PRs welcome. Fork this repo and open a pull request.

---

## 📣 Call To Action

💸 **Get FREE API Credits** for Novita AI with this link:

👉 [Click to Claim Now!](https://novita.ai/referral?invited_code=2HWJHB)

---

## 📄 License

MIT
