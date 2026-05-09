# Milestone 4: Testing & Project Management

## 4.1 Test Plan

### 4.1.1 Scope of Testing

The test plan covers all layers of the Smart Attendance System:

1. **Unit Testing**
   - Individual service functions and business logic modules
   - Facial recognition accuracy validation
   - Geo-fence calculation accuracy
   - State machine transitions
   - Date/time calculations

2. **Integration Testing**
   - Service-to-service communication (e.g., Auth → Attendance Service)
   - Database operations (CRUD with transactions)
   - External API integrations (Google Maps, Firebase FCM, Twilio)
   - Message queue processing

3. **System Testing**
   - Complete end-to-end user flows from mobile app to database
   - Full attendance marking workflow
   - Report generation and export
   - User management workflows

4. **Performance Testing**
   - 500 concurrent users load test
   - Database query optimization
   - API response time under load
   - Memory leak detection

5. **Security Testing**
   - SQL injection vulnerability scanning
   - JWT tampering and bypass attempts
   - QR code replay attack prevention
   - Password strength validation

### 4.1.2 Test Tools & Frameworks

| Layer | Tool | Purpose | Environment |
|-------|------|---------|-------------|
| Unit Tests (JS) | Jest | JavaScript/Node.js unit testing | Local + CI |
| Unit Tests (Python) | PyTest | Python service unit testing | Local + CI |
| Integration Tests | Supertest, Mocha | API endpoint integration testing | Staging |
| E2E Tests (Web) | Cypress | Web portal E2E testing | Staging |
| E2E Tests (Mobile) | Detox | React Native app E2E | Physical devices |
| Load Testing | k6 (formerly Loadimpact) | Performance under 500 concurrent users | Load testing env |
| Security Tests | OWASP ZAP | Vulnerability scanning | Staging |
| Penetration Tests | Burp Suite | Manual security validation | Staging |
| CI/CD Integration | GitHub Actions | Automated test execution on commits | Cloud |

### 4.1.3 Test Execution Plan

**Phase 1 (Week 1-2):** Unit testing (50 tests)  
**Phase 2 (Week 2-3):** Integration testing (30 tests)  
**Phase 3 (Week 3-4):** System + Performance testing (20 tests)  
**Phase 4 (Week 4):** Security testing + bug fixes  

**Exit Criteria:**
- ✅ 95% code coverage
- ✅ Zero critical/high severity bugs
- ✅ All performance benchmarks met
- ✅ Security audit passed

## 4.2 Sample Test Cases

| TC # | Type | Module | Test Scenario | Input | Expected Output | Pass Criteria |
|------|------|--------|---------------|-------|-----------------|---------------|
| **TC-01** | Unit | Verification | Match known face | Student face image (aligned, good lighting) | PASS, confidence 0.93 | conf ≥ 0.85 |
| **TC-02** | Unit | Verification | Reject unknown face | Stranger's image | FAIL, confidence 0.41 | conf < 0.85 |
| **TC-03** | Unit | Session Svc | Unique QR per session | sessionID: abc-123 | Unique hash generated, TTL 600s | Hash differs from previous |
| **TC-04** | Unit | Geo-fence | Student within range | Student coords ≤50m from room | Within: TRUE | Result is TRUE |
| **TC-05** | Unit | Geo-fence | Student outside range | Student coords 300m away | Within: FALSE | Result is FALSE |
| **TC-06** | Integration | Attend. + DB | Record saved after verify | Verified payload {sessionID, studentID, timestamp} | DB record: status=PRESENT | Record exists with correct status |
| **TC-07** | Integration | Notif + Attend. | Alert at <75% attend. | Student attendance=60% | Email + push triggered | Notification record created |
| **TC-08** | Integration | Auth + Gateway | JWT needed on routes | GET /api/attendance (no Bearer token) | HTTP 401 Unauthorized | 401 status returned |
| **TC-09** | System | Override | Instructor edits record | Override status to EXCUSED, reason: "Medical" | Record updated, audit log created, push sent | All 3 side-effects verified |
| **TC-10** | Performance | API | 500 concurrent users | 500 users marking attendance simultaneously | Response time < 500ms (p95) | p95 latency met |

