import streamlit as st
import streamlit.components.v1 as components
import base64, os
import json

st.set_page_config(page_title="Nature's Cluster", page_icon="🌿", layout="wide")

# --- HELPER FUNCTIONS ---
def b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# --- DATA LOADING ---
logo_b64 = b64("logo.jpg")
mmc_font_b64 = b64("mmc.ttf")

video_b64 = ""
video_type = "mp4"
for ext in ["mp4", "MP4", "mov", "MOV", "webm"]:
    p = f"home_components/hero.{ext}"
    if os.path.exists(p):
        video_b64 = b64(p)
        video_type = "mp4" if "mp4" in ext.lower() else ("webm" if "webm" in ext.lower() else "mp4")
        break

slides_html = ""
if os.path.exists("images"):
    imgs = []
    for f in sorted(os.listdir("images")):
        if f.lower().endswith((".jpg",".jpeg",".png")):
            imgs.append(f'<img class="slide" src="data:image/jpeg;base64,{b64(os.path.join("images",f))}">')
    slides_html = "".join(imgs)
    
# --- GALLERY LOADING ---
gallery_folder = "home_gallery"
gallery_html = ""
if os.path.exists(gallery_folder):
    imgs = []
    for f in sorted(os.listdir(gallery_folder)):
        if f.lower().endswith((".jpg", ".jpeg", ".png")):
            b64_img = b64(os.path.join(gallery_folder, f))
            name = os.path.splitext(f)[0].replace("_", " ").title()
            imgs.append(f'''
                <div class="gallery-slide">
                    <img src="data:image/jpeg;base64,{b64_img}">
                    
                </div>
            ''')
    gallery_html = "".join(imgs)
    
qr_b64 = b64("qr_code.png")

