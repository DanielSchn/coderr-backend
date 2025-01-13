# example_data.py

EXAMPLE_BUSINESS_USERS = [
    {
        'username': 'developer_max',
        'file': '/profile_pictures/max.jpg',
        'password': 'password123',
        'first_name': 'Max',
        'last_name': 'Müller',
        'location': 'Berlin',
        'tel': '0301234567',
        'description': 'Ich bin ein erfahrener Softwareentwickler und spezialisiere mich auf Backend-Systeme.',
        'working_hours': '9-17 Uhr',
        'email': 'max.developer@example.com'
    },
    {
        'username': 'webdesigner_lisa',
        'file': '/profile_pictures/lisa.jpg',
        'password': 'password123',
        'first_name': 'Lisa',
        'last_name': 'Schmidt',
        'location': 'Hamburg',
        'tel': '0407654321',
        'description': 'Ich bin eine kreative Webdesignerin mit einem Auge für Ästhetik und UX.',
        'working_hours': '10-18 Uhr',
        'email': 'lisa.designer@example.com'
    },
    {
        'username': 'kevin',
        'file': '/profile_pictures/kevin.jpg',
        'password': 'asdasd',
        'first_name': 'Kevin',
        'last_name': 'Businessguest',
        'location': 'Testlocation',
        'tel': '000000',
        'description': 'Ich bin ein Testbusinessaccount.',
        'working_hours': '9-17 Uhr',
        'email': 'kevin@business.de'
    }
]

EXAMPLE_CUSTOMERS = [
    {
        'username': 'hannah_meyer',
        'file': '/profile_pictures/hannah.jpg',
        'password': 'password123',
        'first_name': 'Hannah',
        'last_name': 'Meyer',
        'location': 'Frankfurt',
        'tel': '0699876543',
        'description': 'Ich benötige Unterstützung für ein Softwareentwicklungsprojekt.',
        'email': 'hannah.meyer@example.com'
    },
    {
        'username': 'tom_schneider',
        'file': '/profile_pictures/tom.jpg',
        'password': 'password123',
        'first_name': 'Tom',
        'last_name': 'Schneider',
        'location': 'München',
        'tel': '0898765432',
        'description': 'Ich suche nach modernem Webdesign für mein Unternehmen.',
        'email': 'tom.schneider@example.com'
    },
    {
        'username': 'sophia_bauer',
        'file': '/profile_pictures/sophia.jpg',
        'password': 'password123',
        'first_name': 'Sophia',
        'last_name': 'Bauer',
        'location': 'Köln',
        'tel': '0221123456',
        'description': 'Ich habe ein kleines Projekt und brauche Unterstützung in Softwareentwicklung.',
        'email': 'sophia.bauer@example.com'
    },
    {
        'username': 'lukas_weber',
        'file': '/profile_pictures/lukas.jpg',
        'password': 'password123',
        'first_name': 'Lukas',
        'last_name': 'Weber',
        'location': 'Stuttgart',
        'tel': '0711123456',
        'description': 'Ich möchte eine Webseite für mein Startup erstellen lassen.',
        'email': 'lukas.weber@example.com'
    },
    {
        'username': 'andrey',
        'file': '/profile_pictures/andrey.jpg',
        'password': 'asdasd',
        'first_name': 'Andrey',
        'last_name': 'Customerguest',
        'location': 'Testlocation',
        'tel': '0000',
        'description': 'Ich bin ein Testcustomeraccout.',
        'email': 'andrey@customer.de'
    },
]


