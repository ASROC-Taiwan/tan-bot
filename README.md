# TANBot
**TANBot** automatically converts data from a Google Sheet into JSON and Markdown formats for use on the TAN website.


##  📦 Installation
```bash
pip install .
```

## 🔧 Usage

1. Create a .env file in your project root:

```
SHEET_ID=<the sheet id>
WORKSHEET_GID=<the worksheet gid>
LINE_TOKEN=<the line message api token>
```

2. Use the following code to generate Hugo posts:

```python
from tanbot import TANBot

bot = TANBot()
bot.load_gsheet()
has_updated = bot.hugo.generate_posts()
```

## ❌ Uninstallation
```
pip unintall tanbot
```
