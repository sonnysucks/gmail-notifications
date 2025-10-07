-- SnapStudio Database Schema
-- Professional Photography Business Management System
-- Cloudflare D1 Database Schema

-- Clients table
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    status TEXT DEFAULT 'scheduled',
    notes TEXT,
    session_fee DECIMAL(10,2) DEFAULT 0,
    payment_status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Packages table
CREATE TABLE IF NOT EXISTS packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    duration_minutes INTEGER NOT NULL,
    active BOOLEAN DEFAULT 1,
    featured BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Baby milestones table
CREATE TABLE IF NOT EXISTS baby_milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    baby_name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    milestone_type TEXT NOT NULL,
    milestone_date DATE NOT NULL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Birthday sessions table
CREATE TABLE IF NOT EXISTS birthday_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    child_name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    session_date DATE NOT NULL,
    age_years INTEGER NOT NULL,
    package_id INTEGER,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (package_id) REFERENCES packages(id)
);

-- Client notes table
CREATE TABLE IF NOT EXISTS client_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    note_type TEXT DEFAULT 'general',
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Correspondence table
CREATE TABLE IF NOT EXISTS correspondence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    client_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT DEFAULT 'draft',
    scheduled_send_time DATETIME,
    sent_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Session types table
CREATE TABLE IF NOT EXISTS session_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_appointments_client_id ON appointments(client_id);
CREATE INDEX IF NOT EXISTS idx_appointments_start_time ON appointments(start_time);
CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_packages_category ON packages(category);
CREATE INDEX IF NOT EXISTS idx_packages_active ON packages(active);
CREATE INDEX IF NOT EXISTS idx_baby_milestones_client_id ON baby_milestones(client_id);
CREATE INDEX IF NOT EXISTS idx_birthday_sessions_client_id ON birthday_sessions(client_id);
CREATE INDEX IF NOT EXISTS idx_client_notes_client_id ON client_notes(client_id);
CREATE INDEX IF NOT EXISTS idx_correspondence_appointment_id ON correspondence(appointment_id);
CREATE INDEX IF NOT EXISTS idx_correspondence_client_id ON correspondence(client_id);

-- Insert default session types
INSERT OR IGNORE INTO session_types (name, duration_minutes, base_price, description) VALUES
('Newborn Session', 180, 350.00, 'Professional newborn photography session'),
('Milestone Session', 60, 225.00, 'Baby milestone photography (3, 6, 9, 12 months)'),
('Birthday Session', 90, 275.00, 'Birthday celebration photography'),
('Family Session', 120, 300.00, 'Family portrait session'),
('Maternity Session', 90, 250.00, 'Maternity photography session');

-- Insert default packages
INSERT OR IGNORE INTO packages (name, category, description, base_price, duration_minutes) VALUES
('Newborn Essentials', 'newborn', 'Basic newborn session with 20 edited photos', 350.00, 180),
('Newborn Deluxe', 'newborn', 'Premium newborn session with 40 edited photos and props', 500.00, 240),
('Milestone Collection', 'milestone', '3 milestone sessions (3, 6, 9 months) with 15 photos each', 600.00, 180),
('First Year Package', 'milestone', 'Complete first year package with newborn and all milestones', 1200.00, 600),
('Family Portrait', 'family', 'Family session with 25 edited photos', 300.00, 120),
('Maternity & Newborn', 'maternity', 'Combined maternity and newborn session', 700.00, 300);
