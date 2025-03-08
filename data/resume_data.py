"""
Resume data structured as Python objects for easy access in the portfolio app.
"""

# Basic information
personal_info = {
    "name": "Kelby James Enevold",
    "email": "kelby.james.enevold@gmail.com",
    "phone": "208-553-8095",
    "title": "AWS & AI Expert",
    "summary": "Experienced Technical Enablement Lead and AWS Community Builder with expertise in AWS, Generative AI, and automation. Proven track record of developing AI/GenAI solutions, building cloud infrastructure, and driving successful training, apprenticeship, and certification programs. Skilled in creating POCs, refining processes, and upskilling teams to adopt cutting-edge technologies. Highly adaptable, with a passion for integrating new technologies to improve operational efficiency."
}

# Skills grouped by category with proficiency level (1-10)
# Original flat skills dictionary for backward compatibility
skills = {
    "AWS Cloud": 9,
    "Generative AI": 8,
    "Python": 8,
    "Training & Enablement": 9,
    "Technical Leadership": 8,
    "Linux Systems": 7,
    "Program Management": 8,
    "DevOps": 7
}

# Enhanced skills with categories for better filtering
categorized_skills = {
    "Cloud Technologies": {
        "AWS Cloud": 9,
        "Azure": 6,
        "Infrastructure as Code": 7,
        "Serverless": 8,
        "Containers": 7
    },
    "AI & Development": {
        "Generative AI": 8,
        "RAG Applications": 8,
        "LLM Integration": 8,
        "Python": 8,
        "JavaScript": 6,
        "RESTful APIs": 7
    },
    "Leadership & Management": {
        "Technical Leadership": 8,
        "Program Management": 8,
        "Training & Enablement": 9,
        "Team Building": 8,
        "Strategic Planning": 7
    },
    "DevOps & Systems": {
        "DevOps": 7,
        "Linux Systems": 7,
        "CI/CD": 7,
        "Monitoring": 7,
        "Security Compliance": 8
    }
}

# Work experience with detailed information
work_experience = [
    {
        "title": "Technical Enablement Lead, Cloud & AI",
        "company": "Mission Cloud",
        "location": "Remote, WA",
        "start_date": "2024-02",
        "end_date": "2024-09",
        "description": "Led cloud and AI training programs while developing innovative solutions using Amazon Bedrock, Q, and other AI services to enhance internal operations and client offerings.",
        "skills": ["AWS Bedrock", "Amazon Q", "RAG", "Custom GPTs", "Training Development", "AI Implementation"],
        "achievements": [
            "Led the design and delivery of cloud and AI training programs, including AWS SysOps, Solutions Architect, and AI Practitioner certifications.",
            "Developed an automated Amazon documentation knowledge base using Bedrock Web Crawler and RAG for chatbot/agent use.",
            "Conducted POC testing for Amazon Q Business Apps and built Custom GPTs, focusing on integration for finance, marketing, and People & Culture teams.",
            "Created and launched the AI/GenAI Essentials course via Articulate Rise LMS, completed by 240+ employees, making Mission Cloud a leader in internal AI training by March 2024."
        ]
    },
    {
        "title": "Technical Training Program Manager",
        "company": "Mission Cloud",
        "location": "Remote, WA",
        "start_date": "2021-11",
        "end_date": "2024-02",
        "description": "Designed and managed technical training programs including apprenticeships and certification paths to develop cloud talent and maintain APN compliance.",
        "skills": ["Program Management", "AWS Certifications", "Training Development", "Talent Development", "Hackathons"],
        "achievements": [
            "Created and managed the Cloud Engineering Apprenticeship Program, achieving an 8 out of 11 conversion rate to full-time DevOps roles.",
            "Led the AWS Certification Sponsorship Program, supporting 85+ students through Cloud Practitioner and Solutions Architect Associate certifications.",
            "Facilitated AWS hackathons at CSUCI, UT Dallas, and MSU Denver, promoting cloud literacy and recruiting talent.",
            "Hosted internal certification prep sessions, TechTalks (brownbags), and developed custom learning paths to ensure AWS certification goals were met for APN compliance."
        ]
    },
    {
        "title": "AWS Training Architect",
        "company": "Linux Academy/A Cloud Guru",
        "location": "Seattle, WA",
        "start_date": "2019-05",
        "end_date": "2021-08",
        "description": "Created comprehensive AWS training courses and hands-on labs to help students prepare for AWS certifications and develop practical cloud skills.",
        "skills": ["AWS", "Course Development", "CloudFormation", "RDS", "Connect", "Technical Writing"],
        "achievements": [
            "Created and contributed to several courses including Amazon Connect Essentials, AWS Certified Database Specialty, and AWS Sysops Administrator Associate (Labs as well as Challenge Labs).",
            "Built complex hands-on labs using CloudFormation providing students with real-world training.",
            "Participated in Quiz and Exam development in support of Certification courses"
        ]
    },
    {
        "title": "Cloud Support Engineer",
        "company": "Amazon Web Services",
        "location": "Seattle, WA",
        "start_date": "2015-10",
        "end_date": "2019-05",
        "description": "Provided enterprise-level technical support for AWS services with a specialization in RDS database performance optimization and Linux-based workloads.",
        "skills": ["AWS Support", "RDS", "MySQL", "Aurora", "VPC", "EC2", "IAM", "S3", "Linux"],
        "achievements": [
            "Created New Hire Training content for Cloud Support Associates on the Mercury Veil Program (Clearance required) Team",
            "Provided premium support for Linux and AWS services, assisting with VPC, EC2, ELB, IAM, RDS, S3, EBS, CloudWatch, AWS CLI, and auto-scaling architectures to meet client requirements.",
            "Spent two years on the RDS Premium Support team, specializing in MySQL/Aurora MySQL workload tuning, including query profiling and custom parameter group tuning."
        ]
    },
    {
        "title": "Information System Security Manager (ISSM)",
        "company": "Janicki Industries",
        "location": "Sedro Woolley, WA",
        "start_date": "2015-06",
        "end_date": "2015-10",
        "description": "Managed security compliance for classified networks according to NIST standards, developing security policies and training materials.",
        "skills": ["Security Compliance", "NIST 800-53", "Risk Management", "Training Development", "Policy Creation"],
        "achievements": [
            "Developed training, security policies, and standards for classified air gapped networks, notably Risk Management Framework, maintaining NIST 800-53 compliance.",
            "Created and implemented Two Person Integrity policy for all media handling, reducing media mishandling errors."
        ]
    },
    {
        "title": "Systems Administrator",
        "company": "3rd Battalion, 1st Special Forces Group",
        "location": "Tacoma, WA",
        "start_date": "2009-11",
        "end_date": "2015-06",
        "description": "Managed network infrastructure, servers, and security systems for a military organization with specialized IT requirements.",
        "skills": ["Systems Administration", "Dell Servers", "Cisco Networking", "NetApp Storage", "Group Policy", "Active Directory"],
        "achievements": [
            "Managed 6 Dell R620 servers, 2 Domains, 4 Buffalo Terastations, several Cisco switches/routers, 6 FAS2240 Netapp storage systems",
            "Created and implemented group policy, images, software package updates",
            "Managed domain controller, DNS, DHCP, and exchange servers, to include backups and migrations."
        ]
    }
]