EXAMPLE_OFFERS = {
    'developer_max': [
        {
            'title': 'API-Entwicklung',
            'image': '/offers/api.jpg',
            'description': 'Entwicklung von robusten und skalierbaren APIs.',
            'details': [
                {'offer_type': 'basic', 'price': 500, 'revisions': 2, 'delivery_time_in_days': 7, 'features': [
                    'API-Dokumentation', 'Initiales Setup']},
                {'offer_type': 'standard', 'price': 1000, 'revisions': 5, 'delivery_time_in_days': 14, 'features': [
                    'API-Dokumentation', 'Initiales Setup', 'Sicherheitsfeatures']},
                {'offer_type': 'premium', 'price': 2000, 'revisions': -1, 'delivery_time_in_days': 30,
                 'features': ['API-Dokumentation', 'Initiales Setup', 'Sicherheitsfeatures', 'Skalierbarkeit']},
            ]
        },
        {
            'title': 'Datenbankdesign',
            'image': '/offers/datenbank.jpg',
            'description': 'Erstellung eines optimierten und sicheren Datenbankdesigns.',
            'details': [
                {'offer_type': 'basic', 'price': 600, 'revisions': 2,
                 'delivery_time_in_days': 10, 'features': ['Normalisierung', 'Datenmodell']},
                {'offer_type': 'standard', 'price': 1200, 'revisions': 5, 'delivery_time_in_days': 20, 'features': [
                    'Normalisierung', 'Datenmodell', 'Backup-Strategie']},
                {'offer_type': 'premium', 'price': 2500, 'revisions': -1, 'delivery_time_in_days': 30,
                 'features': ['Normalisierung', 'Datenmodell', 'Backup-Strategie', 'Optimierung für Performance']},
            ]
        },
        {
            'title': 'Backend-Entwicklung',
            'image': '/offers/backend.jpg',
            'description': 'Erstellung von performanten und skalierbaren Backendsystemen.',
            'details': [
                {'offer_type': 'basic', 'price': 700, 'revisions': 1, 'delivery_time_in_days': 10, 'features': [
                    'Grundlegende APIs', 'Datenbankintegration']},
                {'offer_type': 'standard', 'price': 1500, 'revisions': 3, 'delivery_time_in_days': 20, 'features': [
                    'Grundlegende APIs', 'Datenbankintegration', 'Caching-Strategie']},
                {'offer_type': 'premium', 'price': 3000, 'revisions': -1, 'delivery_time_in_days': 40, 'features': [
                    'Grundlegende APIs', 'Datenbankintegration', 'Caching-Strategie', 'Lastenverteilung']},
            ]
        },
        {
            'title': 'DevOps-Beratung & Implementierung',
            'image': '/offers/dev-ops.jpg',
            'description': 'Einführung von DevOps-Praktiken für effizientere Softwareentwicklung und -bereitstellung.',
            'details': [
                {'offer_type': 'basic', 'price': 700, 'revisions': 2, 'delivery_time_in_days': 10,
                 'features': ['CI/CD Pipeline-Setup', 'Tool-Auswahl']},
                {'offer_type': 'standard', 'price': 1400, 'revisions': 4, 'delivery_time_in_days': 20,
                 'features': ['CI/CD Pipeline-Setup', 'Tool-Auswahl', 'Automatisierung']},
                {'offer_type': 'premium', 'price': 2800, 'revisions': -1, 'delivery_time_in_days': 30,
                 'features': ['CI/CD Pipeline-Setup', 'Tool-Auswahl', 'Automatisierung', 'Monitoring']},
            ]
        },
        {
            'title': 'Cloud-Migration & -Optimierung',
            'image': '/offers/cloud.jpg',
            'description': 'Nahtlose Migration Ihrer Anwendungen in die Cloud und Optimierung für maximale Leistung.',
            'details': [
                {'offer_type': 'basic', 'price': 800, 'revisions': 2, 'delivery_time_in_days': 10,
                 'features': ['AWS/Azure/GCP Migration', 'Performance-Überprüfung']},
                {'offer_type': 'standard', 'price': 1500, 'revisions': 4, 'delivery_time_in_days': 20,
                 'features': ['AWS/Azure/GCP Migration', 'Performance-Überprüfung', 'Kostenoptimierung']},
                {'offer_type': 'premium', 'price': 3000, 'revisions': -1, 'delivery_time_in_days': 30,
                 'features': ['AWS/Azure/GCP Migration', 'Performance-Überprüfung', 'Kostenoptimierung', 'Sicherheitsaudit']}
            ]
        }
    ],
    'webdesigner_lisa': [
        {
            'title': 'Responsive Webdesign',
            'image': '/offers/responsive.jpg',
            'description': 'Gestaltung von ansprechenden und responsiven Webseiten.',
            'details': [
                {'offer_type': 'basic', 'price': 400, 'revisions': 1, 'delivery_time_in_days': 5, 'features': [
                    'Design für Mobilgeräte', 'Einfache Navigation']},
                {'offer_type': 'standard', 'price': 800, 'revisions': 3, 'delivery_time_in_days': 10, 'features': [
                    'Design für Mobilgeräte', 'Einfache Navigation', 'SEO-Optimierung']},
                {'offer_type': 'premium', 'price': 1600, 'revisions': -1, 'delivery_time_in_days': 15, 'features': [
                    'Design für Mobilgeräte', 'Einfache Navigation', 'SEO-Optimierung', 'Optimierung der Ladegeschwindigkeit']},
            ]
        },
        {
            'title': 'Landing Page Design',
            'image': '/offers/landing.jpg',
            'description': 'Erstellung einer modernen und ansprechenden Landing Page.',
            'details': [
                {'offer_type': 'basic', 'price': 300, 'revisions': 2, 'delivery_time_in_days': 4, 'features': [
                    'Designvorlage', 'Einfache Struktur']},
                {'offer_type': 'standard', 'price': 700, 'revisions': 3, 'delivery_time_in_days': 7, 'features': [
                    'Designvorlage', 'Einfache Struktur', 'CTA-Buttons']},
                {'offer_type': 'premium', 'price': 1300, 'revisions': -1, 'delivery_time_in_days': 12,
                 'features': ['Designvorlage', 'Einfache Struktur', 'CTA-Buttons', 'SEO-Optimierung']},
            ]
        },
        {
            'title': 'UX/UI Audit',
            'image': '/offers/ux-ui.jpg',
            'description': 'Detaillierte Analyse und Optimierung Ihrer Website in Bezug auf UX/UI.',
            'details': [
                {'offer_type': 'basic', 'price': 500, 'revisions': 1, 'delivery_time_in_days': 5, 'features': [
                    'Usability-Tests', 'Visuelle Optimierung']},
                {'offer_type': 'standard', 'price': 1000, 'revisions': 2, 'delivery_time_in_days': 10, 'features': [
                    'Usability-Tests', 'Visuelle Optimierung', 'Benutzerfeedback']},
                {'offer_type': 'premium', 'price': 2000, 'revisions': -1, 'delivery_time_in_days': 20, 'features': [
                    'Usability-Tests', 'Visuelle Optimierung', 'Benutzerfeedback', 'Erweiterte A/B-Tests']},
            ]
        },
        {
            'title': 'Mobile App UI/UX Design',
            'image': '/offers/app.jpg',
            'description': 'Erstellung von intuitiven und ansprechenden Designs für Ihre mobile App.',
            'details': [
                {'offer_type': 'basic', 'price': 600, 'revisions': 2,
                 'delivery_time_in_days': 8, 'features': ['Wireframes', 'Styleguide']},
                {'offer_type': 'standard', 'price': 1200, 'revisions': 4,
                 'delivery_time_in_days': 15, 'features': ['Wireframes', 'Styleguide', 'Prototyp']},
                {'offer_type': 'premium', 'price': 2400, 'revisions': -1, 'delivery_time_in_days': 30,
                 'features': ['Wireframes', 'Styleguide', 'Prototyp', 'Usability-Tests']}
            ]
        }
    ],
}
