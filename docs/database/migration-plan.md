# Database Migration Plan

## Version 1.0.0 - Initial Schema

### Tables

1. vehicles
```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number_plate TEXT UNIQUE NOT NULL,
    contact_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    entry_timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_vehicles_number_plate ON vehicles(number_plate);
CREATE INDEX idx_vehicles_entry_timestamp ON vehicles(entry_timestamp);
```

2. system_config
```sql
CREATE TABLE system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    retention_hours INTEGER NOT NULL DEFAULT 24,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert default configuration
INSERT INTO system_config (retention_hours) VALUES (24);
```

3. audit_logs
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- Indexes
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity, entity_id);
```

## Future Migrations

### Version 1.1.0 - Enhanced Vehicle Tracking
```sql
-- Add vehicle type classification
ALTER TABLE vehicles ADD COLUMN vehicle_type TEXT;
ALTER TABLE vehicles ADD COLUMN parking_spot TEXT;

-- Add parking spot management
CREATE TABLE parking_spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_number TEXT UNIQUE NOT NULL,
    vehicle_type TEXT,
    is_occupied BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Version 1.2.0 - Payment Integration
```sql
-- Add payment tracking
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_status TEXT NOT NULL,
    payment_method TEXT,
    transaction_id TEXT UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- Add payment status to vehicles
ALTER TABLE vehicles ADD COLUMN payment_status TEXT;
```

### Version 1.3.0 - Rate Configuration
```sql
-- Add parking rate configuration
CREATE TABLE parking_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT NOT NULL,
    rate_per_hour DECIMAL(10,2) NOT NULL,
    minimum_hours INTEGER DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Migration Guidelines

### Pre-migration Checks
1. Backup existing database
2. Verify disk space availability
3. Check for active connections
4. Validate current schema version

### Migration Process
1. Use Alembic for version control
2. Run migrations during low-traffic periods
3. Implement rollback procedures
4. Validate data integrity post-migration

### Post-migration Tasks
1. Update indexes
2. Analyze query performance
3. Update application code
4. Update documentation

## Rollback Procedures

### Quick Rollback
```sql
-- For each version, create down migrations
-- Example for v1.1.0
ALTER TABLE vehicles DROP COLUMN vehicle_type;
ALTER TABLE vehicles DROP COLUMN parking_spot;
DROP TABLE parking_spots;
```

### Emergency Procedures
1. Stop application servers
2. Restore from backup
3. Verify data integrity
4. Restart application servers

## Data Migration

### Data Cleanup
```sql
-- Remove expired vehicle records
DELETE FROM vehicles 
WHERE entry_timestamp < datetime('now', '-' || (
    SELECT retention_hours FROM system_config LIMIT 1
) || ' hours');

-- Archive old audit logs
INSERT INTO audit_logs_archive 
SELECT * FROM audit_logs 
WHERE timestamp < datetime('now', '-90 days');
```

### Data Validation
```sql
-- Verify data integrity
SELECT COUNT(*) FROM vehicles;
SELECT COUNT(*) FROM audit_logs;
SELECT COUNT(*) FROM system_config;

-- Check for orphaned records
SELECT v.* FROM vehicles v
LEFT JOIN audit_logs a ON v.id = a.entity_id
WHERE a.id IS NULL;
```

## Performance Optimization

### Index Optimization
```sql
-- Analyze index usage
ANALYZE;
PRAGMA index_list('vehicles');
PRAGMA index_info('idx_vehicles_number_plate');

-- Add composite indexes for common queries
CREATE INDEX idx_vehicles_status_timestamp 
ON vehicles(payment_status, entry_timestamp);
```

### Query Optimization
1. Use prepared statements
2. Implement connection pooling
3. Regular VACUUM operations
4. Monitor query performance

## Monitoring

### Key Metrics
1. Migration duration
2. Table sizes
3. Index sizes
4. Query performance
5. Error rates

### Alerts
1. Migration failures
2. Data validation errors
3. Performance degradation
4. Disk space warnings

## Documentation Requirements

### Version Documentation
1. Schema version number
2. Changes in each version
3. Dependencies between migrations
4. Known issues and workarounds

### Operational Documentation
1. Backup procedures
2. Recovery procedures
3. Monitoring setup
4. Performance tuning