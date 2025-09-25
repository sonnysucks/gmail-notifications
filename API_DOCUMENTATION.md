# 📡 API Documentation
## Gmail Photography Appointment Scheduler - Web API Reference

**Version**: 2.0  
**Base URL**: `http://localhost:5001`  
**Authentication**: Session-based (cookies)

---

## 🔐 **Authentication**

All API endpoints require authentication via session cookies. The web application uses Flask-Login for session management.

### **Login**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

### **Logout**
```http
GET /logout
```

---

## 📅 **Appointments API**

### **List Appointments**
```http
GET /appointments
```

**Response**:
```json
{
  "appointments": [
    {
      "id": 1,
      "client_name": "Sarah Johnson",
      "session_type": "Newborn Session",
      "start_time": "2024-01-15 10:00:00",
      "duration": 180,
      "status": "scheduled",
      "baby_name": "Baby Emma",
      "total_amount": 350.00
    }
  ]
}
```

### **Get Appointment Details**
```http
GET /appointments/<id>
```

**Response**:
```json
{
  "id": 1,
  "client_id": 1,
  "client_name": "Sarah Johnson",
  "client_email": "sarah@email.com",
  "session_type": "Newborn Session",
  "start_time": "2024-01-15 10:00:00",
  "end_time": "2024-01-15 13:00:00",
  "duration": 180,
  "status": "scheduled",
  "notes": "First baby, very excited parents",
  "baby_name": "Baby Emma",
  "baby_age_days": 7,
  "session_fee": 350.00,
  "total_amount": 350.00,
  "payment_status": "pending"
}
```

### **Create Appointment**
```http
POST /appointments
Content-Type: application/json

{
  "client_name": "Sarah Johnson",
  "client_email": "sarah@email.com",
  "session_type": "Newborn Session",
  "start_time": "2024-01-15 10:00:00",
  "duration": 180,
  "baby_name": "Baby Emma",
  "baby_age_days": 7,
  "session_fee": 350.00,
  "notes": "First baby session"
}
```

### **Update Appointment**
```http
PUT /appointments/<id>
Content-Type: application/json

{
  "status": "confirmed",
  "notes": "Updated notes"
}
```

### **Delete Appointment**
```http
DELETE /appointments/<id>
```

---

## 👥 **Clients API**

### **List Clients**
```http
GET /clients
```

**Response**:
```json
{
  "clients": [
    {
      "id": 1,
      "name": "Sarah Johnson",
      "email": "sarah@email.com",
      "phone": "+1-555-0123",
      "children_count": 1,
      "children_names": ["Baby Emma"],
      "created_at": "2024-01-01 00:00:00"
    }
  ]
}
```

### **Get Client Details**
```http
GET /clients/<id>
```

### **Create Client**
```http
POST /clients
Content-Type: application/json

{
  "name": "Sarah Johnson",
  "email": "sarah@email.com",
  "phone": "+1-555-0123",
  "address": "123 Main St, City, State",
  "children_count": 1,
  "children_names": ["Baby Emma"],
  "children_birth_dates": ["2024-01-08"]
}
```

### **Update Client**
```http
PUT /clients/<id>
Content-Type: application/json

{
  "phone": "+1-555-0124",
  "children_count": 2
}
```

### **Delete Client**
```http
DELETE /clients/<id>
```

---

## 📊 **Analytics API**

### **Revenue Data**
```http
GET /api/analytics/revenue
```

**Response**:
```json
{
  "total_revenue": 4500.00,
  "monthly_data": {
    "2024-01": {"revenue": 1200.00, "count": 3},
    "2024-02": {"revenue": 1500.00, "count": 4}
  },
  "labels": ["Jan 2024", "Feb 2024", "Mar 2024"],
  "data": [1200.00, 1500.00, 1800.00]
}
```

### **Session Statistics**
```http
GET /api/analytics/sessions
```

**Response**:
```json
{
  "total_sessions": 15,
  "by_type": {
    "Newborn Session": 5,
    "Milestone Session": 8,
    "Smash Cake Session": 2
  },
  "labels": ["Newborn", "Milestone", "Smash Cake"],
  "data": [5, 8, 2]
}
```

### **Client Metrics**
```http
GET /api/analytics/clients
```

**Response**:
```json
{
  "total_clients": 25,
  "new_clients_this_month": 3,
  "by_family_type": {
    "Newborn": 8,
    "Baby": 12,
    "Toddler": 5
  },
  "labels": ["Newborn", "Baby", "Toddler"],
  "data": [8, 12, 5]
}
```

---

## 💾 **Backup & Restore API**

### **Create Backup**
```http
POST /api/backup
```

**Response**:
```json
{
  "success": true,
  "message": "Backup created successfully!",
  "filename": "gmail_notifications_backup_20240924_211948.json",
  "file_size": 21318,
  "backup_path": "/path/to/backup/file.json"
}
```

### **List Backups**
```http
GET /api/backup/list
```

