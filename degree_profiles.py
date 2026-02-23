PCM_DEGREE_PROFILES = {

    # ===============================
    # CORE ENGINEERING BRANCHES
    # ===============================

    "Mechanical Engineering": {
        "academic": [0.9, 0.9, 0.75],
        "personality": [0.85, 0.7, 0.3, 0.3, 0.4, 0.6],
        "interest": [0.95, 0.4, 0.5, 0.6, 0.3, 0.2]
    },

    "Civil Engineering": {
        "academic": [0.8, 0.85, 0.7],
        "personality": [0.8, 0.6, 0.3, 0.4, 0.5, 0.6],
        "interest": [0.85, 0.3, 0.4, 0.7, 0.4, 0.2]
    },

    "Electrical Engineering": {
        "academic": [0.9, 0.85, 0.8],
        "personality": [0.75, 0.8, 0.3, 0.3, 0.4, 0.7],
        "interest": [0.9, 0.6, 0.5, 0.5, 0.3, 0.2]
    },

    # ===============================
    # COMPUTER DOMAIN BRANCHES
    # ===============================

    "Computer Science Engineering": {
        "academic": [0.95, 0.8, 0.7],
        "personality": [0.6, 0.95, 0.4, 0.3, 0.5, 0.7],
        "interest": [0.5, 0.95, 0.6, 0.3, 0.4, 0.6]
    },

    "Artificial Intelligence / ML": {
        "academic": [0.95, 0.85, 0.75],
        "personality": [0.6, 0.98, 0.4, 0.3, 0.5, 0.6],
        "interest": [0.4, 0.98, 0.9, 0.2, 0.3, 0.4]
    },

    "Data Science": {
        "academic": [0.95, 0.8, 0.7],
        "personality": [0.5, 0.95, 0.4, 0.3, 0.4, 0.8],
        "interest": [0.4, 0.95, 0.85, 0.2, 0.4, 0.3]
    },

    "Cyber Security": {
        "academic": [0.9, 0.8, 0.7],
        "personality": [0.6, 0.9, 0.3, 0.3, 0.4, 0.9],
        "interest": [0.5, 0.9, 0.6, 0.2, 0.4, 0.3]
    },

    # ===============================
    # PURE SCIENCE
    # ===============================

    "BSc Physics": {
        "academic": [0.9, 0.95, 0.7],
        "personality": [0.4, 0.98, 0.3, 0.3, 0.2, 0.6],
        "interest": [0.5, 0.7, 0.98, 0.3, 0.2, 0.2]
    },

    "BSc Mathematics": {
        "academic": [0.98, 0.7, 0.6],
        "personality": [0.4, 0.99, 0.3, 0.2, 0.2, 0.7],
        "interest": [0.6, 0.8, 0.95, 0.2, 0.2, 0.2]
    },

    # ===============================
    # DEFENSE
    # ===============================

    "NDA / Armed Forces Technical": {
        "academic": [0.8, 0.8, 0.7],
        "personality": [0.95, 0.6, 0.2, 0.3, 0.7, 0.5],
        "interest": [0.8, 0.4, 0.5, 0.98, 0.3, 0.2]
    },

    # ===============================
    # CREATIVE TECH
    # ===============================

    "Game Development": {
        "academic": [0.8, 0.7, 0.6],
        "personality": [0.4, 0.7, 0.9, 0.3, 0.4, 0.5],
        "interest": [0.5, 0.9, 0.6, 0.2, 0.4, 0.98]
    },

    "UI/UX & Design Technology": {
        "academic": [0.6, 0.6, 0.5],
        "personality": [0.3, 0.6, 0.98, 0.4, 0.4, 0.4],
        "interest": [0.3, 0.7, 0.4, 0.2, 0.5, 0.99]
    }
}

