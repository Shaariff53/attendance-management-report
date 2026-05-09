# Milestone 3: Design & Architecture

## 3.1 System Architecture — Layered MVC + Microservices

The system follows a modern **Layered Architecture with Microservices** pattern, combining the scalability of microservices with the clarity of layered architecture.

```
┌─────────────────────────────────────────────────────────────┐
│             Presentation Layer (View)                         │
│  React Native Mobile App  |  React.js Web Portal              │
│  (iOS 14+, Android 10+)   |  (Chrome, Firefox, Safari)        │
└─────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────┐
│         API Gateway (Nginx/Kong) — Port 443                   │
│  ├─ Request Routing                                           │
│  ├─ Rate Limiting (100 req/min per user)                      │
│  ├─ SSL/TLS 1.3 Encryption                                    │
│  └─ Load Balancing (round-robin across services)              │
└─────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────┐
│        Controller Layer (REST API Controllers)                │
│  Express.js with Routing:                                     │
│  ├─ /api/auth/* → Auth Controller                             │
│  ├─ /api/sessions/* → Session Controller                      │
│  ├─ /api/attendance/* → Attendance Controller                 │
│  └─ /api/reports/* → Reporting Controller                     │
└─────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────┐
│    Business Logic Layer (Microservices)                       │
│  ├─ Auth Service (Port 3001)                                  │
│  ├─ Session Service (Port 3002)                               │
│  ├─ Verification Service (Port 3003)                          │
│  ├─ Attendance Service (Port 3004)                            │
│  ├─ Notification Service (Port 3005)                          │
│  └─ Reporting Service (Port 3006)                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────┐
│    Data Access Layer (Repository Pattern / ORM)               │
│  ├─ Sequelize ORM (Node.js models)                            │
│  ├─ Connection Pooling (30 active connections)                │
│  └─ Redis Caching (session data, frequently accessed records) │
└─────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────┐
│           Database Layer                                      │
│  ├─ PostgreSQL (relational, primary data store)               │
│  ├─ Redis (cache, sessions, rate limits)                      │
│  └─ MongoDB (audit logs, unstructured data)                   │
└─────────────────────────────────────────────────────────────┘
```

**Key Architectural Decisions:**

1. **Separation of Concerns:** Each service owns its business logic and data
2. **Scalability:** Services can be deployed independently and scaled horizontally
3. **Resilience:** Failure in one service doesn't cascade to others
4. **Technology Diversity:** Can use different tech stacks per service (Python for ML, Node.js for APIs)

## 3.2 Microservices Breakdown

| Service | Port | Responsibility | Tech Stack | Scaling |
|---------|------|-----------------|------------|---------|
| **Auth Service** | 3001 | User login, JWT issuance, role management, token refresh | Node.js, Express, bcrypt, jsonwebtoken | Replicated (2-3 instances) |
| **Session Service** | 3002 | Create/manage class sessions, HMAC-signed QR generation, expiry tracking | Node.js, Express, UUID, crypto, NodeSchedule | Auto-scaled (min 2, max 5) |
| **Verification Service** | 3003 | Facial recognition, geo-fence calculation, BLE proximity validation | Python, FastAPI, TensorFlow, FaceNet, NumPy | Auto-scaled (min 1, max 3 - GPU heavy) |
| **Attendance Service** | 3004 | Record CRUD, state machine management, override workflow | Node.js, Express, PostgreSQL, Sequelize | Replicated (2-4 instances) |
| **Notification Service** | 3005 | Email/SMS/push dispatch, retry logic, template management | Node.js, Express, Firebase FCM, Twilio, Bull Queue | Auto-scaled (queue-based, 3-6 workers) |
| **Reporting Service** | 3006 | Data aggregation, PDF/CSV export, analytics calculations | Node.js, Express, PDFKit, ExcelJS, PostgreSQL | Batch-triggered (on-demand) |
| **API Gateway** | 443 | Routing, rate limiting, SSL termination, load balancing | Nginx / Kong Gateway | Always available (2 instances, failover) |

## 3.3 Database Schema (Key Tables)

