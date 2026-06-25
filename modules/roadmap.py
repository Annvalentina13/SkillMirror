"""
SkillMirror — Smart Roadmap Generator
Module 5 of 5 — Phase 3 (Rule-based, no API needed)
"""

import json

# ── Roadmap Database ──────────────────────────────────────────────────────────
# Hand-curated roadmaps for every skill we track
# Real URLs, real resources, real projects

ROADMAP_DB = {
    "Git": {
        "why_it_matters": "Git is the #1 tool every tech company uses for version control. Without it, you can't collaborate on code, contribute to open source, or even apply to most jobs.",
        "time_estimate": "1 week",
        "difficulty": "Beginner",
        "free_resources": [
            {"name": "Pro Git Book (free)", "url": "https://git-scm.com/book/en/v2", "type": "Book"},
            {"name": "Git & GitHub Crash Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "type": "Video"},
            {"name": "Learn Git Branching (interactive)", "url": "https://learngitbranching.js.org", "type": "Interactive"},
            {"name": "GitHub Skills", "url": "https://skills.github.com", "type": "Course"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Git basics — init, add, commit, push, pull, clone", "goal": "Push your first project to GitHub"},
            {"week": 2, "focus": "Branching, merging, pull requests, resolving conflicts", "goal": "Collaborate on a repo with a friend"},
        ],
        "project_to_build": {
            "name": "Your GitHub Portfolio",
            "description": "Push all your existing projects to GitHub with proper READMEs",
            "why": "Employers check GitHub before interviews — a filled profile beats a blank one every time"
        },
        "tips": [
            "Commit every day, even small changes — builds habit and fills your contribution graph",
            "Write meaningful commit messages — 'fixed bug' is bad, 'fix login crash when email is empty' is good",
            "Learn git stash and git rebase early — they save hours"
        ]
    },

    "Docker": {
        "why_it_matters": "Docker lets you package your app so it runs the same everywhere — on your laptop, a teammate's machine, or a cloud server. It's now expected in most backend and ML roles.",
        "time_estimate": "2 weeks",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "Docker Official Docs", "url": "https://docs.docker.com/get-started/", "type": "Docs"},
            {"name": "Docker Tutorial for Beginners — TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "type": "Video"},
            {"name": "Play with Docker (browser-based practice)", "url": "https://labs.play-with-docker.com", "type": "Interactive"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Docker basics — images, containers, Dockerfile, docker run", "goal": "Containerise a simple Python app"},
            {"week": 2, "focus": "Docker Compose, volumes, networking, pushing to Docker Hub", "goal": "Run a multi-container app (app + database)"},
        ],
        "project_to_build": {
            "name": "Dockerise SkillMirror",
            "description": "Package your Streamlit app into a Docker container",
            "why": "Proves you can containerise a real ML app — directly relevant to any DS/SWE role"
        },
        "tips": [
            "Always use .dockerignore to exclude venv and data files",
            "Keep images small — use python:3.11-slim as base, not full python:3.11",
            "Docker Compose is what you'll use 90% of the time in real jobs"
        ]
    },

    "Kubernetes": {
        "why_it_matters": "Kubernetes orchestrates containers at scale. It's the standard for deploying ML models and web apps in production at any company running microservices.",
        "time_estimate": "3 weeks",
        "difficulty": "Advanced",
        "free_resources": [
            {"name": "Kubernetes Official Docs", "url": "https://kubernetes.io/docs/tutorials/", "type": "Docs"},
            {"name": "Kubernetes Tutorial for Beginners — TechWorld with Nana", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "type": "Video"},
            {"name": "KodeKloud Free Labs", "url": "https://kodekloud.com/courses/labs-kubernetes-for-the-absolute-beginners/", "type": "Interactive"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Pods, deployments, services, kubectl basics", "goal": "Deploy a simple app on minikube locally"},
            {"week": 2, "focus": "ConfigMaps, secrets, persistent volumes, namespaces", "goal": "Deploy a stateful app with a database"},
            {"week": 3, "focus": "Ingress, Helm charts, horizontal pod autoscaling", "goal": "Deploy a real app on free tier cloud K8s"},
        ],
        "project_to_build": {
            "name": "Deploy a Flask API on Kubernetes",
            "description": "Containerise a REST API and deploy it on minikube with 3 replicas",
            "why": "Shows you can handle production-grade deployment — rare skill for fresh graduates"
        },
        "tips": [
            "Learn Docker thoroughly before Kubernetes — K8s builds on Docker concepts",
            "Use minikube locally to practice without cloud costs",
            "kubectl get all and kubectl describe are your best debugging tools"
        ]
    },

    "Data Engineering": {
        "why_it_matters": "Data engineers build the pipelines that feed data to analysts and ML models. It's one of the highest paying data roles and in huge demand.",
        "time_estimate": "1 month",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "Data Engineering Zoomcamp (free)", "url": "https://github.com/DataTalksClub/data-engineering-zoomcamp", "type": "Course"},
            {"name": "Apache Airflow Tutorial", "url": "https://www.youtube.com/watch?v=K9AnJ9_ZAXE", "type": "Video"},
            {"name": "dbt Learn (free)", "url": "https://learn.getdbt.com", "type": "Course"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "ETL concepts, Python pipelines, data cleaning at scale", "goal": "Build a basic ETL pipeline in Python"},
            {"week": 2, "focus": "Apache Airflow — DAGs, scheduling, operators", "goal": "Automate a data pipeline with Airflow"},
            {"week": 3, "focus": "Data warehousing concepts, dbt basics", "goal": "Transform raw data into analytics-ready tables"},
            {"week": 4, "focus": "Cloud storage (S3/GCS), Spark basics", "goal": "Build an end-to-end pipeline on cloud"},
        ],
        "project_to_build": {
            "name": "Job Market Data Pipeline",
            "description": "Build an automated pipeline that scrapes job postings daily and stores them in a structured format",
            "why": "Directly relevant to SkillMirror and shows end-to-end data engineering skills"
        },
        "tips": [
            "Learn SQL deeply before data engineering — it's the foundation",
            "Airflow is the most in-demand orchestration tool — prioritise it",
            "Data quality is as important as the pipeline itself"
        ]
    },

    "XGBoost": {
        "why_it_matters": "XGBoost wins Kaggle competitions and dominates tabular data in industry. It's faster and more accurate than most deep learning models for structured data.",
        "time_estimate": "1 week",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "XGBoost Official Docs", "url": "https://xgboost.readthedocs.io/en/stable/", "type": "Docs"},
            {"name": "XGBoost Tutorial — StatQuest", "url": "https://www.youtube.com/watch?v=OtD8wVaFm6E", "type": "Video"},
            {"name": "Kaggle XGBoost Tutorial", "url": "https://www.kaggle.com/learn/intermediate-machine-learning", "type": "Course"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Gradient boosting theory, XGBoost API, hyperparameter tuning", "goal": "Beat a baseline model on a Kaggle dataset"},
        ],
        "project_to_build": {
            "name": "Placement Predictor",
            "description": "Use XGBoost to predict campus placement outcomes from student data",
            "why": "Tabular data + XGBoost is the most common ML interview task"
        },
        "tips": [
            "Always start with XGBoost before trying deep learning on tabular data",
            "SHAP values + XGBoost = explainable ML — very impressive in interviews",
            "LightGBM is faster for very large datasets — learn both"
        ]
    },

    "JavaScript": {
        "why_it_matters": "JavaScript is the language of the web. Every frontend role requires it and most full stack roles do too.",
        "time_estimate": "1 month",
        "difficulty": "Beginner",
        "free_resources": [
            {"name": "JavaScript.info (best free JS resource)", "url": "https://javascript.info", "type": "Book"},
            {"name": "freeCodeCamp JavaScript Course", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "Course"},
            {"name": "JavaScript30 — 30 projects in 30 days", "url": "https://javascript30.com", "type": "Course"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Variables, functions, arrays, objects, DOM manipulation", "goal": "Build an interactive webpage"},
            {"week": 2, "focus": "ES6+ features, async/await, fetch API, promises", "goal": "Fetch and display data from a public API"},
            {"week": 3, "focus": "React basics — components, props, state, hooks", "goal": "Build a simple React app"},
            {"week": 4, "focus": "NodeJS basics, REST APIs, Express", "goal": "Build a full stack mini app"},
        ],
        "project_to_build": {
            "name": "SkillMirror Web Version",
            "description": "Build a simple web frontend for SkillMirror using React",
            "why": "Shows full stack thinking and directly extends your existing project"
        },
        "tips": [
            "Master vanilla JS before jumping to React — frameworks make more sense after",
            "Build projects from day 1 — JS is learned by doing, not reading",
            "Chrome DevTools is your best friend — learn to debug in the browser"
        ]
    },

    "Java": {
        "why_it_matters": "Java powers most enterprise backends, Android apps, and large-scale systems. It's the most commonly tested language in product company interviews.",
        "time_estimate": "1 month",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "Java Programming MOOC (University of Helsinki)", "url": "https://java-programming.mooc.fi", "type": "Course"},
            {"name": "Java Full Course — Bro Code", "url": "https://www.youtube.com/watch?v=xk4_1vDrzzo", "type": "Video"},
            {"name": "LeetCode Java Problems", "url": "https://leetcode.com/problemset/", "type": "Practice"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Java syntax, OOP — classes, inheritance, interfaces", "goal": "Build a simple OOP project"},
            {"week": 2, "focus": "Collections, generics, exception handling, file I/O", "goal": "Build a data management app"},
            {"week": 3, "focus": "Multithreading, streams, lambda expressions", "goal": "Build a concurrent app"},
            {"week": 4, "focus": "Spring Boot basics, REST API development", "goal": "Build and test a REST API"},
        ],
        "project_to_build": {
            "name": "Student Management REST API",
            "description": "Build a Spring Boot REST API with CRUD operations and a database",
            "why": "Spring Boot is the most in-demand Java framework — shows enterprise readiness"
        },
        "tips": [
            "Java is verbose but teaches OOP properly — the concepts transfer to every language",
            "Focus on Collections and OOP first — they appear in every interview",
            "IntelliJ IDEA Community Edition is free and far better than Eclipse"
        ]
    },

    "Web Development": {
        "why_it_matters": "Web development skills are expected even in data and ML roles — for building dashboards, APIs, and deploying models as web apps.",
        "time_estimate": "1 month",
        "difficulty": "Beginner",
        "free_resources": [
            {"name": "The Odin Project (free, project-based)", "url": "https://www.theodinproject.com", "type": "Course"},
            {"name": "freeCodeCamp Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "type": "Course"},
            {"name": "CSS Tricks", "url": "https://css-tricks.com", "type": "Docs"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "HTML5 — structure, semantic tags, forms", "goal": "Build a personal portfolio page"},
            {"week": 2, "focus": "CSS3 — flexbox, grid, responsive design", "goal": "Make your portfolio mobile-friendly"},
            {"week": 3, "focus": "JavaScript DOM, events, fetch API", "goal": "Add interactivity to your portfolio"},
            {"week": 4, "focus": "Deploy with GitHub Pages or Netlify", "goal": "Live portfolio with a real URL"},
        ],
        "project_to_build": {
            "name": "Personal Portfolio Website",
            "description": "A responsive portfolio showcasing your projects, skills, and contact info",
            "why": "A live portfolio URL on your resume is worth more than any certification"
        },
        "tips": [
            "Build real projects from day 1 — tutorials alone won't get you hired",
            "Learn flexbox and CSS grid properly — they solve 90% of layout problems",
            "Deploy early — having a live URL feels great and impresses employers"
        ]
    },

    "Cloud Computing": {
        "why_it_matters": "Cloud is where everything runs in production. AWS is the most in-demand platform and knowledge of cloud basics is expected in most tech roles.",
        "time_estimate": "3 weeks",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "AWS Free Tier (12 months free)", "url": "https://aws.amazon.com/free/", "type": "Practice"},
            {"name": "AWS Cloud Practitioner Essentials (free)", "url": "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials", "type": "Course"},
            {"name": "freeCodeCamp AWS Course", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "type": "Video"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Cloud concepts, AWS core services — EC2, S3, IAM", "goal": "Deploy a static website on S3"},
            {"week": 2, "focus": "Lambda, API Gateway, RDS, VPC basics", "goal": "Build a serverless API"},
            {"week": 3, "focus": "Deploy a real app — EC2 + RDS + S3", "goal": "Host your portfolio or SkillMirror on AWS"},
        ],
        "project_to_build": {
            "name": "Deploy SkillMirror on AWS",
            "description": "Host your Streamlit app on an EC2 instance with a public URL",
            "why": "Shows cloud deployment skills — directly relevant to any engineering role"
        },
        "tips": [
            "Use the AWS Free Tier — most beginner projects cost nothing",
            "Learn IAM properly — bad permissions cause most cloud security issues",
            "AWS Certified Cloud Practitioner is worth getting — it's beginner friendly and recognised"
        ]
    },

    "Linux": {
        "why_it_matters": "Most servers run Linux. Every DevOps, backend, and ML engineering role expects comfortable command line usage.",
        "time_estimate": "1 week",
        "difficulty": "Beginner",
        "free_resources": [
            {"name": "Linux Command Line Basics — freeCodeCamp", "url": "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "type": "Video"},
            {"name": "The Linux Command Line (free book)", "url": "https://linuxcommand.org/tlcl.php", "type": "Book"},
            {"name": "OverTheWire Bandit (learn Linux by hacking)", "url": "https://overthewire.org/wargames/bandit/", "type": "Interactive"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Navigation, file operations, permissions, processes, bash scripting", "goal": "Automate a repetitive task with a bash script"},
        ],
        "project_to_build": {
            "name": "Bash Automation Script",
            "description": "Write a script that automates your project setup — creates folders, activates venv, installs requirements",
            "why": "Shows practical Linux usage and saves you time every day"
        },
        "tips": [
            "Use WSL2 on Windows to get a real Linux environment",
            "Learn vim basics — you'll need it on servers where no GUI exists",
            "man command is your best friend — man ls, man grep, man everything"
        ]
    },

    "Embedded Systems": {
        "why_it_matters": "Embedded systems power everything from cars to medical devices. It's a specialised, high-paying field with strong demand in automotive, IoT, and defence sectors.",
        "time_estimate": "2 months",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "Embedded Systems — University of Texas (Coursera free audit)", "url": "https://www.coursera.org/specializations/embedded-systems-shape-the-world", "type": "Course"},
            {"name": "Arduino Getting Started", "url": "https://www.arduino.cc/en/Guide", "type": "Docs"},
            {"name": "Bare Metal Embedded — YouTube", "url": "https://www.youtube.com/watch?v=hyZS2p1tW-g", "type": "Video"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "C programming review, microcontroller architecture, GPIO", "goal": "Blink an LED and read a button on Arduino"},
            {"week": 2, "focus": "UART, SPI, I2C communication protocols", "goal": "Interface a sensor and display readings"},
            {"week": 3, "focus": "Interrupts, timers, PWM", "goal": "Build a motor controller"},
            {"week": 4, "focus": "RTOS basics — tasks, queues, semaphores", "goal": "Run two tasks concurrently on FreeRTOS"},
        ],
        "project_to_build": {
            "name": "IoT Weather Station",
            "description": "Read temperature and humidity from a DHT11 sensor and send data to a cloud dashboard",
            "why": "Covers sensors, communication, and cloud — shows full embedded + IoT stack"
        },
        "tips": [
            "Get an Arduino or STM32 Nucleo board — hands-on practice is essential",
            "Read datasheets — the ability to understand hardware documentation separates embedded engineers",
            "FreeRTOS is the most popular RTOS — learn it early"
        ]
    },

    "VLSI": {
        "why_it_matters": "VLSI engineers design the chips inside every electronic device. It's a specialised, high-paying field concentrated in semiconductor companies like Intel, Qualcomm, and TSMC.",
        "time_estimate": "2 months",
        "difficulty": "Advanced",
        "free_resources": [
            {"name": "VLSI Design — NPTEL (free)", "url": "https://nptel.ac.in/courses/108105127", "type": "Course"},
            {"name": "Nandland — FPGA and Verilog tutorials", "url": "https://www.nandland.com", "type": "Docs"},
            {"name": "HDLBits — Verilog practice", "url": "https://hdlbits.01xz.net/wiki/Main_Page", "type": "Interactive"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Digital logic review, Verilog basics, combinational circuits", "goal": "Implement basic gates and MUX in Verilog"},
            {"week": 2, "focus": "Sequential circuits, FSMs, flip-flops in Verilog", "goal": "Build a traffic light controller FSM"},
            {"week": 3, "focus": "FPGA implementation, timing analysis, synthesis", "goal": "Implement a design on FPGA simulation"},
            {"week": 4, "focus": "CMOS basics, standard cell design, layout concepts", "goal": "Understand a simple standard cell layout"},
        ],
        "project_to_build": {
            "name": "RISC-V Processor Core",
            "description": "Implement a simple 4-bit ALU in Verilog and simulate it",
            "why": "Shows RTL design skills — the core requirement for VLSI design roles"
        },
        "tips": [
            "HDLBits is the LeetCode of VLSI — solve all problems",
            "Simulation before synthesis — always verify your design in simulation first",
            "Learn timing constraints early — setup and hold violations cause most chip bugs"
        ]
    },

    "CAD": {
        "why_it_matters": "CAD is the core tool of every mechanical engineer. Without it, you can't design parts, create assemblies, or generate manufacturing drawings.",
        "time_estimate": "3 weeks",
        "difficulty": "Beginner",
        "free_resources": [
            {"name": "SolidWorks Tutorials (official)", "url": "https://www.solidworks.com/sw/resources/solidworks-tutorials.htm", "type": "Docs"},
            {"name": "FreeCAD — free open source CAD", "url": "https://www.freecad.org/", "type": "Software"},
            {"name": "Autodesk Fusion 360 (free for students)", "url": "https://www.autodesk.com/education/edu-software/overview", "type": "Software"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "2D sketching, constraints, dimensions", "goal": "Create 5 mechanical sketches"},
            {"week": 2, "focus": "3D modelling — extrude, revolve, sweep, loft", "goal": "Model a mechanical component"},
            {"week": 3, "focus": "Assembly modelling, mates, exploded views, drawings", "goal": "Create a full assembly with drawing"},
        ],
        "project_to_build": {
            "name": "Mechanical Assembly Model",
            "description": "Model a real object (clamp, bearing housing, or gear assembly) from scratch",
            "why": "Shows 3D modelling proficiency — the minimum requirement for any design role"
        },
        "tips": [
            "Get SolidWorks through your college — most engineering colleges have licences",
            "Fusion 360 is free for students and cloud-based — great for beginners",
            "Learn GD&T (Geometric Dimensioning and Tolerancing) — it's tested in interviews"
        ]
    },

    "Network Security": {
        "why_it_matters": "Cyber attacks cost companies billions. Network security skills are in massive demand and the field has one of the lowest unemployment rates in tech.",
        "time_estimate": "1 month",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": "Professor Messer Network+ (free)", "url": "https://www.professormesser.com/network-plus/n10-008/n10-008-video/n10-008-training-course/", "type": "Video"},
            {"name": "TryHackMe — learn by doing (free tier)", "url": "https://tryhackme.com", "type": "Interactive"},
            {"name": "Cybersecurity for Everyone — Coursera (free audit)", "url": "https://www.coursera.org/learn/cybersecurity-for-everyone", "type": "Course"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Networking fundamentals — TCP/IP, DNS, HTTP, firewalls", "goal": "Set up a home lab with Wireshark"},
            {"week": 2, "focus": "Common attacks — SQL injection, XSS, phishing, MITM", "goal": "Complete 5 TryHackMe rooms"},
            {"week": 3, "focus": "Firewalls, IDS/IPS, VPNs, security policies", "goal": "Configure a basic firewall ruleset"},
            {"week": 4, "focus": "SIEM basics, log analysis, incident response", "goal": "Analyse a sample security incident"},
        ],
        "project_to_build": {
            "name": "Home Security Lab",
            "description": "Set up Kali Linux + Metasploitable in VirtualBox and practice ethical hacking",
            "why": "Hands-on labs beat certifications — shows real practical skills"
        },
        "tips": [
            "TryHackMe is the best free platform for practical cybersecurity — use it daily",
            "CompTIA Security+ is the entry-level cert most employers recognise",
            "Document everything — a security blog or write-ups on HackTheBox are great portfolio pieces"
        ]
    },

    "Penetration Testing": {
        "why_it_matters": "Penetration testers are paid to hack companies legally. It's one of the most exciting and well-paid roles in cybersecurity.",
        "time_estimate": "2 months",
        "difficulty": "Advanced",
        "free_resources": [
            {"name": "HackTheBox (free tier)", "url": "https://www.hackthebox.com", "type": "Interactive"},
            {"name": "TryHackMe — Jr Penetration Tester path", "url": "https://tryhackme.com/path/outline/jrpenetrationtester", "type": "Course"},
            {"name": "OWASP Testing Guide (free)", "url": "https://owasp.org/www-project-web-security-testing-guide/", "type": "Docs"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": "Linux, networking, Python scripting for security", "goal": "Set up Kali Linux and complete basic rooms on TryHackMe"},
            {"week": 2, "focus": "Web vulnerabilities — SQL injection, XSS, CSRF", "goal": "Complete OWASP Top 10 on TryHackMe"},
            {"week": 3, "focus": "Network scanning, enumeration, Metasploit", "goal": "Hack your first Metasploitable machine"},
            {"week": 4, "focus": "Report writing, responsible disclosure, bug bounty basics", "goal": "Submit your first bug bounty report"},
        ],
        "project_to_build": {
            "name": "Bug Bounty Write-up",
            "description": "Find and report a vulnerability through HackerOne or Bugcrowd",
            "why": "Real bug bounties pay money and prove skills better than any certificate"
        },
        "tips": [
            "Always practice on legal targets only — TryHackMe, HackTheBox, your own lab",
            "Python scripting is essential for automating pentesting tasks",
            "Write up every box you solve — builds your portfolio and helps you learn"
        ]
    },
}

# ── Role-specific why_it_matters overrides ────────────────────────────────────

ROLE_OVERRIDES = {
    "Software Engineering": {
        "Git": "Git is non-negotiable in software engineering. Every team uses it for code collaboration, code review, and deployment pipelines.",
        "Docker": "Software engineers are expected to containerise their apps. Docker is how you ship code that works the same in dev, staging, and production.",
    },
    "Data & AI": {
        "Git": "Data scientists use Git to version control notebooks, models, and pipelines. Without it, reproducing your own experiments is impossible.",
        "Docker": "ML engineers containerise models for deployment. Docker is how a model goes from your Jupyter notebook to a production API.",
    },
    "Cloud & DevOps": {
        "Git": "Git is the foundation of CI/CD. Every DevOps pipeline starts with a git push.",
        "Docker": "Docker is the core of DevOps. Everything in cloud-native development runs in containers.",
    }
}

# ── Default roadmap for unknown skills ────────────────────────────────────────

def get_default_roadmap(skill, role_group, demand_pct):
    return {
        "skill": skill,
        "why_it_matters": f"{skill} appears in {demand_pct}% of {role_group} job descriptions, making it an important skill to develop.",
        "time_estimate": "2-4 weeks",
        "difficulty": "Intermediate",
        "free_resources": [
            {"name": f"Search '{skill} tutorial' on YouTube", "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial", "type": "Video"},
            {"name": f"Search '{skill}' on freeCodeCamp", "url": f"https://www.freecodecamp.org/news/search/?query={skill.replace(' ', '+')}", "type": "Article"},
            {"name": f"Official {skill} documentation", "url": f"https://www.google.com/search?q={skill.replace(' ', '+')}+official+documentation", "type": "Docs"},
        ],
        "weekly_plan": [
            {"week": 1, "focus": f"Learn {skill} fundamentals", "goal": f"Understand what {skill} is and why it's used"},
            {"week": 2, "focus": f"Apply {skill} in a small project", "goal": f"Build something using {skill}"},
        ],
        "project_to_build": {
            "name": f"{skill} practice project",
            "description": f"Build a small project that demonstrates your {skill} knowledge",
            "why": "Employers want to see practical application, not just theoretical knowledge"
        },
        "tips": [
            f"Find a community around {skill} — Discord, Reddit, or local meetups",
            "Build something real, even if small — portfolio projects beat certifications"
        ],
        "demand_pct": demand_pct
    }

# ── Main functions ────────────────────────────────────────────────────────────

def generate_skill_roadmap(skill, role_group, demand_pct):
    """Get roadmap for a single skill."""
    roadmap = ROADMAP_DB.get(skill, None)

    if roadmap is None:
        return get_default_roadmap(skill, role_group, demand_pct)

    # Apply role-specific override if available
    result = roadmap.copy()
    if role_group in ROLE_OVERRIDES:
        if skill in ROLE_OVERRIDES[role_group]:
            result["why_it_matters"] = ROLE_OVERRIDES[role_group][skill]

    result["demand_pct"] = demand_pct
    return result


def generate_full_roadmap(gap_data, role_group):
    """Generate roadmap for all gap skills."""
    gaps = gap_data.get("gaps", [])

    if not gaps:
        return {"message": "No gaps found!", "roadmap": []}

    top_gaps = gaps[:5]
    print(f"\nGenerating roadmap for {len(top_gaps)} skills...")

    roadmap = []
    for gap in top_gaps:
        skill = gap["skill"]
        demand = gap["demand"]
        print(f"  ✓ {skill}")
        plan = generate_skill_roadmap(skill, role_group, demand)
        roadmap.append(plan)

    result = {
        "role_group": role_group,
        "total_gaps": len(gaps),
        "roadmap_generated_for": len(roadmap),
        "roadmap": roadmap
    }

    with open("data/roadmap.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Roadmap saved to data/roadmap.json")
    return result


# ── Test ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Testing roadmap generator...")
    result = generate_skill_roadmap("Git", "Software Engineering", 100.0)
    print(json.dumps(result, indent=2))