PCB_DEGREE_PROFILES = {

    # ===============================
    # CORE MEDICAL (BIOLOGY HEAVY)
    # ===============================

    "MBBS (Doctor)": {
        "academic": [0.99, 0.75, 0.8],   # Biology dominant
        "personality": [0.5, 0.9, 0.2, 0.98, 0.3, 0.5],
        "interest": [0.99, 0.5, 0.3, 0.6, 0.4, 0.3]
    },

    "BDS (Dentistry)": {
        "academic": [0.9, 0.7, 0.75],
        "personality": [0.6, 0.8, 0.3, 0.9, 0.4, 0.6],
        "interest": [0.9, 0.4, 0.3, 0.5, 0.3, 0.2]
    },

    # ===============================
    # ALTERNATIVE MEDICINE
    # ===============================

    "BAMS (Ayurveda)": {
        "academic": [0.85, 0.65, 0.7],
        "personality": [0.4, 0.6, 0.6, 0.9, 0.3, 0.5],
        "interest": [0.8, 0.4, 0.2, 0.6, 0.5, 0.4]
    },

    "BHMS (Homeopathy)": {
        "academic": [0.8, 0.6, 0.65],
        "personality": [0.4, 0.6, 0.7, 0.95, 0.3, 0.4],
        "interest": [0.75, 0.3, 0.2, 0.6, 0.6, 0.3]
    },

    # ===============================
    # RESEARCH FOCUSED
    # ===============================

    "BSc Biotechnology": {
        "academic": [0.92, 0.8, 0.85],
        "personality": [0.4, 0.98, 0.3, 0.5, 0.2, 0.7],
        "interest": [0.4, 0.99, 0.3, 0.3, 0.2, 0.4]
    },

    # ===============================
    # PHARMA (CHEMISTRY HEAVY)
    # ===============================

    "BPharm (Pharmacy)": {
        "academic": [0.85, 0.7, 0.99],  # Chemistry dominant
        "personality": [0.4, 0.8, 0.2, 0.5, 0.4, 0.9],
        "interest": [0.4, 0.6, 0.99, 0.4, 0.2, 0.3]
    },

    # ===============================
    # ALLIED HEALTH
    # ===============================

    "BSc Nursing / Physiotherapy": {
        "academic": [0.85, 0.6, 0.7],
        "personality": [0.3, 0.5, 0.3, 0.99, 0.3, 0.5],
        "interest": [0.6, 0.3, 0.3, 0.99, 0.5, 0.3]
    },

    # ===============================
    # PSYCHOLOGY
    # ===============================

    "BA/BSc Psychology": {
        "academic": [0.7, 0.5, 0.5],
        "personality": [0.2, 0.7, 0.6, 0.99, 0.3, 0.4],
        "interest": [0.3, 0.3, 0.2, 0.4, 0.99, 0.3]
    }
}



COMMERCE_DEGREE_PROFILES = {

    "Chartered Accountant (CA)": {
        "academic": [0.95, 0.85, 0.7],
        "personality": [0.3, 0.6, 0.2, 0.3, 0.8, 0.95],
        "interest": [0.98, 0.6, 0.5, 0.4, 0.4, 0.3, 0.6]
    },

    "Banking & Finance": {
        "academic": [0.8, 0.8, 0.6],
        "personality": [0.4, 0.6, 0.3, 0.5, 0.7, 0.8],
        "interest": [0.6, 0.95, 0.6, 0.4, 0.5, 0.3, 0.5]
    },

    "BBA / MBA": {
        "academic": [0.7, 0.6, 0.6],
        "personality": [0.3, 0.5, 0.4, 0.6, 0.95, 0.6],
        "interest": [0.5, 0.6, 0.98, 0.8, 0.4, 0.5, 0.6]
    },

    "Economics (BA/BSc Economics)": {
        "academic": [0.9, 0.95, 0.6],
        "personality": [0.3, 0.95, 0.2, 0.4, 0.6, 0.7],
        "interest": [0.5, 0.6, 0.6, 0.4, 0.98, 0.4, 0.7]
    },

    "Entrepreneurship / Startup": {
        "academic": [0.6, 0.6, 0.5],
        "personality": [0.3, 0.6, 0.4, 0.6, 0.98, 0.4],
        "interest": [0.4, 0.6, 0.9, 0.98, 0.5, 0.7, 0.6]
    },

    "Digital Marketing": {
        "academic": [0.6, 0.5, 0.5],
        "personality": [0.2, 0.5, 0.9, 0.7, 0.8, 0.4],
        "interest": [0.4, 0.5, 0.8, 0.7, 0.4, 0.98, 0.5]
    },

    "Business Analytics": {
        "academic": [0.9, 0.9, 0.7],
        "personality": [0.3, 0.95, 0.4, 0.4, 0.7, 0.8],
        "interest": [0.5, 0.6, 0.7, 0.6, 0.7, 0.5, 0.98]
    }
}