# --- MODULAR COMPONENTS ---
CSS_STYLES = """
::-webkit-scrollbar {
    display: none;
}

@font-face {{
    font-family: 'MMC';
    /* Use data:font/woff if you are using a .woff file */
    src: url(data:font/truetype;charset=utf-8;base64,{mmc_font_b64}) format('truetype');
    font-weight: normal;
    font-style: normal;
}}

@import url('https://fonts.googleapis.com/css2?family=Cabin:ital,wght@0,400;0,600;1,400&family=Lora:ital,wght@0,400;0,600;0,700;1,400&display=swap');

body{margin:0;width:100%;font-family:MMC;background:#fff;}
.header{display:flex;justify-content:space-between;align-items:center;padding:15px 40px;background:white;position:fixed;top:0;width:100%;z-index:999;border-bottom:1px solid #eee;box-sizing:border-box;}
.left{display:flex;align-items:center;}
.logo{height:105px;width:105px;margin-right:15px;}

/* Container for Name/Tagline to control alignment */
.text-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}

/* English Styling */
.name-en {
    font-family:MMC;
    font-size: 42px; 
    font-weight: 800; 
    color: #004B23; 
    text-align: left; 
    margin: 0; 
    margin-left: 0px;  /* X-axis spacing: adjust to move right */
    margin-top: 0px;   /* Y-axis spacing: adjust to move down */
}
.tag-en { 
    color: saddlebrown;
     font-family:'MMC',Segoe UI, sans-serif;
    font-style: italic; 
    font-size: 24px; 
    text-align: left; 
    margin: 0;
    margin-left: 100px;  /* X-axis spacing: adjust to move right */
    padding-top: -38px;  /* Y-axis spacing: distance from headline */
    margin-top: 0px;
}

/* Kannada Styling */
.name-kn { 
    font-size: 42px; 
    font-weight: 800; 
    color: #004B23; 
    font-family: 'Noto Sans Kannada', sans-serif;
    text-align: left; 
    margin: 0; 
    margin-left: 0px;  /* X-axis spacing: adjust to move right */
    margin-top: -10px;   /* Y-axis spacing: adjust to move down */
}
.tag-kn { 
    color: saddlebrown; 
    font-size: 17px; 
    font-family: 'Noto Sans Kannada', sans-serif;
    text-align: left; 
    margin: 0;
    line-height: 1;
    margin-left: 0px;  /* X-axis spacing: adjust to move right */
    padding-top: -80px;  /* Y-axis spacing: distance from headline */
    margin-top: -20px;   /* Y-axis spacing: adjust to move down */
}

.menu{cursor:pointer;}
.menu span{display:block;width:35px;height:4px;background:#004B23;margin:6px;border-radius:10px;}


/* --- UPDATED DRAWER & NAVIGATION STYLES --- */
.drawer {
    position: fixed;
    right: -320px;
    top: 0;
    width: 270px;
    height: 5.9%; 
    background: #004B23; /* Primary Dark Green */
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1001;
    overflow-y: auto;
    box-shadow: -5px 0 25px rgba(0,0,0,0.5); /* Stronger shadow for depth */
}
.drawer.active { 
    right: 0; 
}

/* Main Navigation Links & Dropdown Button */
.drawer a:not(.close), .dropbtn {
    display: block;
    color: #FDFBF7; /* Off-white for crisp readability */
    text-decoration: none;
    padding: 20px 30px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
    border-left: 0px solid #C97A1D; /* Initial hidden highlight bar */
    box-sizing: border-box;
    width: 100%;
}

/* Highlight Hover Effect */
.drawer a:not(.close):hover, .dropbtn:hover {
    background: rgba(201, 122, 29, 0.15); /* Subtle golden tint */
    color: #C97A1D; /* Golden Brown text */
    border-left: 8px solid #C97A1D; /* Thick highlight bar appears */
    padding-left: 38px; /* Pushes text right dynamically */
}

/* Dropdown Container */
.dropdown {
    width: 100%;
    display: block;
}

.dropbtn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    margin: 0;
}

/* Active state for the dropdown button itself */
.dropdown.active .dropbtn {
    color: #C97A1D;
    background: rgba(0, 0, 0, 0.2);
}

/* Dropdown Content Area */
.dropdown-content {
    display: none;
    background-color: #002210; /* Deeper green to separate sub-menu */
    flex-direction: column;
    width: 100%;
}

.dropdown.active .dropdown-content { 
    display: flex; 
}

/* Nested Dropdown Links */
.dropdown-content a:not(.close) {
    padding: 15px 30px 15px 50px; /* Deep indentation for visual hierarchy */
    font-size: 15px;
    font-weight: 400;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* Highlight Hover Effect for Nested Links */
.dropdown-content a:not(.close):hover {
    background: rgba(201, 122, 29, 0.2);
    border-left: 4px solid #C97A1D; /* Thinner highlight for sub-items */
    padding-left: 56px; /* Smooth text shift */
}

/* Close Button Styling */
.close {
    color: white;
    font-size: 40px;
    padding: 15px 30px;
    text-align: right;
    cursor: pointer;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    transition: color 0.3s ease;
}
.close:hover {
    color: #C97A1D;
}

.hero{position:relative;height:15vh;overflow:hidden;}
.hero video{position:relative;top:0;left:0;width:100%;height:100%;object-fit:cover;}
.overlay{position:absolute;inset:0;background:rgba(0,0,0,.45);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;text-align:center;padding:20px;}
.overlay h1{font-size:72px;margin:10px;}
.btn{background:#C97A1D;color:white;padding:14px 28px;border-radius:30px;margin:8px;display:inline-block;text-decoration:none;}
.section{padding:60px 10%;}
.title{font-size:42px;color:#004B23;text-align:center;margin-bottom:20px;}
.para{text-align:center;font-size:18px;color:#555;line-height:1.6;}
.highlight{font-style:italic;color:#C97A1D;text-align:center;font-weight:bold;margin:20px 0;}
.slider{height:500px;overflow:hidden;border-radius:20px;}
.slide{display:none;width:100%;height:100%;object-fit:cover;}
.cards{display:grid;grid-template-columns:repeat(auto-fit, minmax(250px, 1fr));gap:20px;}
.card{background:#f7f7f7;padding:25px;border-radius:15px;text-align:center;}
.feature{background:#004B23;color:white;padding:60px;border-radius:20px;text-align:center;}
.impact{display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:20px;}
.metric{background:#004B23;color:white;padding:30px;border-radius:15px;text-align:center;}
.metric h1 {
    font-size: 3.5rem;
    margin: 0;
    color: white; /* Golden Brown for the numbers */
}
.feature-container {
    /* Vibrant Gradient Background */
    background: linear-gradient(135deg, #004B23 0%, #006400 100%);
    color: white;
    padding: 80px 40px;
    border-radius: 30px;
    text-align: center;
    position: relative;
    min-height: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Adding a subtle shadow for depth */
    box-shadow: 0 10px 30px rgba(0, 75, 35, 0.3);
    overflow: hidden;
}

.feature-slide h4 {
    color: #C97A1D; /* Accent color for the label */
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 14px;
    margin-bottom: 10px;
}

.feature-slide h1 {
    font-size: 52px;
    margin: 10px 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.feature-slide p {
    font-size: 20px;
    max-width: 700px;
    margin: 20px auto;
    line-height: 1.5;
    opacity: 0.9;
}

.gautraa-section {
    padding: 50px 10%;
    background: linear-gradient(135deg, #fdfbf7 0%, #f4f1ea 100%);
    border-top: 5px solid #C97A1D;
    border-bottom: 5px solid #C97A1D;
    text-align: center;
    position: relative;
    margin-top:20px;
}

.gautraa-title {
    font-size: 52px;
    color: #004B23;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top:20px;
}

.gautraa-tagline {
    font-size: 24px;
    color: #004B23;
    font-style: italic;
    margin-bottom: 40px;
}

.gautraa-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.gautraa-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    border: 1px solid #e0dcd0;
    transition: transform 0.3s ease;
}

.gautraa-card:hover { transform: translateY(-10px); }
.icon-box { font-size: 40px; margin-bottom: 15px; }

.why-section {
    padding: 80px 10%;
    background: #FDFBF7;
    border-top: 2px solid #E0DCD0;
    border-bottom: 2px solid #E0DCD0;
}

.why-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    border: 1px solid #e0dcd0;
    
    /* Centering logic */
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.why-card p {
    color: #555;
    line-height: 1.6;
    margin-top: 10px;
    /* Uniform height prevents wobbling layouts */
    min-height: 80px; 
}


.testimonial-container {
    max-width: 600px;
    margin: 40px auto;
    text-align: center;
    position: relative;
    min-height: 350px;
}
.testimonial-card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border: 1px solid #E0DCD0;
    min-height: 200px;
    min-width: 500px;
    display: none; /* Hidden by default */
}
.testimonial-card.active { display: block; }
.stars { color: #C5A059; font-size: 30px; margin-bottom: 15px; }
.testimonial-card p { font-size: 20px; font-style: italic; color: #333; margin-bottom: 20px; }
.testimonial-card h4 { color: #004B23; font-weight: bold; margin: 0; }

.gallery-wrapper {
    background: #002b16; /* Deep Dark Green */
    padding: 60px 10%;
    text-align: center;
    margin-radius:20px;
}
.gallery-container {
    max-width: 1000px;
    height: 450px;
    margin: 40px auto;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15px; /* Spacing between the 3 visible images */
    overflow: hidden;
}

.gallery-slide {
    width: 30%; /* Three images side-by-side */
    height: 70%;
    transition: all 0.6s ease-in-out;
    filter: brightness(0.4); /* Dim side images */
    transform: scale(0.9);
    
}

/* The highlighted center image */
.gallery-slide.active {
    filter: brightness(1);
    transform: scale(1.2); /* Make it pop */
    border: 2px solid #SADDLEBROWN;
    box-shadow: 0 0 0px #C97A1D;
    box-radius:20px;
    z-index: 0;
}

.gallery-slide img { 
    width: 100%; height: 100%; object-fit: cover; border-radius: 10px; 
}

.footer {
    background: #002b16;
    color: white;
    padding: 50px 10%;
    text-align: center;
    font-size:14px;
    border-top: 5px solid #C97A1D;
}

.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
    margin-top: 30px;
}

.footer-qr { width: 120px; height: 120px; margin-bottom: 10px; }

.social-links a {
    color: #C97A1D;
    font-size: 30px;
    margin: 0 10px;
    text-decoration: none;
    font-weight: bold;
}
.footer-social-wrapper {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
    font-size:20px;
}

.social-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: white;
    font-size: 15px;
    transition: 0.3s;
}

.social-item:hover { color: #C97A1D; }

.social-icon {
    font-size: 29px;
    margin-bottom: 5px;
}

"""