**Response**:
```json
{
  "success": true,
  "backups": [
    {
      "filename": "gmail_notifications_backup_20240924_211948.json",
      "file_size": 21318,
      "created_time": "2024-09-24T21:19:48",
      "created_date": "2024-09-24 21:19:48",
      "backup_info": {
        "created_at": "2024-09-24T21:19:48",
        "version": "1.0",
        "system": "Gmail Notifications System"
      }
    }
  ]
}
```

### **Delete Backup**
```http
DELETE /api/backup/delete/<filename>
```

**Response**:
```json
{
  "success": true,
  "message": "Backup deleted successfully"
}
```

### **Restore Backup**
```http
POST /api/backup/restore
Content-Type: application/json

{
  "filename": "gmail_notifications_backup_20240924_211948.json"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Backup restored successfully"
}
```

---

## 📦 **Packages API**

### **List All Packages**
```http
GET /api/packages
```

**Response**:
```json
{
  "success": true,
  "packages": [
    {
      "id": "package-uuid",
      "name": "Newborn Essentials",
      "description": "Comprehensive newborn session within the first 14 days",
      "category": "newborn",
      "base_price": 350.00,
      "duration_minutes": 180,
      "is_customizable": true,
      "includes": ["2-3 hours session", "25 edited digital images", "Online gallery"],
      "recommended_age": "5-14 days",
      "is_active": true,
      "is_featured": true,
      "display_order": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### **Get Active Packages**
```http
GET /api/packages/active
```

### **Get Packages by Category**
```http
GET /api/packages/category/<category>
```

**Categories**: `newborn`, `maternity`, `milestone`, `birthday`, `family`

### **Get Specific Package**
```http
GET /api/packages/<package_id>
```

### **Create Package**
```http
POST /api/packages
Content-Type: application/json

{
  "name": "Newborn Essentials",
  "description": "Comprehensive newborn session",
  "category": "newborn",
  "base_price": 350.00,
  "duration_minutes": 180,
  "is_customizable": true,
  "includes": ["2-3 hours session", "25 edited digital images"],
  "recommended_age": "5-14 days",
  "is_active": true,
  "is_featured": true
}
```

### **Update Package**
```http
PUT /api/packages/<package_id>
Content-Type: application/json

{
  "base_price": 375.00,
  "description": "Updated description"
}
```

### **Delete Package**
```http
DELETE /api/packages/<package_id>
```

---

## 📄 **Client Packet Generation API**

### **Generate Client Packet**
```http
GET /api/client-packet/<client_id>?package_id=<package_id>
```

**Parameters**:
- `client_id`: Required client ID
- `package_id`: Optional package ID to highlight in packet

**Response**: HTML content (print-ready client packet)

**Features**:
- Client information and session history
- Recommended packages based on family type
- Selected package highlighting (if package_id provided)
- Business information and policies
- Professional formatting for printing

---

## 📋 **Configuration API**

### **Get Configuration**
```http
GET /api/config
```

**Response**:
```json
{
  "business": {
    "name": "Your Photography Business",
    "email": "your@email.com",
    "phone": "+1-XXX-XXX-XXXX"
  },
  "calendar": {
    "target_calendar_id": "primary",
    "timezone": "America/New_York"
  },
  "appointments": {
    "session_types": [
      {
        "name": "Newborn Session",
        "duration": 180,
        "base_price": 350
      }
    ]
  }
}
```

### **Update Configuration**
```http
PUT /api/config
Content-Type: application/json

{
  "business": {
    "name": "Updated Business Name"
  }
}
```

---

## 🚨 **Error Responses**

### **Authentication Error**
```json
{
  "error": "Authentication required",
  "status": 401
}
```

### **Validation Error**
```json
{
  "error": "Validation failed",
  "details": {
    "client_name": "This field is required",
    "email": "Invalid email format"
  },
  "status": 400
}
```

### **Not Found Error**
```json
{
  "error": "Resource not found",
  "status": 404
}
```

### **Server Error**
```json
{
  "error": "Internal server error",
  "status": 500
}
```

---

## 🔧 **Usage Examples**

### **Create Appointment with Client**
```bash
# 1. Create client
curl -X POST http://localhost:5001/clients \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Sarah Johnson",
    "email": "sarah@email.com",
    "phone": "+1-555-0123"
  }'

# 2. Create appointment
curl -X POST http://localhost:5001/appointments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "client_name": "Sarah Johnson",
    "session_type": "Newborn Session",
    "start_time": "2024-01-15 10:00:00",
    "duration": 180,
    "session_fee": 350.00
  }'
```

### **Backup System**
```bash
# Create backup
curl -X POST http://localhost:5001/api/backup \
  -b cookies.txt

# List backups
curl -X GET http://localhost:5001/api/backup/list \
  -b cookies.txt

# Delete backup
curl -X DELETE http://localhost:5001/api/backup/delete/backup_file.json \
  -b cookies.txt
```

---

## 📝 **Notes**

- All timestamps are in ISO format (`YYYY-MM-DD HH:MM:SS`)
- All monetary amounts are in decimal format (e.g., `350.00`)
- Session cookies are required for all authenticated endpoints
- The API follows RESTful conventions
- Error responses include appropriate HTTP status codes
- All responses are in JSON format

---

**This API documentation covers all available endpoints for the Gmail Photography Appointment Scheduler web application.** 🎯📸👶