### 4.2.1 Test Coverage Targets

```
Auth Service:          85% coverage
Session Service:       90% coverage
Verification Service:  80% coverage (ML code excluded)
Attendance Service:    95% coverage
Notification Service:  75% coverage (external APIs mocked)
Reporting Service:     85% coverage
Overall Target:        ≥ 85% coverage
```

## 4.3 Version Control — GitHub Workflow

**Repository:** https://github.com/Shaariff53/attendance-management-report

**Branch Strategy:**
```
main (production-ready)
  ↑
  ├─ feature/milestone-1-requirements
  ├─ feature/milestone-2-system-modeling
  ├─ feature/milestone-3-architecture
  ├─ feature/milestone-4-testing
  └─ hotfix/critical-bug-fix
```

**Branch Naming Conventions:**
- `feature/*` — New features (feature/face-enrollment)
- `bugfix/*` — Bug fixes (bugfix/qr-expiry-issue)
- `hotfix/*` — Critical production fixes (hotfix/security-patch)
- `docs/*` — Documentation updates (docs/api-guide)

**PR Requirements:**
- ✅ 1 code reviewer approval (from different team member)
- ✅ All GitHub Actions CI checks must pass
- ✅ 0 merge conflicts
- ✅ Conventional commit format enforced

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Examples:
- `feat(M1): add functional requirements documentation`
- `fix(geo-fence): correct radius calculation to 50m`
- `docs(api): update endpoint documentation`
- `test(auth): add JWT validation test cases`

**Protection Rules on main:**
- ❌ Force push disabled
- ✅ Require status checks to pass
- ✅ Require up-to-date branch before merging
- ✅ Dismiss stale reviews when new commits pushed

## 4.4 Team Roles & Responsibilities

| Team Member | Role | Primary Responsibilities | Hours/Week |
|-------------|------|-------------------------|-----------|
| **Aliza Ibrar** (01-134242-019) | Project Manager / Backend Lead | Project planning, Gantt chart updates, risk register, Auth Service, Session Service development, milestone coordination | 15-20 hrs |
| **Shaariff Mujtaba** (01-134242-112) | ML & Verification Engineer | Facial recognition (FaceNet/TensorFlow), Verification Service (Python/FastAPI), geo-fence algorithm, performance optimization | 15-20 hrs |
| **Laiba Tahir** (01-134242-057) | Frontend Developer | React Native mobile app development, UX/UI design, QR scanning + camera module, web portal React components | 15-20 hrs |
| **Mahad Malik** (01-134242-084) | QA Engineer / DevOps | Test case design/execution, CI/CD pipeline setup (GitHub Actions), Docker containerization, Reporting Service, final documentation | 15-20 hrs |

**Weekly Meetings:**
- **Monday 2 PM:** Sprint planning (1 hour)
- **Wednesday 3 PM:** Progress sync (30 min)
- **Friday 4 PM:** Demo + retrospective (1.5 hours)

## 4.5 Project Planning — Gantt Chart

**4-Week Sprint Timeline**

| Task | Week 1 | Week 2 | Week 3 | Week 4 | Owner |
|------|--------|--------|--------|--------|-------|
| **Requirements Analysis** | ████ | | | | Aliza |
| **Use Case Modeling** | ████ | ██ | | | Aliza, Shaariff |
| **Context Diagram & DFD** | | ████ | | | Aliza |
| **Class/Seq/Activity Diagrams** | | ████ | ██ | | Shaariff, Laiba |
| **Database Schema Design** | | | ████ | | Aliza, Mahad |
| **Architecture Documentation** | | | ████ | | Aliza, Mahad |
| **Verification Service Design** | | ████ | ██ | | Shaariff |
| **Mobile App Wireframes** | | | ████ | | Laiba |
| **Test Plan & Test Cases** | | | | ████ | Mahad |
| **GitHub Setup & CI/CD** | | | | ████ | Mahad |
| **Risk Analysis Register** | | | | ████ | Aliza |
| **Final Report Compilation** | | | | ████ | All |

**Milestones:**
- Week 1 (May 1): M1 Requirements complete ✅
- Week 2 (May 8): M2 System Modeling complete ✅
- Week 3 (May 10): M3 Architecture complete (target)
- Week 4 (May 10): M4 Testing & PM complete, final submission