HEADER_SECTION = f"""
<div class="header">
    <div class="left">
        <img class="logo" src="data:image/jpeg;base64,{logo_b64}">
        <div class="text-container">
            <h1 id="nm" class="name-en">NATURE'S CLUSTER</h1>
            <div id="tg" class="tag-en">Land of Fortune</div>
        </div>
    </div>
    <div class="menu" onclick="toggleDrawer()">
        <span></span><span></span><span></span>
    </div>
</div>

<div id="drawer" class="drawer">
    <div class="close" onclick="toggleDrawer()">&times;</div>
    <a href="#home" onclick="toggleDrawer()">Home</a>
    <a href="#about" onclick="toggleDrawer()">About Us</a>
    
    <div class="dropdown" id="projects-dropdown">
        <a class="dropbtn" onclick="toggleDropdown()">Our Projects <span id="arrow">&#9662;</span></a>
        <div class="dropdown-content">
            <a href="/Chandan_Valley_Phase_1" target="_self">
    Chandan Valley Phase-I
</a>

<a href="/Chandan_Valley_Phase_2" target="_self">
    Chandan Valley Phase-II
</a>

<a href="/Tribal_Trails" target="_self">
    Tribal Trails
</a>

<a href="/Rhythm_of_Rivers" target="_self">
    Rhythm of Rivers
</a>
        </div>
    </div>
    
    <a href="/Gautraa" target="_blank">Gautraa</a>
    <a href="#contact" onclick="toggleDrawer()">Contact Us</a>
</div>
"""

