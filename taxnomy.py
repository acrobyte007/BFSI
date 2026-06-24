import sqlite3

DB_NAME = "bfsi.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver TEXT,
    sub_driver TEXT,
    description TEXT
)
""")

data = [
    ("Brand Perception", "Thought Leadership", "CXO/expert commentary, market outlook, industry viewpoints. Examples: Fund manager view on rate cuts, CIO interview, market op-ed."),
    ("Brand Perception", "Product Strategy", "Product launches, positioning, pricing, offers. Examples: New NFO launch, revised expense ratio, new SIP plan, festive offer."),
    ("Brand Perception", "Brand Visibility & Marketing", "Campaigns, sponsorships, ambassadors, awareness initiatives. Examples: Ad campaign, cricket sponsorship, brand ambassador announcement, investor awareness event"),

    ("User Experience", "Product & Service Quality", "Product performance, reliability, quality. Examples: Fund returns, scheme vs benchmark performance, praised or criticised feature."),
    ("User Experience", "Customer Support & Complaint Resolution", "Responsiveness, issue resolution, complaints handling. Examples: Delayed redemption, slow KYC process, unresponsive helpline, quick complaint resolution."),
    ("User Experience", "Digital & Omnichannel Experience", "App, website, digital journey experience. Examples: App crash, login issue, website downtime, confusing transaction screen."),

    ("Responsible Business Practices", "Regulatory Compliance & Ethical Governance", "Governance, regulatory actions, compliance issues, ethics. Examples: SEBI penalty, disclosure lapse, mis-selling allegation, transparency initiatives."),
    ("Responsible Business Practices", "Social Impact & Community (CSR)", "CSR activities, social initiatives, financial literacy programs, donations, rural outreach initiatives.")
]

cursor.executemany("""
INSERT INTO taxonomy (driver, sub_driver, description)
VALUES (?, ?, ?)
""", data)

conn.commit()
conn.close()

print("Taxonomy table created and data inserted successfully.")