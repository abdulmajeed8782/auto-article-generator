import sys
import os
from openai import OpenAI
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QSpinBox, QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Worker thread to handle API requests
class ArticleGeneratorThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)

    def __init__(self, api_key, topics, titles, anchor_texts, num_articles, output_dir):
        super().__init__()
        self.api_key = api_key
        self.topics = topics
        self.titles = titles
        self.anchor_texts = anchor_texts
        self.num_articles = num_articles
        self.output_dir = output_dir
        self.stop_flag = False

    def run(self):
        client = OpenAI(
            base_url="https://api.novita.ai/v3/openai",
            api_key=self.api_key
        )

        model = "meta-llama/llama-3.1-8b-instruct"
        max_tokens = 1024

        for i in range(self.num_articles):
            if self.stop_flag:
                self.log.emit("Article generation stopped by user.")
                break

            title = self.titles[i % len(self.titles)]
            topic = self.topics[i % len(self.topics)] if self.topics else ""
            anchor_text = self.anchor_texts[i % len(self.anchor_texts)] if self.anchor_texts else ""

            prompt = f"Title: {title}\n"
            if topic:
                prompt += f"Topic: {topic}\n"
            if anchor_text:
                prompt += f"Anchor Text Keywords: {anchor_text}\n"
            prompt += "\nPlease generate an article based on the above information."

            try:
                self.log.emit(f"Generating article {i + 1} of {self.num_articles}...")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens
                )
                article_content = response.choices[0].message.content.strip()
                file_name = f"article_{i + 1}.txt"
                file_path = os.path.join(self.output_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(article_content)
                self.log.emit(f"Article {i + 1} saved as {file_name}.")
            except Exception as e:
                self.log.emit(f"Error generating article {i + 1}: {str(e)}")

            self.progress.emit(int(((i + 1) / self.num_articles) * 100))

    def stop(self):
        self.stop_flag = True

# Main application window
class DeepSeekApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.generator_thread = None

    def init_ui(self):
        self.setWindowTitle('Novita Article Generator')
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Novita AI API Key:'))
        self.api_key_input = QLineEdit()
        layout.addWidget(self.api_key_input)

        layout.addWidget(QLabel('Main Topics (one per line, optional):'))
        self.topics_input = QTextEdit()
        layout.addWidget(self.topics_input)

        layout.addWidget(QLabel('Titles (one per line):'))
        self.titles_input = QTextEdit()
        layout.addWidget(self.titles_input)

        layout.addWidget(QLabel('Anchor Text Keywords (one per line, optional):'))
        self.anchor_texts_input = QTextEdit()
        layout.addWidget(self.anchor_texts_input)

        layout.addWidget(QLabel('Number of Articles to Generate:'))
        self.num_articles_input = QSpinBox()
        self.num_articles_input.setRange(1, 100)
        layout.addWidget(self.num_articles_input)

        layout.addWidget(QLabel('Output Directory:'))
        dir_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        dir_layout.addWidget(self.output_dir_input)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_output_directory)
        dir_layout.addWidget(browse_button)
        layout.addLayout(dir_layout)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_generation)
        button_layout.addWidget(self.start_button)
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_generation)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        layout.addWidget(QLabel('Log Output:'))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def browse_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if dir_path:
            self.output_dir_input.setText(dir_path)

    def start_generation(self):
        api_key = self.api_key_input.text().strip()
        topics = [line.strip() for line in self.topics_input.toPlainText().splitlines() if line.strip()]
        titles = [line.strip() for line in self.titles_input.toPlainText().splitlines() if line.strip()]
        anchor_texts = [line.strip() for line in self.anchor_texts_input.toPlainText().splitlines() if line.strip()]
        num_articles = self.num_articles_input.value()
        output_dir = self.output_dir_input.text().strip()

        if not api_key or not titles or not output_dir:
            QMessageBox.warning(self, "Missing Info", "Please fill in all required fields.")
            return

        if not os.path.isdir(output_dir):
            QMessageBox.warning(self, "Invalid Directory", "Output directory does not exist.")
            return

        self.progress_bar.setValue(0)
        self.log_output.clear()

        self.generator_thread = ArticleGeneratorThread(api_key, topics, titles, anchor_texts, num_articles, output_dir)
        self.generator_thread.progress.connect(self.progress_bar.setValue)
        self.generator_thread.log.connect(self.log_output.append)
        self.generator_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_generation(self):
        if self.generator_thread:
            self.generator_thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DeepSeekApp()
    window.show()
    sys.exit(app.exec_())