HERO_SECTION = f"""
<div class="hero">
<video autoplay muted loop playsinline><source src="data:video/{video_type};base64,{video_b64}"></video>
<div class="overlay">
<h1>Building Wealth Through Nature</h1>
<p>Sustainable Farmland Development • Agroforestry • Cattle Management</p>
<div><a href="#" class="btn">Explore Projects</a><a href="#" class="btn">Contact Us</a></div>
</div>
</div>
"""

CONTENT_SECTIONS = f"""
<div class="section">
<h2 class="title">Creating Value Beyond Agriculture</h2>
<p class="para">Nature's Cluster isn't just about developing land; it’s about stewarding the future. We bridge the gap between ecological restoration and robust economic growth, turning underutilized landscapes into high-performing natural assets. By blending advanced scientific management with the wisdom of agroforestry, we transform barren spaces into vibrant ecosystems that stand the test of time. We aren’t just cultivating crops—we are nurturing legacies, restoring biodiversity, and securing a greener, wealthier tomorrow for everyone.</p>
<p class="highlight">We don't just develop land — we cultivate opportunities, ecosystems, and legacies.</p>
</div>

<div class="section" style="background:#f9f9f9;">
<h2 class="title">Every Acre Has A Story</h2>
<p class="para">From barren landscapes transformed into productive ecosystems to thriving plantations supporting communities and biodiversity, every project reflects our commitment to responsible growth and sustainable prosperity.</p>
<div class="slider" style="margin-top:30px;">{slides_html}</div>
</div>

<div class="impact">
    <div class="metric">
        <h1 class="counter" data-target="400" data-suffix="+">0</h1>
        <p>Acres Developed</p>
    </div>
    <div class="metric">
        <h1 class="counter" data-target="50000" data-suffix="+">0</h1>
        <p>Trees Planted</p>
    </div>
    <div class="metric">
        <h1 class="counter" data-target="50" data-suffix="+">0</h1>
        <p>Families Benefited</p>
    </div>
</div>

<div class="why-section">
    <h2 class="title">Why Choose Nature's Cluster!?</h2>
    <div class="cards">
        <!-- Each card now uses the 'why-card' class for alignment -->
        <div class="why-card">
            <h3>Engineered Agronomic Excellence</h3>
            <p>Our strategies are built on a foundation of formal Agricultural Engineering, ensuring every action on your land is calculated, scientific, and deliberate.</p>
        </div>
        <div class="why-card">
            <h3>Spatial Intelligence </h3>
            <p>We utilize advanced mapping and spatial analysis to optimize land usage, ensuring maximum efficiency in plantation layouts and grid management.</p>
        </div>
        <div class="why-card">
            <h3>Full-Cycle Transparency</h3>
            <p>We provide comprehensive, data-backed reporting, giving you complete visibility into work ledgers, timelines, and the status of your assets.</p>
        </div>
        <div class="why-card">
            <h3>Data-Driven Scalability</h3>
            <p>Our management models are built to scale, ensuring that the same high standards applied to a single plot are maintained across expansive estates.</p>
        </div>
        <div class="why-card">
            <h3>Proactive Risk Management</h3>
            <p>By anticipating biological and climate-related challenges early, we implement preventative measures to safeguard your long-term land investment.</p>
        </div>
        <div class="why-card">
            <h3>Integrated Economic Stability</h3>
            <p>We bridge the gap between ecological restoration and financial growth, creating assets designed to appreciate through sustainable productivity.</p>
        </div>
    </div>
</div>
"""
FEATURED_SECTION = """
<div class="section">
    <div id="project-slider" class="feature-container">
        <!-- Project 1 -->
        <div class="feature-slide active">
            <h4>Featured Nature's Cluster Initiative</h4>
            <h1>CHANDAN VALLEY PHASE-I</h1>
            <p>The Call of the Forest: A premium agroforestry destination featuring sandalwood, orchards, and biodiversity.</p>
            <br><a href="/chandan-valley-1" target="_blank" class="btn" style="background:#C97A1D; color:white; border:none; font-weight:bold;">Discover Project</a>
        </div>
        <!-- Project 2 -->
        <div class="feature-slide">
            <h4>Featured Nature's Cluster Initiative</h4>
            <h1>CHANDAN VALLEY PHASE-II</h1>
            <p>Expanding the legacy: Advanced irrigation, premium orchards, and sustainable growth at scale.</p>
            <br><a href="/chandan-valley-2" target="_blank" class="btn" style="background:#C97A1D; color:white; border:none; font-weight:bold;">Discover Project</a>
        </div>
        <!-- Project 3 -->
        <div class="feature-slide">
            <h4>Featured Nature's Cluster Initiative</h4>
            <h1>TRIBAL TRAILS</h1>
            <p>A journey through heritage: Integrating indigenous knowledge with modern ecological restoration.</p>
            <br><a href="/tribal-trails" target="_blank" class="btn" style="background:#C97A1D; color:white; border:none; font-weight:bold;">Discover Project</a>
        </div>
        <!-- Project 4 -->
        <div class="feature-slide">
            <h4>Featured Nature's Cluster Initiative</h4>
            <h1>RHYTHM OF RIVERS</h1>
            <p>Water-positive landscapes: Designing natural basins to nurture the land and restore the flow.</p>
            <br><a href="/rhythm-of-rivers" target="_blank" class="btn" style="background:#C97A1D; color:white; border:none; font-weight:bold;">Discover Project</a>
        </div>
    </div>
</div>
"""
GAUTRAA_SECTION = """
<div class="gautraa-section">
    <h2 class="gautraa-title"style="color:#2D241C">GAUTRAA</h2>
    <p class="gautraa-tagline">Nurturing Native Breeds. Building Sustainable Futures.</p>
    
    <div class="gautraa-grid">
        <div class="gautraa-card">
            <div class="icon-box"></div>
            <h3>Preserving Heritage</h3>
            <p>"Protecting the distinct genetic legacy of our indigenous breeds as a cornerstone of sustainable and resilient agriculture."</p>
        </div>
        <div class="gautraa-card">
            <div class="icon-box"></div>
            <h3>Farm-to-Table Integrity</h3>
            <p>"Delivering unrivaled purity by merging traditional cattle care with rigorous quality standards for your complete peace of mind."</p>
        </div>
        <div class="gautraa-card">
            <div class="icon-box;align:center;"></div>
            <h3>Regenerative Symbiosis</h3>
            <p>"Our cattle form the heart of a circular, sustainable ecosystem.We restore the vitality of our soil by utilizing farm outputs as bio-stimulants."</p>
        </div>
    </div>
    <div style="margin-top: 50px; text-align: center;">
        <a href="https://gautraa-m9qgdo95josswktvjaiayx.streamlit.app/" class="btn" style="background:#C5A059; color:#2D241C; padding:15px 30px; border-radius:30px; text-decoration:none; font-weight:bold; font-size:18px; display:inline-block;">
            Explore the Gautraa Way →
        </a>
    </div>
</div>
"""

