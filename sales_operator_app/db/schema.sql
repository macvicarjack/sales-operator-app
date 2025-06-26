-- Sales Operator Database Schema

-- Leads table
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company TEXT,
    email TEXT,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    customer_name TEXT,
    customer_tier TEXT CHECK (customer_tier IN ('A', 'B', 'C')),
    potential_revenue REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_action_date TIMESTAMP,
    next_followup_date TIMESTAMP,
    due_date DATE,
    type TEXT CHECK (type IN ('normal', 'quick')) DEFAULT 'normal',
    status TEXT CHECK (status IN ('open', 'waiting', 'done')) DEFAULT 'open',
    completed_at TIMESTAMP
);

-- Create indexes for tasks table
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(type);
CREATE INDEX IF NOT EXISTS idx_tasks_customer_tier ON tasks(customer_tier);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_next_followup_date ON tasks(next_followup_date);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_customer_name ON tasks(customer_name);
