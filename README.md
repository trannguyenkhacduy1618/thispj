# Time Tracking App

## 1. Giới thiệu dự án

Time Tracking App là ứng dụng theo dõi thời gian làm việc của người dùng trên các công việc (task).  
Hệ thống cho phép ghi nhận thời gian làm việc, thống kê theo ngày, xuất báo cáo và hỗ trợ quản lý hiệu suất hoặc tính lương (billing).

Ứng dụng được xây dựng theo mô hình **Frontend – Backend – Database**, có thể triển khai trên môi trường local và Ubuntu Server.

---

## 2. Chức năng chính

- Quản lý công việc (Task)
- Bắt đầu / tạm dừng / kết thúc bộ đếm thời gian (Timer)
- Lưu trữ thời gian làm việc theo từng ngày
- Thống kê tổng thời gian làm việc
- Xuất dữ liệu báo cáo (Timesheet)
- Giao tiếp Frontend – Backend thông qua RESTful API

---

## 3. Kiến trúc hệ thống

Hệ thống được thiết kế theo mô hình **3-tier architecture**:

```
User
  |
Frontend (React)
  |
HTTP + JWT
  |
Backend (FastAPI)
  |
PostgreSQL
```

---

## 4. Công nghệ sử dụng

### Backend
- Python 3
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- PostgreSQL

### Frontend
- JavaScript
- Node.js
- React (Vite)

### Hạ tầng & Công cụ
- Nginx
- systemd
- Git

---

## 5. Cấu trúc thư mục

```
project/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── migrations/
│   ├── schemas/
│   ├── main.py
│   └── settings.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .env
├── alembic.ini
├── requirements.txt
├── run.sh
├── nixpacks.toml
└── README.md
```

---

## 6. Yêu cầu hệ thống

- Ubuntu 20.04+
- Python 3.9+
- Node.js & npm
- PostgreSQL
- Nginx

---

## 7. Cấu hình môi trường

File `.env`:

```
DATABASE_URL=postgresql://time_tracker_user:password@localhost:5432/time_tracker_db
SECRET_KEY=your_secret_key
```

---

## 8. Hướng dẫn cài đặt và triển khai

### 8.1. Cài đặt package

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git postgresql postgresql-contrib
```

### 8.2. Clone project

```bash
mkdir /var/www
cd /var/www
git clone <LINK_TO_YOUR_REPOSITORY> time_tracker
cd time_tracker
```

### 8.3. Backend (FastAPI)

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 8.4. Frontend (React)

```bash
cd frontend
npm install
npm run build
sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
```

---

## 9. Truy cập hệ thống

- Frontend: `http://<SERVER_IP>`  
- Backend API: `http://<SERVER_IP>:8000`

---

## 10. Ghi chú

- Dự án phục vụ mục đích học tập và nghiên cứu
- Có thể mở rộng thêm: phân quyền người dùng, báo cáo nâng cao, tích hợp calendar, billing theo giờ