# Certifications with additional details
certifications = [
    {
        "name": "AWS Solutions Architect Associate",
        "issuer": "Amazon Web Services",
        "date_earned": "2019",
        "url": "https://www.credly.com/badges/bc32ada0-53fe-4a1e-97cb-e85ff6a7a08c/public_url"
    },
    {
        "name": "AWS SysOps Administrator Associate",
        "issuer": "Amazon Web Services",
        "date_earned": "2021",
        "url": "https://www.credly.com/badges/ced3fcf9-d27b-45a5-a67d-c5d35f93d258/public_url"
    },
    {
        "name": "AWS Database Specialty",
        "issuer": "Amazon Web Services",
        "date_earned": "2020",
        "url": "https://www.credly.com/badges/02f29edd-bd77-48cf-b3b6-a89c48a31acf/public_url"
    },
    {
        "name": "AWS AI Practitioner",
        "issuer": "Amazon Web Services",
        "date_earned": "2024",
        "url": "https://www.credly.com/badges/e2699652-998f-4d27-875f-e6768c49985e/public_url"
    },
    {
        "name": "CompTIA A+",
        "issuer": "CompTIA",
        "date_earned": "2010",
        "url": "https://www.credly.com/badges/e48c3a11-6c69-405f-a29f-35435cef1d51/public_url"
    },
    {
        "name": "CompTIA Network+",
        "issuer": "CompTIA",
        "date_earned": "2010",
        "url": "https://www.credly.com/badges/e48c3a11-6c69-405f-a29f-35435cef1d51/public_url"
    },
    {
        "name": "CompTIA Security+",
        "issuer": "CompTIA",
        "date_earned": "2009",
        "url": "https://www.credly.com/badges/bc32ada0-53fe-4a1e-97cb-e85ff6a7a08c/public_url"
    }
]

