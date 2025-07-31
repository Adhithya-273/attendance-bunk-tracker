# 📊 College Attendance Tracker Web App

A simple yet powerful web application built with **Python**, **Flask**, and **Selenium** to automatically scrape, calculate, and display your college attendance. This tool helps you stay on top of your attendance requirements by showing your current percentage, how many classes you can afford to miss, and how many you need to attend to meet your target.

---

## ✨ Features

- **Automatic Scraping**: Securely logs into your college portal and fetches up-to-date attendance data in real-time.
- **Detailed Analysis**: For each subject, it calculates:
  - Your current attendance percentage.
  - The number of classes you must attend to reach your goal.
  - The maximum number of classes you can safely bunk.
- **Customizable Target**: Set your own attendance target (e.g., 75%, 80%, 85%).
- **User-Friendly Interface**: A clean, modern, and responsive UI built with **Tailwind CSS** for a great experience on any device.

---

## 🛠️ How It Works

This application uses a combination of powerful Python libraries:

- **Flask**: Acts as the back-end web server, handling user requests and displaying the results.
- **Selenium**: Automates a real web browser (Google Chrome) in the background to log in and navigate the college website just like a human would.
- **Beautiful Soup**: Parses the HTML of the attendance page to accurately extract the subject and attendance data.

---

## 🚀 Getting Started

Follow these steps to get the application running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Google Chrome
- ChromeDriver that exactly matches your Google Chrome version. You can [download it here](https://sites.google.com/a/chromium.org/chromedriver/).

### Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Install the required Python libraries
pip install Flask selenium beautifulsoup4
```

### 3. Configure ChromeDriver

Open the `app.py` file and find the following line:

```python
# --- Configuration ---
DRIVER_PATH = r"C:\path\to\your\chromedriver.exe"
```

> 🔧 **Important**: Change the path to the exact location where you saved your `chromedriver.exe` file.

---

## ▶️ How to Run

1. Open your command prompt or terminal.
2. Navigate to the project directory.
3. Run the following command to start the server:

```bash
python -m flask run
```

4. Open your web browser:
   You will see output similar to this:

```
 * Running on http://127.0.0.1:5000
```

Now visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser to view the app.

