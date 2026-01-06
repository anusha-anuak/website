# 👟 BuyNexa - Premium E-Commerce Shoe Store

BuyNexa is a modern, high-performance e-commerce platform built with Django, designed specifically for premium footwear retailers. It features a sleek user interface, robust product management, and a seamless shopping experience.

![BuyNexa Banner](https://github.com/anusha-anuak/website/raw/main/banner.png)

## 🚀 Key Features

- **Storefront & Catalog**: Browse products by category (Sneakers, Formal, Boots, for example) with beautiful imagery and detailed descriptions.
- **Shopping Cart**: Fully functional cart system with the ability to add, update, and remove items.
- **Secure Authentication**: Integrated with `django-allauth` for secure login, signup, and Google Social Auth.
- **Order Management**: Comprehensive checkout process with order tracking and status updates (Pending, Processing, Shipped, Delivered).
- **Admin Dashboard**: Powerful administrative control over products, categories, users, and orders.
- **Responsive Design**: Optimized for both desktop and mobile devices for a fluid shopping experience.

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Django 5.x
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Database**: SQLite3 (Development)
- **Authentication**: Django Allauth (Social & Local)
- **Image Processing**: Pillow (for product/category images)

## 📁 Project Structure

```text
online website/
├── src/
│   ├── BuyNexa/          # Project configuration & settings
│   ├── store/           # Main application logic (models, views, forms)
│   ├── static/          # CSS, JS, and global assets
│   ├── templates/       # HTML templates
│   ├── media/           # User-uploaded product images
│   └── manage.py        # Django management script
├── venv/                # Virtual environment
├── .gitignore           # Git exclusion rules
└── requirements.txt     # Python dependencies
```

## ⚙️ Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anusha-anuak/website.git
   cd website
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   The site will be available at `http://127.0.0.1:8000/`.

## 🛡️ Admin Access
To access the admin panel (`/admin/`), create a superuser:
```bash
python manage.py createsuperuser
```

---
*Developed with ❤️ by [Anusha](https://github.com/anusha-anuak)*
