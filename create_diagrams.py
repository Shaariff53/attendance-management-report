#!/usr/bin/env python3
"""
Create placeholder diagram images with descriptive text
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_diagram_image(filename, title, description):
    """Create a placeholder diagram image"""
    # Create image with white background
    width, height = 1000, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add border
    draw.rectangle([(10, 10), (width-10, height-10)], outline='#333333', width=3)
    
    # Add title
    title_color = '#0066cc'
    draw.text((50, 50), title, fill=title_color)
    
    # Add description
    desc_color = '#666666'
    desc_y = 150
    for line in description.split('\n'):
        draw.text((50, desc_y), line, fill=desc_color)
        desc_y += 40
    
    # Add footer
    footer_text = f"[See {filename} in PDF report for full diagram]"
    draw.text((50, height-80), footer_text, fill='#999999')
    
    # Save image
    img.save(f'images/{filename}')
    print(f"✓ Created {filename}")

# Create diagrams
diagrams = {
    'context-diagram.png': 'Context Diagram (Level 0 DFD)', 
    'context-diagram.png': ['Context Diagram - Level 0 DFD',
                            'Entities: Students, Instructors, Admin',
                            'External Systems: LMS, Maps, Face API, FCM',
                            'Shows system boundary and external interactions'],
    
    'level1-dfd.png': 'Level 1 DFD - Major Processes',
    'level1-dfd.png': ['Level 1 Data Flow Diagram',
                       'P1: Authentication & Authorization',
                       'P2: Session Management',
                       'P3: Verification Engine',
                       'P4: Attendance Recording',
                       'P5: Reporting & Analytics'],
    
    'class-diagram.png': 'Class Diagram - Object Design',
    'class-diagram.png': ['UML Class Diagram',
                          'Base Classes: User, Course, Session',
                          'Entities: Student, Instructor, Admin',
                          'Models: AttendanceRecord, AuditLog',
                          'Relationships and inheritance structure'],
    
    'sequence-diagram.png': 'Sequence Diagram - Facial Recognition Flow',
    'sequence-diagram.png': ['Sequence Diagram: Mark Attendance',
                             'Actors: Student App, Session Service, Verification',
                             'Process: Face capture → Verification → Recording',
                             'Steps: Image send → ML matching → DB store'],
    
    'activity-diagram.png': 'Activity Diagram - Student Attendance Flow',
    'activity-diagram.png': ['Activity Diagram: Student Attendance',
                             'Start → Scan QR → Verify face → Check geo-fence',
                             'Decision points: QR valid? Face match? Location?',
                             'End: Success or Error message'],
    
    'state-diagram-attendance.png': 'State Diagram - AttendanceRecord Lifecycle',
    'state-diagram-attendance.png': ['State Machine: Attendance Record States',
                                      'States: NOT_MARKED → MARKED → LATE/ABSENT',
                                      'Transitions: EXCUSED, CORRECTED, LOCKED',
                                      '48-hour immutable lock after session close'],
    
    'architecture-diagram.png': 'System Architecture - Layered MVC + Microservices',
    'architecture-diagram.png': ['Layered Architecture Diagram',
                                 'Layers: Presentation → Controller → Business Logic',
                                 'Services: Auth, Session, Verification, Attendance',
                                 'Data: PostgreSQL, Redis, MongoDB'],
    
    'state-machine-session.png': 'State Machine - Session Lifecycle',
    'state-machine-session.png': ['State Machine: Session States',
                                   'SCHEDULED → ACTIVE → GRACE_PERIOD → CLOSED',
                                   'Can transition to CORRECTION or FINALIZED',
                                   'Terminal state: CANCELLED'],
    
    'gantt-chart.png': 'Gantt Chart - 4-Week Project Timeline',
    'gantt-chart.png': ['Project Gantt Chart (4 weeks)',
                        'Week 1: Requirements Analysis',
                        'Week 2: System Modeling',
                        'Week 3: Architecture Design',
                        'Week 4: Testing & Documentation'],
}

# Create all diagrams
try:
    for filename, (title, desc_lines) in [
        ('context-diagram.png', ('Context Diagram (Level 0 DFD)', 
                                 ['Entities: Students, Instructors, Admin',
                                  'External Systems: LMS, Maps, Face API, FCM',
                                  'Shows system boundary and data flows'])),
        ('level1-dfd.png', ('Level 1 DFD - Major Processes',
                           ['P1: Authentication & Authorization',
                            'P2: Session Management',
                            'P3: Verification Engine',
                            'P4: Attendance Recording',
                            'P5: Reporting & Analytics'])),
        ('class-diagram.png', ('Class Diagram - Object Design',
                              ['User, Course, Session base classes',
                               'Student, Instructor, Admin entities',
                               'AttendanceRecord and AuditLog models',
                               'Full inheritance and relationships shown'])),
        ('sequence-diagram.png', ('Sequence Diagram - Facial Recognition Flow',
                                 ['Student App → Session Service → Verification',
                                  'Face image capture and ML matching',
                                  'GPS geo-fence validation',
                                  'Database recording with timestamp'])),
        ('activity-diagram.png', ('Activity Diagram - Student Attendance',
                                 ['Start → Open App → Scan QR → Capture Face',
                                  'Verification checks: QR valid? Match? Location?',
                                  'Success: Record attendance and notify student',
                                  'Failure paths with appropriate error messages'])),
        ('state-diagram-attendance.png', ('State Diagram - AttendanceRecord Lifecycle',
                                         ['NOT_MARKED → MARKED → LATE/ABSENT/EXCUSED',
                                          'CORRECTED (with manual override)',
                                          'LOCKED after 48 hours (immutable)',
                                          'Audit trail on all state transitions'])),
        ('architecture-diagram.png', ('System Architecture - Layered Design',
                                     ['Presentation: React Native + React.js',
                                      'Controller: REST API (Express.js)',
                                      'Services: Auth, Session, Verification, Attendance',
                                      'Data: PostgreSQL, Redis cache, MongoDB logs'])),
        ('state-machine-session.png', ('State Machine - Session Lifecycle',
                                      ['SCHEDULED → ACTIVE → GRACE_PERIOD → CLOSED',
                                       'CORRECTION window for 24 hours after close',
                                       'Can transition to FINALIZED or CANCELLED',
                                       'Full state transition diagram with conditions'])),
        ('gantt-chart.png', ('Gantt Chart - 4-Week Sprint Timeline',
                            ['Week 1: Requirements & Use Cases (M1)',
                             'Week 2: System Modeling & Diagrams (M2)',
                             'Week 3: Architecture & Design (M3)',
                             'Week 4: Testing & Project Management (M4)'])),
    ]:
        create_diagram_image(filename, title, '\n'.join(desc_lines))
    
    print("\n✅ All placeholder images created successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
