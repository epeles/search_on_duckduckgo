# DuckDuckGo Search Automation 🦆

A Python-based automation tool that performs searches on DuckDuckGo using Selenium WebDriver. This script automates the search process, retrieves results, and displays them in a structured format.

## 📋 Overview

This project utilizes Selenium to automate searches on the DuckDuckGo search engine. It defines a class named `Duckduckgo` which inherits from the Chrome WebDriver. The script navigates to DuckDuckGo's main page, performs a search using a specified term, retrieves and prints the titles and URLs of the search results, and supports loading additional result pages by clicking the "more" button.

## ✨ Features

- **Headless Browser**: Runs Chrome in headless mode for efficient operation
- **Automatic WebDriver Management**: Uses `webdriver-manager` to handle ChromeDriver installation
- **Multiple Pages Support**: Automatically loads more results (up to 10 pages)
- **Error Handling**: Robust error handling for timeouts and missing elements
- **Input Validation**: Validates search terms before execution
- **User-Friendly Output**: Displays numbered results with URLs

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/epeles/search_on_duckduckgo.git
   cd search_on_duckduckgo
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

Run the script from the terminal with your search term:

```bash
python bot/run.py "your search term"
```

### Example

```bash
python bot/run.py "Python automation"
```

### Output Example

```
1. Python Automation Tutorial, URL: https://example.com/tutorial
2. Best Python Automation Tools, URL: https://example.com/tools
3. Automating Tasks with Python, URL: https://example.com/tasks
...
Total pages loaded: 3
```

## 🏗️ Project Structure

```
search_on_duckduckgo/
├── bot/
│   ├── duckduckgo/
│   │   ├── constants.py       # Configuration constants
│   │   └── duckduckgo.py      # Main automation class
│   └── run.py                 # Entry point script
├── .gitignore                 # Git ignore file
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

## 🔧 How It Works

1. **Initialization**: The script initializes a Chrome WebDriver in headless mode
2. **Navigation**: Navigates to DuckDuckGo's homepage
3. **Search Execution**: Enters the search term and submits the query
4. **Results Collection**: Waits for results to load and collects them
5. **Pagination**: Automatically clicks "more results" button to load additional pages (max 10)
6. **Output**: Displays all collected results with their URLs
7. **Cleanup**: Properly closes the browser session

## 🛡️ Error Handling

The script includes comprehensive error handling for:

- **Missing search term**: Validates that a search term is provided
- **Empty search term**: Ensures the search term is not empty or whitespace
- **Timeout errors**: Handles cases where results take too long to load
- **Missing elements**: Gracefully handles missing "more results" buttons
- **No results found**: Informs the user when no results are available

## 📦 Dependencies

- **selenium** (>=4.0.0): Browser automation framework
- **webdriver-manager** (>=3.8.0): Automatic WebDriver management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Eitan Peles**
- GitHub: [@epeles](https://github.com/epeles)
- Website: [https://epeles.github.io/resume/](https://epeles.github.io/resume/)

## 🔄 Recent Updates

- Fixed `quit()` method bug (missing parentheses)
- Added input validation and error handling
- Implemented maximum page limit to prevent infinite loops
- Added `requirements.txt` for easy dependency management
- Added `.gitignore` for Python projects
- Improved user feedback and error messages