### Users Table
```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('student', 'instructor', 'admin') NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Students Table
```sql
CREATE TABLE students (
  student_id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(user_id),
  enrollment_no VARCHAR(20) UNIQUE NOT NULL,
  department VARCHAR(100),
  semester INTEGER,
  face_embedding_hash VARCHAR(1024),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Sessions Table
```sql
CREATE TABLE sessions (
  session_id UUID PRIMARY KEY,
  section_id UUID NOT NULL REFERENCES course_sections(section_id),
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  qr_hash VARCHAR(256) NOT NULL,
  qr_expiry TIMESTAMP NOT NULL,
  geo_fence_json JSONB,
  status ENUM('SCHEDULED', 'ACTIVE', 'GRACE_PERIOD', 'CLOSED') DEFAULT 'SCHEDULED',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);
```

### Attendance Records Table
```sql
CREATE TABLE attendance_records (
  record_id UUID PRIMARY KEY,
  session_id UUID NOT NULL REFERENCES sessions(session_id),
  student_id UUID NOT NULL REFERENCES students(student_id),
  status ENUM('PRESENT', 'ABSENT', 'LATE', 'EXCUSED') NOT NULL,
  method_used ENUM('facial', 'qr', 'manual') NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  location_hash VARCHAR(256),
  state ENUM('NOT_MARKED', 'MARKED', 'LATE', 'ABSENT', 'EXCUSED', 'CORRECTED', 'LOCKED'),
  locked_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);
```

### Audit Logs Table
```sql
CREATE TABLE audit_logs (
  log_id UUID PRIMARY KEY,
  record_id UUID REFERENCES attendance_records(record_id),
  action_type VARCHAR(50) NOT NULL,
  actor_id UUID NOT NULL REFERENCES users(user_id),
  reason VARCHAR(500),
  old_value VARCHAR(500),
  new_value VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Notifications Table
```sql
CREATE TABLE notifications (
  notif_id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES students(student_id),
  type ENUM('email', 'sms', 'push') NOT NULL,
  message TEXT NOT NULL,
  channel VARCHAR(100),
  status ENUM('pending', 'sent', 'failed') DEFAULT 'pending',
  sent_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Indexes for Performance:**
```sql
CREATE INDEX idx_student_enrollment ON students(enrollment_no);
CREATE INDEX idx_session_section ON sessions(section_id);
CREATE INDEX idx_attendance_session_student ON attendance_records(session_id, student_id);
CREATE INDEX idx_attendance_status ON attendance_records(status);
CREATE INDEX idx_audit_record ON audit_logs(record_id);
```

## 3.4 State Machine Diagram — Session Lifecycle

**Session States:**

1. **SCHEDULED**
   - Initial state when session is created
   - Awaiting start_time
   - Transitions to ACTIVE

2. **ACTIVE**
   - Instructor starts session
   - Students can mark attendance
   - QR code is active (10 min TTL)
   - Transitions to GRACE_PERIOD when end_time reached

3. **GRACE_PERIOD**
   - 15-minute window after official end time
   - Students can still mark attendance as LATE
   - Instructor can regenerate QR if needed
   - Transitions to CLOSED

4. **CLOSED**
   - Grace period expired
   - Attendance locked from editing (except admin)
   - Report can be generated
   - Can transition to CORRECTION (admin only)

5. **CORRECTION**
   - Admin reopens session for corrections
   - 24-hour correction window
   - All changes logged in audit trail
   - Transitions back to CLOSED

6. **FINALIZED**
   - Attendance report generated
   - Immutable state
   - Used for archival

7. **CANCELLED**
   - Session cancelled (instructor/admin action)
   - All students marked ABSENT (unless already marked)
   - No manual overrides possible

**State Transition Rules:**
```
SCHEDULED
  ├─→ ACTIVE (Instructor starts session)
  └─→ CANCELLED

ACTIVE
  ├─→ GRACE_PERIOD (End time reached)
  └─→ CANCELLED

GRACE_PERIOD
  ├─→ CLOSED (Grace period expires)
  └─→ CANCELLED

CLOSED
  ├─→ CORRECTION (Admin reopens)
  ├─→ FINALIZED (Report generated)
  └─→ CANCELLED

CORRECTION
  └─→ CLOSED (After 24h or admin closes)

CANCELLED (terminal state)
```

## Deployment Architecture

**Development Environment:**
- Local services on separate ports
- SQLite for lightweight testing
- Mock external APIs

**Staging Environment:**
- Docker containers (docker-compose)
- PostgreSQL + Redis + MongoDB
- CloudFlare CDN for static assets

**Production Environment:**
- Kubernetes (k8s) for orchestration
- AWS RDS for PostgreSQL
- AWS ElastiCache for Redis
- AWS DocumentDB for MongoDB
- CloudFront CDN
- Auto-scaling based on CPU/memory metrics

## Security Architecture

1. **API Security:**
   - JWT tokens (HS256 algorithm)
   - 24-hour token expiry
   - Refresh token rotation
   - Rate limiting (100 req/min)

2. **Data Security:**
   - Face embeddings stored as hashed vectors (never raw images)
   - Passwords hashed with bcrypt (10 rounds)
   - TLS 1.3 for all transport

3. **Application Security:**
   - CORS policy restricted to app domain
   - SQL injection prevention via parameterized queries
   - XSS protection via Content Security Policy (CSP)
   - CSRF tokens on state-changing operations