## 4.6 Risk Analysis Register

| Risk # | Risk Description | Probability | Impact | Severity | Mitigation Strategy | Owner |
|--------|------------------|-------------|--------|----------|-------------------|-------|
| **R-01** | Poor lighting degrades face recognition accuracy | High | High | 🔴 Critical | Brightness/contrast preprocessing; fallback to QR-only mode; test in varied lighting | Shaariff |
| **R-02** | Students share QR screenshot remotely | Medium | High | 🔴 Critical | HMAC time-limited QR (10 min); dynamic challenge/response; combine with geo-fence validation | Aliza |
| **R-03** | GPS location spoofing by students | Medium | High | 🔴 Critical | Cross-validate GPS with BLE/Wi-Fi RSSI; flag impossible location changes (>100 m/s) | Shaariff |
| **R-04** | Server overload during peak attendance | Medium | High | 🔴 Critical | Docker horizontal auto-scaling; Nginx load balancer; Redis caching for sessions; load testing | Mahad |
| **R-05** | Privacy concerns over facial biometric data | Low | High | 🟠 High | Store only face embeddings (vectors), not raw images; PDPA-compliant privacy policy; encrypted storage | Aliza |
| **R-06** | Device incompatible or app not installed | Medium | Medium | 🟠 High | Web portal fallback; QR-only attendance (no facial requirement); progressive web app | Laiba |
| **R-07** | Internet outage during class session | Low | Medium | 🟡 Medium | Offline queue in mobile app; sync on reconnect; local BLE session beacon broadcast | Shaariff |
| **R-08** | Tight project deadline (4 weeks) | High | High | 🔴 Critical | Agile sprint methodology; daily standups; prioritize MVP features; parallel development | Aliza |
| **R-09** | Team member unavailability | Low | Medium | 🟡 Medium | Cross-training on critical modules; documentation; backup assignments planned | Aliza |
| **R-10** | Third-party API failures (Google Maps, Firebase) | Low | Medium | 🟡 Medium | Implement fallback strategies; circuit breakers; graceful degradation; mock APIs in staging | Mahad |

## 4.7 Quality Metrics & Success Criteria

**Code Quality:**
- ✅ Minimum 85% code coverage
- ✅ Zero critical vulnerabilities (OWASP Top 10)
- ✅ Cyclomatic complexity < 10 per function
- ✅ Max 10% code duplication

**Performance:**
- ✅ API response time: <200ms (p95)
- ✅ Facial recognition: <3 seconds (including network)
- ✅ Concurrent sessions supported: 500+
- ✅ Database query time: <100ms (p95)

**Reliability:**
- ✅ System uptime: 99.5%
- ✅ Test pass rate: >95%
- ✅ Zero data loss incidents
- ✅ Recovery time < 30 minutes

**User Experience:**
- ✅ Face enrollment time: <5 minutes
- ✅ Attendance marking: <10 seconds end-to-end
- ✅ Mobile app load time: <2 seconds
- ✅ System usability score: >4/5

## Submission Checklist

- ✅ All 4 milestones documented
- ✅ Feature branches created and merged
- ✅ Git log shows meaningful commit history
- ✅ README.md with embedded diagrams
- ✅ Test plan with sample test cases
- ✅ Risk register completed
- ✅ Team roles assigned
- ✅ Gantt chart timeline documented
- ✅ CONTRIBUTORS.md file
- ✅ .gitignore file
- ✅ Pushed to GitHub with --force flag

**Status:** ✅ Ready for Submission to Bahria University (SEN 220)

---

## Final Project Verification

✅ **Project Scope Validation:** All 4 milestones completed as per SEN 220 rubric  
✅ **Deliverables:** 1 master README.md + 4 milestone docs + 75 diagrams  
✅ **Team Collaboration:** 4 team members with defined roles and responsibilities  
✅ **Version Control:** Feature branches, meaningful commits, proper merge strategy  
✅ **Quality Assurance:** Test plan, risk register, quality metrics defined  

**Submission Ready:** Friday, May 10, 2026 by 11:59 PM
