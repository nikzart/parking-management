# Parking Management System API Documentation

Version: 1.0.0


A robust parking management system API that handles vehicle tracking and automated data cleanup.

Features:
- Vehicle registration and tracking
- Automated data cleanup based on retention period
- Comprehensive audit logging
- Real-time vehicle search
- Rate limiting and security measures


## Authentication

All endpoints require API key authentication

Type: API Key  
Header: X-API-Key

## Endpoints

### Create Vehicle

Register a new vehicle entry

**Method:** POST  
**Path:** /api/v1/vehicles

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "body": {
    "number_plate": "TEST0E1195",
    "contact_name": "Test User",
    "phone_number": "+1234567890"
  }
}
```

**Response:**
Status Code: 201
```json
{
  "number_plate": "TEST0E1195",
  "contact_name": "Test User",
  "phone_number": "+1234567890",
  "id": 1,
  "entry_timestamp": "2025-01-26T10:25:20.558722"
}
```

### List Vehicles

List all active vehicles with pagination

**Method:** GET  
**Path:** /api/v1/vehicles

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "items": [
    {
      "number_plate": "TEST0E1195",
      "contact_name": "Test User",
      "phone_number": "+1234567890",
      "id": 1,
      "entry_timestamp": "2025-01-26T10:25:20.558722"
    }
  ],
  "pagination": {
    "total": 1,
    "skip": 0,
    "limit": 50,
    "current_page": 1,
    "total_pages": 1,
    "total_items": 1,
    "per_page": 50
  }
}
```

### Get Vehicle

Get vehicle details by number plate

**Method:** GET  
**Path:** /api/v1/vehicles/{number_plate}

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "path_params": {
    "number_plate": "TEST0E1195"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "number_plate": "TEST0E1195",
  "contact_name": "Test User",
  "phone_number": "+1234567890",
  "id": 1,
  "entry_timestamp": "2025-01-26T10:25:20.558722"
}
```

### Search Vehicles

Search vehicles by number plate or contact name

**Method:** GET  
**Path:** /api/v1/vehicles/search/{term}

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "path_params": {
    "term": "TES"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "items": [
    {
      "number_plate": "TEST0E1195",
      "contact_name": "Test User",
      "phone_number": "+1234567890",
      "id": 1,
      "entry_timestamp": "2025-01-26T10:25:20.558722"
    }
  ],
  "pagination": {
    "total": 1,
    "skip": 0,
    "limit": 50,
    "current_page": 1,
    "total_pages": 1,
    "total_items": 1,
    "per_page": 50
  }
}
```

### Remove Vehicle

Remove a vehicle entry

**Method:** DELETE  
**Path:** /api/v1/vehicles/{number_plate}

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "path_params": {
    "number_plate": "TEST0E1195"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "number_plate": "TEST0E1195",
  "contact_name": "Test User",
  "phone_number": "+1234567890",
  "id": 1,
  "entry_timestamp": "2025-01-26T10:25:20.558722"
}
```

### Get Retention Period

Get current data retention period

**Method:** GET  
**Path:** /api/v1/config/retention

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "retention_hours": 24,
  "id": 1
}
```

### Update Retention Period

Update data retention period

**Method:** PUT  
**Path:** /api/v1/config/retention

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "body": {
    "retention_hours": 48
  }
}
```

**Response:**
Status Code: 200
```json
{
  "retention_hours": 48,
  "id": 1
}
```

### Clear Database

Clear entire database (requires confirmation)

**Method:** POST  
**Path:** /api/v1/config/maintenance/clear

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "body": {
    "confirmation": "I understand this will delete all data"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "message": "Database cleared successfully",
  "timestamp": "2025-01-26T10:25:20.576473",
  "records_removed": 0
}
```

### Get Audit Logs

Get all audit logs with pagination