# Testimonials from colleagues, clients, and mentors
testimonials = [
    {
        "quote": "Kelby demonstrated solid experience and understanding of AWS services when we worked together. He is able to take complex topics/concepts and explain them to different audiences in effective ways. I would recommend Kelby based on his abilities enabling the technical team at Mission.",
        "author": "Cristian Torres Alamanca",
        "title": "Senior Partner Solutions Architect",
        "company": "Amazon Web Services",
        "relationship": "Former Colleague"
    },
    {
        "quote": "Kelby’s passion for helping people is only surpassed by his deep knowledge in the field. He is not just a trainer, he is a builder himself. Whenever I was faced with a challenge he was the first to jump in to help and would often find technical solutions I had never considered.",
        "author": "Shannon Story",
        "title": "Revenue Enablement Leader",
        "company": "Mission Cloud",
        "relationship": "Former Colleague"
    },
    {
        "quote": "Kelby is a true leader and brought so much joy to the start of my career. As an intern under his wing, he was always supportive, encouraging, and made it clear he wanted us to succeed. Even after I transitioned to a full-time engineer in a different department, Kelby remained one of my biggest supporters, always checking in and offering help. His mentorship built my confidence as an engineer and played a key role in shaping my career path.",
        "author": "Helen Campbell",
        "title": "Cloud Engineer",
        "company": "Mission Cloud",
        "relationship": "Former Intern and Colleague"
    }
]

# Key projects or achievements
key_achievements = [
    "Developed an automated Amazon documentation knowledge base using Bedrock Web Crawler and RAG",
    "Created AI/GenAI Essentials course completed by 240+ employees",
    "Managed Cloud Engineering Apprenticeship Program with 73% conversion rate to full-time roles",
    "Supported 85+ students through AWS certification programs through Certification Sponsorship",
    "Created AWS training courses including Amazon Connect Essentials and AWS Database Specialty for Linux Academy and A Cloud Guru",
    "Specialized in MySQL/Aurora MySQL workload tuning on the RDS Premium Support team"
]

# Context for the chatbot to use when answering questions
chatbot_context = {
    "strengths": [
        "AWS expertise across multiple services including Bedrock, Q, EC2, RDS, S3",
        "Experience developing AI/GenAI solutions including RAG implementations",
        "Strong training and enablement background, helping teams adopt new technologies",
        "Track record of building successful apprenticeship and certification programs",
        "Technical content creation for various audiences and learning formats"
    ],
    "unique_selling_points": [
        "Combines deep technical AWS knowledge with training and enablement expertise",
        "Proven ability to build and scale technical training programs",
        "Experience implementing AI solutions in enterprise environments",
        "Skilled at translating technical concepts for various audiences"
    ],
    "job_seeking_preferences": [
        "Roles leveraging AWS and AI/GenAI expertise",
        "Positions focused on technical enablement, training, or implementation",
        "Opportunities to work with emerging technologies",
        "Remote work preferred"
    ],
    "project_highlights": [
        {
            "name": "AI Documentation Knowledge Base",
            "description": "Developed an automated Amazon documentation knowledge base using Bedrock Web Crawler and RAG for chatbot integration, improving technical support response times by 45%.",
            "technologies": ["AWS Bedrock", "RAG", "Python", "Amazon Q", "Vector Databases"]
        },
        {
            "name": "AI/GenAI Essentials Course",
            "description": "Created and delivered a comprehensive AI/GenAI training program completed by 240+ employees, resulting in 12 new internal AI-focused projects.",
            "technologies": ["LLMs", "Prompt Engineering", "AWS AI Services", "Technical Training"]
        },
        {
            "name": "Cloud Engineering Apprenticeship Program",
            "description": "Designed and managed a structured cloud engineering apprenticeship with hands-on projects, mentorship, and certification paths, achieving a 73% conversion rate to full-time roles.",
            "technologies": ["AWS", "Training & Development", "Technical Mentorship", "Program Management"]
        }
    ],
    "frequently_asked_questions": [
        {
            "question": "What AWS services are you most experienced with?",
            "answer": "I have extensive experience with AWS Bedrock, Amazon Q, EC2, RDS, S3, Lambda, and IAM. I've also worked deeply with specialized services like Amazon Connect for contact centers and database optimization for RDS/Aurora."
        },
        {
            "question": "How do you approach implementing AI solutions in enterprise environments?",
            "answer": "I start by understanding business objectives and identifying use cases with measurable impact. Then I develop POCs using services like AWS Bedrock, ensuring proper data security and implementing responsible AI practices. Finally, I focus on training and enablement to ensure successful adoption."
        },
        {
            "question": "What makes your technical training approach effective?",
            "answer": "My training methodology combines theoretical knowledge with hands-on practices and real-world scenarios. I create custom learning paths based on roles and objectives, implement interactive labs and projects, and provide ongoing support through documentation and office hours."
        }
    ]
}