# Milestone 2: System Modeling

## 2.1 Context Diagram (Level 0 DFD)

The context diagram shows the Smart Attendance System at the highest level, depicting the system as a single bubble with external entities and systems:

**External Entities:**
- Students
- Instructors
- Admin

**External Systems:**
- LMS/ERP
- Email/SMS Service
- Google Maps API
- Face Recognition API
- Firebase FCM

**Data Flows:**
- Students → System: Attendance data, face images, QR scans
- Instructors → System: Session creation, QR generation, manual overrides
- Admin → System: User management, system configuration
- System → LMS/ERP: Attendance records, reports
- System → Notification Services: Email, SMS, push notifications

## 2.2 Level 1 DFD — Major Processes

The Level 1 DFD expands the system into five major processes:

### P1 - Authentication & Authorization
- Handles user login
- Issues JWT tokens
- Manages role-based access control (RBAC)
- Validates user permissions

### P2 - Session Management
- Creates class sessions
- Generates HMAC-signed QR codes
- Manages session state (SCHEDULED → ACTIVE → GRACE_PERIOD → CLOSED)
- Handles session expiry and regeneration

### P3 - Verification Engine
- Performs facial recognition on captured images
- Calculates geo-fence boundaries
- Detects BLE/Wi-Fi proximity
- Validates combined verification results

### P4 - Attendance Recording
- Records attendance marks from verified students
- Manages attendance state machine
- Handles manual overrides with audit trails
- Generates confirmation messages

### P5 - Reporting & Analytics
- Aggregates attendance data
- Generates daily, weekly, and semester reports
- Exports reports as PDF/CSV
- Sends automated notifications

## 2.3 Class Diagram

**Core Classes:**

### User (Abstract Base Class)
- user_id: UUID
- name: String
- email: String
- password_hash: String
- role: UserRole
- created_at: DateTime

### Student (extends User)
- enrollment_no: String
- department: String
- semester: Integer
- face_embedding_hash: Vector

### Instructor (extends User)
- employee_id: String
- department: String

### Course
- course_id: UUID
- course_code: String
- course_name: String
- credit_hours: Integer

### CourseSection
- section_id: UUID
- section_code: String
- room: String
- schedule_json: JSON
- course_id: FK
- instructor_id: FK

### Session
- session_id: UUID
- start_time: DateTime
- end_time: DateTime
- qr_hash: String (HMAC)
- geo_fence_json: JSON
- status: SessionStatus
- section_id: FK

### AttendanceRecord
- record_id: UUID
- status: AttendanceStatus (PRESENT, ABSENT, LATE, EXCUSED)
- method_used: String (facial, qr, manual)
- timestamp: DateTime
- location_hash: String
- state: RecordState
- session_id: FK
- student_id: FK

### AuditLog
- log_id: UUID
- action_type: String
- actor_id: UUID
- reason: String
- old_value: String
- new_value: String
- record_id: FK
- created_at: DateTime

## 2.4 Sequence Diagram — Mark Attendance

**Facial Recognition Flow:**

1. **Student → App:** Opens attendance interface
2. **App → Camera Module:** Request face capture
3. **App → Verification Svc:** Send face image + QR data
4. **Verification Svc → ML Model:** Process facial recognition
5. **ML Model:** Return face confidence (>0.85 = match)
6. **Verification Svc:** Validate QR signature and timestamp
7. **Verification Svc:** Check GPS geo-fence (±50m)
8. **Verification Svc → Attendance Svc:** Return verification result
9. **Attendance Svc → Database:** Record attendance (PRESENT)
10. **Attendance Svc → Notification Svc:** Send confirmation
11. **Notification Svc → Student App:** Display success message

## 2.5 Activity Diagram — Student Marks Attendance

```
Start
  ↓
[Student opens app]
  ↓
[Scan QR code]
  ↓
Decision: QR valid?
  ├─ NO → [Show error] → End
  └─ YES
       ↓
    [Capture face from camera]
       ↓
    Decision: Face verified? (conf ≥ 0.85)
       ├─ NO → [Show error] → End
       └─ YES
            ↓
         [Check GPS geo-fence]
            ↓
         Decision: Within 50m?
            ├─ NO → [Show error] → End
            └─ YES
                 ↓
              [Record attendance]
                 ↓
              [Send confirmation]
                 ↓
              [Display success message]
                 ↓
              End
```

## 2.6 State Diagram — AttendanceRecord Lifecycle

**States:**
- **NOT_MARKED:** Initial state, no attendance recorded
- **MARKED:** Attendance marked via facial/QR verification
- **LATE:** Marked after session grace period (grace period = 15 min)
- **ABSENT:** No attendance marked before session ends
- **EXCUSED:** Admin/Instructor manually marked as excused with reason
- **CORRECTED:** Record manually overridden with audit entry
- **LOCKED:** 48-hour immutable state, requires admin unlock

**Transitions:**
```
NOT_MARKED → MARKED (on verification)
           → ABSENT (on session end without mark)
           → EXCUSED (on manual override)

MARKED → LATE (if marked after grace period)
      → CORRECTED (on manual edit within 48h)
      → LOCKED (after 48h)

ABSENT → EXCUSED (on manual override)
      → CORRECTED (on manual edit within 48h)
      → LOCKED (after 48h)

EXCUSED → LOCKED (after 48h)

CORRECTED → LOCKED (after 48h)

LOCKED → CORRECTED (on admin unlock + edit)
```

## Integration Points

**Database Connections:**
- Users table → Students, Instructors, Admins
- Courses table → CourseSection
- CourseSection → Sessions, Enrollments
- Sessions → AttendanceRecord
- AttendanceRecord → AuditLog

**External API Calls:**
- Google Maps Geofencing API
- TensorFlow/FaceNet ML Service
- Firebase Cloud Messaging (FCM)
- Twilio SMS Service

## Data Validation Rules

1. **Face Embeddings:** Stored as 128-dim vectors, never raw images
2. **QR Codes:** HMAC-signed, valid for 600 seconds only
3. **GPS Coordinates:** Validated within 50m of classroom
4. **Enrollment Numbers:** Format: 01-XXXXXX-XXX (Bahria standard)
5. **Timestamps:** All records use UTC timezone