GALLERY_SECTION = f"""
<div class="section gallery-wrapper">
    <h2 class="title" style="color:white">Nature's Cluster Gallery</h2>
    <div class="gallery-container">
        {gallery_html}
    </div>
</div>
"""


TESTIMONIAL_SECTION = """
<div class="section" style="background:#FDFBF7;">
    <h2 class="title">Client Testimonies</h2>
    <div id="testimony-carousel" class="testimonial-container">
        <div class="testimonial-card active">
            <div class="stars">★★★★★</div>
            <p>"Nature's Cluster transformed my vision of farmland into a high-performing asset. Their engineering standard is truly unmatched."</p>
            <h4>— Dr. Vikram Rao</h4>
        </div>
        <div class="testimonial-card">
            <div class="stars">★★★★★</div>
            <p>"The transparency in their reporting and the dedication to organic practices made me trust them completely with my land."</p>
            <h4>— Anitha Reddy</h4>
        </div>
        <div class="testimonial-card">
            <div class="stars">★★★★★</div>
            <p>"Gautraa dairy products are the purest I've found. It’s clear they put the same care into their cattle as they do their fields."</p>
            <h4>— Suresh Kumar</h4>
        </div>
    </div>
</div>
"""

FOOTER_SECTION = f"""
<div class="footer">
    <h2 style="color:#C5A059">"The greatest investment is the one that grows with nature."</h2>
    
    <div class="footer-grid">
        <div>
            <h4 style="font-size:20px">Contact Us</h4>
            <p style="font-size:15px">📞: +91 9591597415</p>
            <p style="font-size:15px">✉️: naturescluster@gmail.com</p>
        </div>
        
        <div>
            <h4 style="font-size:20px">Connect With Us</h4>
            <div class="footer-social-wrapper">
                <a href="https://wa.me/yournumber" class="social-item">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width: 30px; height: 30px;margin-bottom:10px">
        <span>WhatsApp</span>
    </a>
    
    <a href="https://instagram.com/yourhandle" class="social-item">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" alt="Instagram" style="width: 30px; height: 30px;margin-bottom:10px">
        <span>Instagram</span>
    </a>
    
    <a href="https://facebook.com/yourhandle" class="social-item">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" alt="Facebook" style="width: 30px; height: 30px;margin-bottom:10px">
        <span>Facebook</span>
    </a>
    
    <a href="https://youtube.com/@yourhandle" class="social-item">
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg" alt="YouTube" style="width: 30px; height: 30px;margin-bottom:10px">
        <span>YouTube</span>
    </a>
            </div>
        </div>
        
        <div>
            <h4 style="font-size:20px">Scan for Location</h4>
            <img src="data:image/jpeg;base64,{qr_b64}" class="footer-qr">
        </div>
    </div>
</div>
"""

