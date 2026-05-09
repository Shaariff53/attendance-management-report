# Milestone 1: Requirements

## 1.1 Problem Statement

Traditional attendance systems rely on manual registers or basic biometric hardware (fingerprint readers, RFID cards). These are prone to proxy attendance, buddy punching, hardware failure, and high maintenance costs. In large universities like Bahria University with hundreds of students per batch, these approaches create administrative bottlenecks and inaccurate records.

The Smart Attendance System (Beyond Biometrics) leverages multiple automated channels — facial recognition, GPS geo-fencing, QR code scanning, and Wi-Fi/BLE proximity detection — to capture attendance seamlessly, accurately, and in real time without dedicated hardware.

## 1.2 Project Scope

### IN SCOPE:
- Automated attendance via facial recognition, GPS geo-fencing, QR codes, and BLE/Wi-Fi proximity
- Role-based access: Admin, Instructor, Student
- Real-time dashboards, attendance statistics, and analytics
- Notification system (email, SMS, push) for absentees and low-attendance warnings
- Reporting module: per student / class / department (CSV/PDF export)
- REST API integration with university LMS/ERP
- Mobile app (Android/iOS) and web portal

## 1.3 Functional Requirements

| FR # | Requirement | Priority |
|------|-------------|----------|
| FR-01 | System shall allow students to mark attendance via facial recognition using the device camera. | High |
| FR-02 | System shall verify student physical location via GPS geo-fencing before marking attendance. | High |
| FR-03 | System shall generate time-limited, single-use HMAC QR codes for each class session. | High |
| FR-04 | System shall detect student Wi-Fi/BLE proximity to classroom AP as secondary verification. | Medium |
| FR-05 | System shall allow instructors to manually override attendance records with a mandatory reason. | High |
| FR-06 | System shall send automated alerts when attendance falls below 75%. | High |
| FR-08 | System shall generate daily, weekly, and semester attendance reports. | High |
| FR-10 | System shall maintain an audit trail of all manual corrections with timestamps and actor ID. | High |

## 1.4 Non-Functional Requirements

| NFR # | Category | Requirement |
|-------|----------|-------------|
| NFR-01 | Performance | Facial recognition verification shall complete within 3 seconds under normal network. |
| NFR-02 | Scalability | System shall support 500 concurrent active class sessions without degradation. |
| NFR-03 | Availability | System shall maintain 99.5% uptime; maintenance only during off-peak hours. |
| NFR-04 | Security | Face data stored as hashed embeddings (vector), never as raw images. |
| NFR-05 | Security | All API communication uses TLS 1.3; JWT tokens expire within 24 hours. |
| NFR-06 | Usability | Student face enrollment (onboarding) completable in under 5 minutes. |
| NFR-07 | Reliability | Mobile app queues attendance locally if offline and syncs on reconnection. |
| NFR-08 | Compatibility | Mobile app supports Android 10+ and iOS 14+. |

## 1.5 Use Case Diagram

The use case diagram depicts five main use cases:
- UC-01: Mark Attendance
- UC-02: Generate Session QR
- UC-03: Generate Report
- UC-04: Manual Override
- UC-05: Manage Users

With actors: Student, Instructor, and Admin.

## 1.6 Use Case Descriptions

### UC-01: Mark Attendance

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-01 |
| **Use Case Name** | Mark Attendance |
| **Actor(s)** | Student, Instructor, System |
| **Pre-condition** | An active session exists; student is enrolled and authenticated; valid QR code is available. |
| **Main Flow** | 1. Instructor starts a session and generates QR (UC-02) 2. Student opens the attendance interface 3. Student scans the session QR code 4. System validates the QR code and student enrollment 5. System records attendance as Present with a timestamp 6. System displays a confirmation to the student |
| **Alternate Flow** | A1: If QR code has expired, system rejects the scan and logs the student as Absent. A2: If student has already marked attendance, system displays "Already marked" message |
| **Post-condition** | Attendance record saved with timestamp; visible to instructor in real time; reflected in reports |
| **Exception** | If QR code is invalid or unrecognized, system rejects the request and displays an error message |

### UC-02: Generate Session QR

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-02 |
| **Use Case Name** | Generate Session QR |
| **Actor(s)** | Instructor, Admin, System |
| **Pre-condition** | Instructor/Admin is authenticated; a scheduled class session exists in the system. |
| **Main Flow** | 1. Instructor selects the relevant course and session 2. Instructor clicks "Generate QR" 3. System creates a unique, time-stamped QR code linked to the session 4. QR code is displayed on screen for students to scan 5. System activates an expiry timer for the QR code |
| **Alternate Flow** | A1: If QR expires mid-session, instructor can regenerate a new code. A2: If no active session is found, system displays an error |
| **Post-condition** | Active QR code linked to the session is available for student scanning; becomes invalid after expiry or session ends |
| **Exception** | If system fails to generate QR due to a server error, instructor is notified and prompted to retry |

### UC-03: Generate Report

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-03 |
| **Use Case Name** | Generate Report |
| **Actor(s)** | Instructor, Admin, System |
| **Pre-condition** | User is authenticated with Instructor or Admin role; attendance records exist in the system. |
| **Main Flow** | 1. User navigates to the Reports section 2. User selects filter criteria (course, student, date range) 3. System retrieves matching attendance records 4. System displays a summarized report with present/absent counts and percentages 5. User optionally exports the report as PDF or CSV |
| **Alternate Flow** | A1: If no records match the selected filters, system displays "No records found". A2: If export fails, system shows an error message and prompts the user to retry |
| **Post-condition** | Report is displayed and/or downloaded successfully |
| **Exception** | If the system times out while fetching large datasets, user is notified and advised to narrow the filter range |

### UC-04: Manual Attendance Override

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-04 |
| **Use Case Name** | Manual Attendance Override |
| **Actor(s)** | Instructor, Admin, System |
| **Pre-condition** | Session has ended or is active; instructor has edit rights; target student is enrolled in the course. |
| **Main Flow** | 1. Instructor searches for the target student 2. Selects the relevant session record 3. Changes attendance status (Present / Absent / Late / Excused) 4. Provides a mandatory reason for the override 5. System validates the changes 6. System saves the updated record with an audit log entry |
| **Alternate Flow** | A1: If instructor lacks permissions, admin approval is required before the override is applied |
| **Post-condition** | Attendance record updated successfully; reason and audit log stored; reports updated automatically |
| **Exception** | Override after 48-hour lock requires admin approval to unlock and edit the record |

### UC-05: Manage Users

| Field | Detail |
|-------|--------|
| **Use Case ID** | UC-05 |
| **Use Case Name** | Manage Users |
| **Actor(s)** | Admin, System |
| **Pre-condition** | The user must have an Admin role. |
| **Main Flow** | 1. Admin navigates to User Management 2. Admin creates, edits, or deactivates a user account 3. System validates input (unique email, required fields) 4. System saves changes and updates access permissions |
| **Alternate Flow** | A1: If email already exists, system rejects the entry and highlights the conflict. A2: System can save locally if offline |
| **Post-condition** | User accounts are active/inactive as intended |
| **Exception** | If bulk import CSV contains invalid rows, system rejects those entries, reports errors per row, and imports the valid ones |
