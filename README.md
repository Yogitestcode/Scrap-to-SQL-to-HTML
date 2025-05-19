# Scrap-to-SQL-to-HTML

A Flask-based application that scrapes book data from the web and stores it in a MySQL database (via XAMPP/phpMyAdmin).

### 🔧 Features
- ✅ User registration & login (Flask-Login)
- ✅ Add / update / delete book entries
- ✅ HTML front-end to manage books
- ✅ SQL (XAMPP) backend integration

---

## 📦 Requirements

- Python 3.x
- Flask
- MySQL (XAMPP/phpMyAdmin)
- BeautifulSoup4
- Requests

---

⚙️ Setup Instructions
1. Clone this repo
```bash 
git clone https://github.com/Yogitestcode/Scrap-to-SQL-to-HTML.git
cd Scrap-to-SQL-to-HTML
```
2. Start MySQL (XAMPP)
-Open XAMPP Control Panel
-Start MySQL and Apache

3. Import Database
-Go to http://localhost/phpmyadmin
-Create a database: books_db
-Import the file books.sql from this project

4. Create Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
5. Run the App
```bash
flask run
```


## ▶️ Notes
If you're using a custom MySQL username/password, update it in:
```bash
app/config.py  # or wherever your DB URI is set
```
Example:
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://youruser:yourpassword@localhost/books_db'
```