JS_LOGIC = """
<script>
// 1. Drawer Toggle Logic
function toggleDrawer() {
    document.getElementById('drawer').classList.toggle('active');
}

// 1.5 Dropdown Toggle Logic
function toggleDropdown() {
    const dropdown = document.getElementById('projects-dropdown');
    const arrow = document.getElementById('arrow');
    dropdown.classList.toggle('active');
    
    // Toggle arrow direction
    if (dropdown.classList.contains('active')) {
        arrow.innerHTML = '&#9652;'; // Up arrow
    } else {
        arrow.innerHTML = '&#9662;'; // Down arrow
    }
}

// 2. Language Switcher Logic
const langs = [
    { name: "NATURE'S CLUSTER", tag: "Land of Fortune", nClass: "name-en", tClass: "tag-en" },
    { name: "ನೇಚರ್ಸ್ ಕ್ಲಸ್ಟರ್", tag: "ಲ್ಯಾಂಡ್ ಆಫ್ ಫಾರ್ಚೂನ್", nClass: "name-kn", tClass: "tag-kn" }
];

let i = 0;
setInterval(() => {
    i = (i + 1) % 2;
    const nm = document.getElementById("nm");
    const tg = document.getElementById("tg");
    if (nm && tg) {
        nm.innerHTML = langs[i].name;
        tg.innerHTML = langs[i].tag;
        nm.className = langs[i].nClass;
        tg.className = langs[i].tClass;
    }
}, 3000);

// 3. Image Slider Logic ("Every Acre Has A Story")
let s = 0;
let slides = document.getElementsByClassName("slide");
function showSlides() {
    if (slides.length === 0) return;
    for (let j = 0; j < slides.length; j++) {
        slides[j].style.display = "none";
    }
    slides[s].style.display = "block";
    s = (s + 1) % slides.length;
}
if (slides.length > 0) {
    showSlides();
    setInterval(showSlides, 3000);
}

// 4. Project Slider Logic ("Featured Project")
let pIdx = 0;
const pSlides = document.getElementsByClassName("feature-slide");
function showProjectSlides() {
    if (pSlides.length === 0) return;
    for (let j = 0; j < pSlides.length; j++) {
        pSlides[j].style.display = "none";
    }
    pIdx = (pIdx + 1) % pSlides.length;
    pSlides[pIdx].style.display = "block";
}
if (pSlides.length > 0) {
    for (let j = 0; j < pSlides.length; j++) { pSlides[j].style.display = "none"; }
    pSlides[0].style.display = "block";
    setInterval(showProjectSlides, 3000);
}

// Counter Animation Logic
const counters = document.querySelectorAll('.counter');

const animateCounters = () => {
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const suffix = counter.getAttribute('data-suffix') || '';
            const count = parseInt(counter.innerText);
            
            // Increment speed: Higher divider = slower count
            const inc = target / 100; 

            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(updateCount, 15);
            } else {
                // Apply the suffix once the counting is done
                counter.innerText = target + suffix;
            }
        };
        updateCount();
    });
};

// Intersection Observer to trigger only when scrolled into view
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        animateCounters();
        observer.disconnect(); 
    }
}, { threshold: 0.5 });

const impactSection = document.querySelector('.impact');
if (impactSection) observer.observe(impactSection);

// 5. Testimonial Carousel Logic
let tIdx = 0;
const tCards = document.getElementsByClassName("testimonial-card");
function showTestimonials() {
    if (tCards.length === 0) return;
    for (let j = 0; j < tCards.length; j++) {
        tCards[j].style.display = "none";
    }
    tIdx = (tIdx + 1) % tCards.length;
    tCards[tIdx].style.display = "block";
}
if (tCards.length > 0) {
    tCards[0].style.display = "block";
    setInterval(showTestimonials, 5000); // Rotates every 5 seconds
}
// 6. Sliding Gallery Carousel Logic
let gIdx = 1; // Start with the second image as the initial center
const gSlides = document.getElementsByClassName("gallery-slide");

function rotateGallery() {
    // Hide all first
    for (let j = 0; j < gSlides.length; j++) {
        gSlides[j].style.display = "none";
        gSlides[j].classList.remove("active");
    }

    // Indices for Left, Center, Right
    let left = (gIdx - 1 + gSlides.length) % gSlides.length;
    let center = gIdx;
    let right = (gIdx + 1) % gSlides.length;

    // Display the three visible images
    gSlides[left].style.display = "block";
    gSlides[center].style.display = "block";
    gSlides[right].style.display = "block";

    // Highlight the center one
    gSlides[center].classList.add("active");

    // Increment index to move the "flow" forward
    gIdx = (gIdx + 1) % gSlides.length;
}

// Ensure there are enough images to form a trio
if (gSlides.length >= 3) {
    rotateGallery(); // Initial call
    setInterval(rotateGallery, 2000); // 2 seconds per shift
} else {
    // If fewer than 3, just show them all
    for (let j = 0; j < gSlides.length; j++) gSlides[j].style.display = "block";
}

</script>
"""


# --- ASSEMBLY ---
full_html = f"""
<!DOCTYPE html>
<html>
<head><style>{CSS_STYLES}</style></head>
<body>
{HEADER_SECTION}
{HERO_SECTION}
{CONTENT_SECTIONS}
{FEATURED_SECTION}
{GAUTRAA_SECTION}
{GALLERY_SECTION}
{TESTIMONIAL_SECTION}
{FOOTER_SECTION}
{JS_LOGIC}
</body>
</html>
"""

components.html(full_html, height=7000,width=5000, scrolling=True)