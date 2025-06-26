-- Sales Operator Database Schema (PostgreSQL)

-- Leads table
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    company VARCHAR(200),
    email VARCHAR(255),
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX idx_leads_email ON leads(email);

-- Create index on status for filtering
CREATE INDEX idx_leads_status ON leads(status);

-- Create index on created_at for sorting
CREATE INDEX idx_leads_created_at ON leads(created_at);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    customer_name VARCHAR(100),
    customer_tier VARCHAR(1) CHECK (customer_tier IN ('A', 'B', 'C')),
    potential_revenue DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_action_date TIMESTAMP,
    next_followup_date TIMESTAMP,
    due_date DATE,
    type VARCHAR(10) CHECK (type IN ('normal', 'quick')) DEFAULT 'normal',
    status VARCHAR(20) CHECK (status IN ('open', 'waiting', 'done')) DEFAULT 'open',
    completed_at TIMESTAMP
);

-- Create indexes for tasks table
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_type ON tasks(type);
CREATE INDEX idx_tasks_customer_tier ON tasks(customer_tier);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_next_followup_date ON tasks(next_followup_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_customer_name ON tasks(customer_name);
