```markdown
# Plants & Pots 🌱  
_Naturally beautiful, purely yours_

An online plant nursery web app built with Flask and MySQL. Browse a catalog of houseplants, view details, add **multiple different plants** to your cart, and “checkout” (clearing your cart for now). Designed to run on AWS Free Tier (RDS + Elastic Beanstalk).

---

## 🔍 Features

- **User Authentication**  
  – Register & Login with username & password  
  – Session-based login using `Flask-Session`

- **Plant Catalog**  
  – Browse all plants (image, name, description, price, stock)  
  – Responsive grid layout

- **Plant Detail & Cart**  
  – View full details for any plant  
  – Add a chosen quantity to your cart  
  – Support for selecting **multiple different** plants

- **Shopping Cart**  
  – View cart with line-item totals  
  – “Checkout” button clears cart (stub for payment)

- **Admin / Data**  
  – MySQL schema for `plants`, `users`, `orders`, `order_items`  
  – Seeded sample data  

---

## 🛠️ Tech Stack

| Layer            | Tech / Service                          | Free-Tier Notes                           |
| ---------------- | --------------------------------------- | ----------------------------------------- |
| **Backend**      | Python 3, Flask                         |                                           |
| **DB**           | MySQL on AWS RDS (db.t2.micro, gp2 gp)  | Free Tier RDS instance                    |
| **Sessions**     | Flask-Session (filesystem)              |                                           |
| **Auth**         | Werkzeug security (hashing/checking)    |                                           |
| **Frontend**     | Jinja2 templates, HTML5, CSS            | Static assets via S3 + CloudFront later   |
| **Hosting**      | AWS Elastic Beanstalk (Python)          | Free Tier EB environment                 |
| **Domain & CDN** | Route 53 + CloudFront (optional)        | Free Tier eligible                       |

---

## 🚀 Quick Start

1. **Clone this repo**  
   ```bash
   git clone https://github.com/Meenakshi1402/plants_and_pots.git
   cd plants_and_pots
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install Flask Flask-MySQLdb Flask-Session Werkzeug
   ```

4. **Configure your database**  
   - Launch a MySQL RDS instance (Free Tier)  
   - Note your endpoint, username & password  
   - In `app.py`, update:
     ```python
     app.config.update(
       MYSQL_HOST='your-rds-endpoint',
       MYSQL_USER='your-db-user',
       MYSQL_PASSWORD='your-db-pass',
       MYSQL_DB='plants_and_pots',
       ...
     )
     ```

5. **Initialize the schema & sample data**  
   ```sql
   -- Connect to your RDS MySQL:
   CREATE DATABASE plants_and_pots;
   USE plants_and_pots;

   CREATE TABLE users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     username VARCHAR(50) UNIQUE NOT NULL,
     password_hash VARCHAR(255) NOT NULL,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE plants (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(100) NOT NULL,
     description TEXT,
     price DECIMAL(8,2) NOT NULL,
     image_url VARCHAR(255),
     stock_qty INT NOT NULL
   );

   -- Insert sample plants:
   INSERT INTO plants (name, description, price, image_url, stock_qty) VALUES
     ('Snake Plant', 'Low-light tolerant, air-purifying plant.', 19.99, '/static/images/snake.jpg', 12),
     ('Monstera Deliciosa', 'Iconic split-leaf philodendron.', 29.99, '/static/images/monstera.jpg', 8),
     ('Pothos', 'Easy-care trailing vine.', 14.99, '/static/images/pothos.jpg', 20),
     ('Tulasi (Holy Basil)', 'Sacred basil with medicinal properties.', 9.99, '/static/images/tulsi.jpg', 15);
   ```

6. **Run the app locally**  
   ```bash
   python app.py
   ```
   Open your browser at <http://127.0.0.1:5000>.

---

## 🖼️ Folder Structure

```
plants_and_pots/
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── welcome.css
│   └── images/
│       ├── snake.jpg
│       ├── monstera.jpg
│       ├── pothos.jpg
│       └── tulsi.jpg
├── templates/
│   ├── welcome.html
│   ├── register.html
│   ├── login.html
│   ├── plants.html
│   ├── detail.html
│   └── cart.html
└── .gitignore
```

---

## 📦 Deploying to AWS (Free Tier)

1. **Push to GitHub**  
2. **Create Elastic Beanstalk app**  
   - Platform: Python  
   - Connect to your GitHub repo  
3. **Set environment variables** for DB creds in EB console  
4. **Upload static assets** to S3 + serve via CloudFront  
5. **Point custom domain** via Route 53 + ACM SSL  

---

## 🤝 Contributing

1. Fork this repo  
2. Create a feature branch: `git checkout -b feat/YourFeature`  
3. Commit & push: `git commit -m "Add awesome feature"`  
4. Open a Pull Request  

---