**Method:** GET  
**Path:** /api/v1/audit

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "items": [
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:25:20.573016",
      "id": 174
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 removed",
      "timestamp": "2025-01-26T10:25:20.569106",
      "id": 173
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 registered",
      "timestamp": "2025-01-26T10:25:20.559363",
      "id": 172
    },
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:23:32.729462",
      "id": 171
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TEST603ECF removed",
      "timestamp": "2025-01-26T10:23:32.725536",
      "id": 170
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TEST603ECF registered",
      "timestamp": "2025-01-26T10:23:32.715766",
      "id": 169
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "6",
      "details": "Vehicle XYZ789 registered",
      "timestamp": "2025-01-26T10:19:47.395045",
      "id": 168
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle ABC123 registered",
      "timestamp": "2025-01-26T10:19:47.392294",
      "id": 167
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TEST8F76BB removed",
      "timestamp": "2025-01-26T10:19:47.380597",
      "id": 166
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TEST8F76BB registered",
      "timestamp": "2025-01-26T10:19:47.377883",
      "id": 165
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "4",
      "details": "Vehicle TEST3DB7DC registered",
      "timestamp": "2025-01-26T10:19:47.364818",
      "id": 164
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "3",
      "details": "Vehicle TEST5B727F registered",
      "timestamp": "2025-01-26T10:19:47.344283",
      "id": 163
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "2",
      "details": "Vehicle TESTA49F7C registered",
      "timestamp": "2025-01-26T10:19:47.332287",
      "id": 162
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST7E7741 registered",
      "timestamp": "2025-01-26T10:19:47.322965",
      "id": 161
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "14",
      "details": "Vehicle TEST446ACD registered",
      "timestamp": "2025-01-26T10:19:47.296453",
      "id": 160
    },
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:19:47.273190",
      "id": 159
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "13",
      "details": "Vehicle TEST7C3AFD registered",
      "timestamp": "2025-01-26T10:19:47.239172",
      "id": 158
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "12",
      "details": "Vehicle TEST4 registered",
      "timestamp": "2025-01-26T10:19:47.224867",
      "id": 157
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "11",
      "details": "Vehicle TEST3 registered",
      "timestamp": "2025-01-26T10:19:47.222092",
      "id": 156
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "10",
      "details": "Vehicle TEST2 registered",
      "timestamp": "2025-01-26T10:19:47.202607",
      "id": 155
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "9",
      "details": "Vehicle TEST1 registered",
      "timestamp": "2025-01-26T10:19:47.194923",
      "id": 154
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TEST0 registered",
      "timestamp": "2025-01-26T10:19:47.181953",
      "id": 153
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TEST3A6F97 removed",
      "timestamp": "2025-01-26T10:19:47.164670",
      "id": 152
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TEST3A6F97 registered",
      "timestamp": "2025-01-26T10:19:47.161308",
      "id": 151
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TEST13E13F registered",
      "timestamp": "2025-01-26T10:19:47.145092",
      "id": 150
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "6",
      "details": "Vehicle XYZ789 registered",
      "timestamp": "2025-01-26T10:18:49.048573",
      "id": 149
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle ABC123 registered",
      "timestamp": "2025-01-26T10:18:49.045474",
      "id": 148
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TESTCC751C removed",
      "timestamp": "2025-01-26T10:18:49.033450",
      "id": 147
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TESTCC751C registered",
      "timestamp": "2025-01-26T10:18:49.030363",
      "id": 146
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "4",
      "details": "Vehicle TEST7A9183 registered",
      "timestamp": "2025-01-26T10:18:49.015927",
      "id": 145
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "3",
      "details": "Vehicle TEST6F97F7 registered",
      "timestamp": "2025-01-26T10:18:48.993168",
      "id": 144
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "2",
      "details": "Vehicle TEST30F2C3 registered",
      "timestamp": "2025-01-26T10:18:48.981384",
      "id": 143
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST71FA65 registered",
      "timestamp": "2025-01-26T10:18:48.971710",
      "id": 142
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "14",
      "details": "Vehicle TEST5898A4 registered",
      "timestamp": "2025-01-26T10:18:48.944911",
      "id": 141
    },
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:18:48.921022",
      "id": 140
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "13",
      "details": "Vehicle TESTAEAC1D registered",
      "timestamp": "2025-01-26T10:18:48.886687",
      "id": 139
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "12",
      "details": "Vehicle TEST4 registered",
      "timestamp": "2025-01-26T10:18:48.872281",
      "id": 138
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "11",
      "details": "Vehicle TEST3 registered",
      "timestamp": "2025-01-26T10:18:48.869470",
      "id": 137
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "10",
      "details": "Vehicle TEST2 registered",
      "timestamp": "2025-01-26T10:18:48.850649",
      "id": 136
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "9",
      "details": "Vehicle TEST1 registered",
      "timestamp": "2025-01-26T10:18:48.847307",
      "id": 135
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TEST0 registered",
      "timestamp": "2025-01-26T10:18:48.844311",
      "id": 134
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TESTE3C7A9 removed",
      "timestamp": "2025-01-26T10:18:48.830660",
      "id": 133
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "8",
      "details": "Vehicle TESTE3C7A9 registered",
      "timestamp": "2025-01-26T10:18:48.827480",
      "id": 132
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TESTAD2CD1 registered",
      "timestamp": "2025-01-26T10:18:48.811320",
      "id": 131
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "6",
      "details": "Vehicle XYZ789 registered",
      "timestamp": "2025-01-26T10:15:29.083301",
      "id": 130
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle ABC123 registered",
      "timestamp": "2025-01-26T10:15:29.080522",
      "id": 129
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TESTD5034F removed",
      "timestamp": "2025-01-26T10:15:29.069336",
      "id": 128
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TESTD5034F registered",
      "timestamp": "2025-01-26T10:15:29.066844",
      "id": 127
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "4",
      "details": "Vehicle TEST01A58E registered",
      "timestamp": "2025-01-26T10:15:29.054787",
      "id": 126
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "3",
      "details": "Vehicle TEST49841C registered",
      "timestamp": "2025-01-26T10:15:29.035239",
      "id": 125
    }
  ],
  "pagination": {
    "total": 174,
    "skip": 0,
    "limit": 50,
    "current_page": 1,
    "total_pages": 4,
    "total_items": 174,
    "per_page": 50
  }
}
```

### Get Entity Logs

Get audit logs for a specific entity

**Method:** GET  
**Path:** /api/v1/audit/entity/{entity}

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "path_params": {
    "entity": "Vehicle"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "items": [
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 removed",
      "timestamp": "2025-01-26T10:25:20.569106",
      "id": 173
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 registered",
      "timestamp": "2025-01-26T10:25:20.559363",
      "id": 172
    }
  ],
  "pagination": {
    "total": 162,
    "skip": 0,
    "limit": 2,
    "current_page": 1,
    "total_pages": 81,
    "total_items": 162,
    "per_page": 2
  }
}
```

### Get Recent Logs

Get most recent audit logs

**Method:** GET  
**Path:** /api/v1/audit/recent

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  }
}
```

**Response:**
Status Code: 200
```json
{
  "items": [
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:25:20.573016",
      "id": 174
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 removed",
      "timestamp": "2025-01-26T10:25:20.569106",
      "id": 173
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "1",
      "details": "Vehicle TEST0E1195 registered",
      "timestamp": "2025-01-26T10:25:20.559363",
      "id": 172
    },
    {
      "action": "UPDATE",
      "entity": "SystemConfig",
      "entity_id": "1",
      "details": "Retention period updated to 48 hours",
      "timestamp": "2025-01-26T10:23:32.729462",
      "id": 171
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TEST603ECF removed",
      "timestamp": "2025-01-26T10:23:32.725536",
      "id": 170
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "7",
      "details": "Vehicle TEST603ECF registered",
      "timestamp": "2025-01-26T10:23:32.715766",
      "id": 169
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "6",
      "details": "Vehicle XYZ789 registered",
      "timestamp": "2025-01-26T10:19:47.395045",
      "id": 168
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle ABC123 registered",
      "timestamp": "2025-01-26T10:19:47.392294",
      "id": 167
    },
    {
      "action": "DELETE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TEST8F76BB removed",
      "timestamp": "2025-01-26T10:19:47.380597",
      "id": 166
    },
    {
      "action": "CREATE",
      "entity": "Vehicle",
      "entity_id": "5",
      "details": "Vehicle TEST8F76BB registered",
      "timestamp": "2025-01-26T10:19:47.377883",
      "id": 165
    }
  ],
  "pagination": {
    "total": 174,
    "skip": 0,
    "limit": 10,
    "current_page": 1,
    "total_pages": 18,
    "total_items": 174,
    "per_page": 10
  }
}
```

### Unauthorized Access

Example of unauthorized access

**Method:** GET  
**Path:** /api/v1/vehicles

**Request:**
```json
{}
```

**Response:**
Status Code: 401
```json
{
  "detail": "API key required"
}
```

### Invalid Input

Example of invalid input validation

**Method:** PUT  
**Path:** /api/v1/config/retention

**Request:**
```json
{
  "headers": {
    "X-API-Key": "your-secret-key-here"
  },
  "body": {
    "retention_hours": -1
  }
}
```

**Response:**
Status Code: 400
```json
{
  "detail": "1 validation error for SystemConfigUpdate\nretention_hours\n  Input should be greater than 0 [type=greater_than, input_value=-1, input_type=int]\n    For further information visit https://errors.pydantic.dev/2.5/v/greater_than"
}
```

