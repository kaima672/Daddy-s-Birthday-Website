import streamlit as st
import json
import os
import random
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Happy Birthday, Daddy! 🎂",
    page_icon="🎂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Persistent storage (JSON file) ───────────────────────────────────────────
MESSAGES_FILE = "birthday_messages.json"
GALLERY_DIR = "gallery"

def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    return []


def load_gallery_images():
    if not os.path.isdir(GALLERY_DIR):
        os.makedirs(GALLERY_DIR, exist_ok=True)
        return []
    return sorted(
        os.path.join(GALLERY_DIR, filename)
        for filename in os.listdir(GALLERY_DIR)
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    )

def save_messages(messages):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# ── Confetti + global styles ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --gold:   #C9A84C;
  --cream:  #FAF6EE;
  --dark:   #1A1208;
  --warm:   #8B4513;
  --blush:  #E8C5A0;
  --deep:   #2D1B00;
}

/* ── Reset ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--dark) !important;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { background: var(--deep) !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Hero ── */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  background: radial-gradient(ellipse at 30% 20%, #3D2400 0%, #1A1208 40%, #0D0804 100%);
  padding: 4rem 2rem;
}

/* Animated background orbs */
.hero::before, .hero::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.35;
  animation: drift 12s ease-in-out infinite alternate;
}
.hero::before {
  width: 600px; height: 600px;
  background: radial-gradient(circle, #C9A84C, transparent);
  top: -200px; left: -100px;
}
.hero::after {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #8B2500, transparent);
  bottom: -150px; right: -100px;
  animation-delay: -6s;
}
@keyframes drift {
  from { transform: translate(0,0) scale(1); }
  to   { transform: translate(40px, 30px) scale(1.1); }
}

.hero-eyebrow {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 1.5rem;
  animation: fadeUp 0.8s ease forwards;
  opacity: 0;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3.5rem, 9vw, 7rem);
  font-weight: 900;
  line-height: 1.05;
  color: var(--cream);
  margin: 0 0 0.5rem;
  animation: fadeUp 0.9s 0.15s ease forwards;
  opacity: 0;
}
.hero-title span { color: var(--gold); font-style: italic; }
.hero-subtitle {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.1rem, 2.5vw, 1.5rem);
  font-style: italic;
  color: var(--blush);
  margin-bottom: 2.5rem;
  animation: fadeUp 1s 0.3s ease forwards;
  opacity: 0;
}
.hero-divider {
  width: 120px; height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  margin: 0 auto 2.5rem;
  animation: fadeUp 1s 0.45s ease forwards;
  opacity: 0;
}
.hero-age {
  font-family: 'Playfair Display', serif;
  font-size: clamp(5rem, 14vw, 10rem);
  font-weight: 900;
  color: transparent;
  -webkit-text-stroke: 2px var(--gold);
  line-height: 1;
  opacity: 0.18;
  position: absolute;
  bottom: -2rem;
  right: 5%;
  user-select: none;
  pointer-events: none;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Confetti canvas ── */
#confetti-canvas {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 9999;
}

/* ── Section wrappers ── */
.section {
  padding: 5rem 2rem;
  max-width: 1100px;
  margin: 0 auto;
}
.section-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.4em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 0.75rem;
}
.section-heading {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 700;
  color: var(--cream);
  margin: 0 0 1rem;
}
.section-body {
  font-family: 'DM Sans', sans-serif;
  font-size: 1.05rem;
  color: var(--blush);
  line-height: 1.8;
  max-width: 680px;
}

/* ── Message cards ── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 3rem;
}
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}
.gallery-card {
  background: linear-gradient(135deg, #2D1B00 0%, #1F1200 100%);
  border: 1px solid rgba(201,168,76,0.18);
  border-radius: 18px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.gallery-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 55px rgba(0,0,0,0.35);
}
.gallery-card img {
  width: 100%;
  height: auto;
  display: block;
}
.gallery-caption {
  padding: 1rem 1.25rem 1.25rem;
  font-family: 'DM Sans', sans-serif;
  color: var(--blush);
  line-height: 1.6;
}
.msg-card {
  background: linear-gradient(135deg, #2D1B00 0%, #1F1200 100%);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 16px;
  padding: 1.75rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}
.msg-card:hover {
  transform: translateY(-5px);
  border-color: rgba(201,168,76,0.5);
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
.msg-card::before {
  content: '"';
  font-family: 'Playfair Display', serif;
  font-size: 6rem;
  color: var(--gold);
  opacity: 0.08;
  position: absolute;
  top: -1rem; left: 1rem;
  line-height: 1;
  pointer-events: none;
}
.msg-author {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 0.75rem;
}
.msg-relation {
  font-style: italic;
  opacity: 0.65;
  text-transform: none;
  letter-spacing: 0;
  font-size: 0.65rem;
}
.msg-text {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-style: italic;
  color: var(--cream);
  line-height: 1.7;
}
.msg-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.65rem;
  color: rgba(232,197,160,0.35);
  margin-top: 1.25rem;
}

/* ── Emoji reaction bar ── */
.reaction-bar {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}
.reaction-btn {
  background: rgba(201,168,76,0.1);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 999px;
  padding: 0.3rem 0.8rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--cream);
  font-family: 'DM Sans', sans-serif;
}
.reaction-btn:hover {
  background: rgba(201,168,76,0.25);
  transform: scale(1.1);
}

/* ── Timeline ── */
.timeline { position: relative; padding: 1rem 0; }
.timeline::before {
  content: '';
  position: absolute;
  left: 18px; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(to bottom, var(--gold), transparent);
}
.tl-item {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  position: relative;
}
.tl-dot {
  width: 38px; height: 38px;
  border-radius: 50%;
  background: var(--gold);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
  box-shadow: 0 0 20px rgba(201,168,76,0.4);
  z-index: 1;
}
.tl-content {
  background: rgba(45,27,0,0.6);
  border: 1px solid rgba(201,168,76,0.15);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  flex: 1;
}
.tl-year {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  color: var(--gold);
  margin-bottom: 0.3rem;
}
.tl-title {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  color: var(--cream);
  font-weight: 700;
}
.tl-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  color: var(--blush);
  margin-top: 0.25rem;
  line-height: 1.6;
}

/* ── Streamlit overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: rgba(45,27,0,0.7) !important;
  border: 1px solid rgba(201,168,76,0.3) !important;
  color: var(--cream) !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > label, .stTextArea > label, .stSelectbox > label {
  color: var(--blush) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
}
.stButton > button {
  background: linear-gradient(135deg, var(--gold), #A07830) !important;
  color: var(--dark) !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.05em !important;
  padding: 0.6rem 2rem !important;
  transition: all 0.3s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(201,168,76,0.4) !important;
}
div[data-testid="stHorizontalBlock"] { gap: 1.5rem; }

@media (max-width: 900px) {
  .hero {
    min-height: auto;
    padding: 3rem 1.25rem;
  }

  .hero-title {
    font-size: clamp(2.8rem, 10vw, 5rem);
  }

  .hero-subtitle {
    font-size: clamp(1rem, 3.5vw, 1.25rem);
    margin-bottom: 1.8rem;
  }

  .hero-age {
    font-size: clamp(3rem, 16vw, 7rem);
    right: 3%;
    bottom: -1.4rem;
  }

  .section {
    padding: 2.8rem 1.25rem;
  }

  .section-body {
    max-width: 100%;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }

  .timeline {
    padding: 1rem 0;
  }

  .tl-item {
    flex-direction: column;
    align-items: stretch;
  }

  .tl-dot {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }

  .stButton > button {
    width: 100% !important;
  }

  div[data-testid="stHorizontalBlock"] {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 600px) {
  .hero {
    padding: 2.4rem 1rem;
  }

  .hero-eyebrow {
    margin-bottom: 1rem;
  }

  .hero-divider {
    width: 90px;
    margin-bottom: 1.8rem;
  }

  .msg-card {
    padding: 1.3rem;
  }

  .section-heading {
    font-size: clamp(1.8rem, 7vw, 2.5rem);
  }

  .section-body {
    font-size: 1rem;
  }
}

/* ── Separator line ── */
.gold-line {
  width: 100%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent);
  margin: 0;
}

/* ── Footer ── */
.footer {
  text-align: center;
  padding: 3rem;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  color: rgba(232,197,160,0.4);
  font-size: 0.9rem;
}
</style>

<!-- Confetti Canvas -->
<canvas id="confetti-canvas"></canvas>

<script>
// Confetti burst on load
(function() {
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });

  const COLORS = ['#C9A84C','#FAF6EE','#E8C5A0','#8B4513','#FFD700','#FFA500'];
  const particles = [];

  class Particle {
    constructor() { this.reset(true); }
    reset(init=false) {
      this.x = Math.random() * canvas.width;
      this.y = init ? Math.random() * canvas.height - canvas.height : -10;
      this.size = Math.random() * 8 + 4;
      this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
      this.speed = Math.random() * 2 + 1;
      this.angle = Math.random() * Math.PI * 2;
      this.spin = (Math.random() - 0.5) * 0.15;
      this.drift = (Math.random() - 0.5) * 1.5;
      this.opacity = Math.random() * 0.7 + 0.3;
      this.shape = Math.random() > 0.5 ? 'rect' : 'circle';
    }
    update() {
      this.y += this.speed;
      this.x += this.drift;
      this.angle += this.spin;
      if (this.y > canvas.height + 20) this.reset();
    }
    draw() {
      ctx.save();
      ctx.globalAlpha = this.opacity;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.angle);
      ctx.fillStyle = this.color;
      if (this.shape === 'rect') {
        ctx.fillRect(-this.size/2, -this.size/4, this.size, this.size/2);
      } else {
        ctx.beginPath();
        ctx.arc(0, 0, this.size/2, 0, Math.PI*2);
        ctx.fill();
      }
      ctx.restore();
    }
  }

  for (let i = 0; i < 120; i++) particles.push(new Particle());

  let frame = 0;
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => { p.update(); p.draw(); });
    frame++;
    // Slow down after 5 seconds
    if (frame < 300 || frame % 3 === 0) requestAnimationFrame(animate);
    else requestAnimationFrame(animate);
  }
  animate();
})();
</script>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = load_messages()
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "show_confetti" not in st.session_state:
    st.session_state.show_confetti = False

page = st.sidebar.radio("Explore", ["Home", "Gallery"], index=0)
gallery_images = load_gallery_images()

if page == "Gallery":
    st.markdown("""
    <div class="section" style="padding-top:3rem; padding-bottom:1rem;">
      <div class="section-label">✦ Story Gallery</div>
      <h2 class="section-heading">Memories from the Heart</h2>
      <p class="section-body">
        These are the moments that make Dad's story so beautiful. Tap or scroll through to relive them.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if gallery_images:
        cols = st.columns(3)
        for index, image_path in enumerate(gallery_images):
            with cols[index % 3]:
                caption = os.path.basename(image_path).replace("_", " ").rsplit('.', 1)[0].title()
                st.image(image_path, caption=caption, width=340)
    else:
        st.warning(
            f"No gallery images found. Add photo files to the `{GALLERY_DIR}` folder so they show up here."
        )
        st.info("Supported file types: PNG, JPG, JPEG, GIF, WEBP.")

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="footer">Thank you for the memories — keep adding more moments to the gallery.</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">✦ A Celebration ✦</div>
  <h1 class="hero-title">  Happy Birthday, Daddy! 🎂<br></h1>
  <p class="hero-subtitle">Thank you for everything you are and everything you do in the life of the Ezeibe family.</p>
  <div class="hero-divider"></div>
  <p style="font-family:'DM Sans',sans-serif; color:rgba(232,197,160,0.55); font-size:0.9rem; letter-spacing:0.1em;">
    Scroll down to read messages from the people who love you most 💛
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
  <div class="section-label">✦ Family Memories</div>
  <h2 class="section-heading">Gallery of Moments</h2>
</div>
""", unsafe_allow_html=True)

if gallery_images:
    cols = st.columns(3)
    for index, image_path in enumerate(gallery_images):
        with cols[index % 3]:
            caption = os.path.basename(image_path).replace("_", " ").rsplit('.', 1)[0].title()
            st.image(image_path, caption=caption, width=340)
else:
    st.warning(
        f"No gallery images were found in `{GALLERY_DIR}`. Add photos there to display them here."
    )

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ── ABOUT / TRIBUTE SECTION ───────────────────────────────────────────────────
st.markdown("""
<div class="section">
  <div class="section-label">✦ A Letter of Gratitude</div>
  <h2 class="section-heading"> Wise Father, Loving Husband, Devoted Son, Visionary, Chimaobi Ezeibe!</h2>
  <p class="section-body">
    Every milestone we've reached, every laugh we've shared, every lesson we've learned —
    you've been there. Not just as a father, but as a teacher, a protector, and our spiritual visionary. 
    <br><br>
    This page is a small token of the enormous love your family and friends have for you.
Know that every message is a reflection of the countless ways you've touched our lives. We celebrate you today, and every day.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ── MILESTONE TIMELINE ────────────────────────────────────────────────────────
st.markdown("""
<div class="section">
  <div class="section-label">✦ A Life Well Lived</div>
  <h2 class="section-heading">Milestones &amp; Memories</h2>
""", unsafe_allow_html=True)

# Editable timeline — stored in session state
default_timeline = [
    {"year": "The Beginning", "emoji": "🌟", "title": "Born to Change Lives",
     "desc": "The world got a little brighter the day you arrived."},
    {"year": "The Early Years", "emoji": "📚", "title": "A Hunger for Knowledge",
     "desc": "You worked hard, studied harder, and always pushed forward."},
    {"year": "A New Chapter", "emoji": "💍", "title": "Built a Family",
     "desc": "You chose love, and love gave you everything in return."},
    {"year": "Every Day", "emoji": "🏡", "title": "The Pillar of Our Home",
     "desc": "Through every season, you showed up — steady, warm, and unwavering."},
    {"year": "Today", "emoji": "🎂", "title": "We Celebrate You",
     "desc": "Because you deserve every bit of joy you've given us, and so much more."},
]

if "timeline" not in st.session_state:
    st.session_state.timeline = default_timeline

tl_html = '<div class="timeline">'
for item in st.session_state.timeline:
    tl_html += f"""
    <div class="tl-item">
      <div class="tl-dot">{item['emoji']}</div>
      <div class="tl-content">
        <div class="tl-year">{item['year']}</div>
        <div class="tl-title">{item['title']}</div>
        <div class="tl-desc">{item['desc']}</div>
      </div>
    </div>"""
tl_html += '</div></div>'
st.markdown(tl_html, unsafe_allow_html=True)

# ── ADD TIMELINE MILESTONE ────────────────────────────────────────────────────
with st.expander("➕  Add a milestone to Dad's story"):
    c1, c2 = st.columns([1, 2])
    tl_year = c1.text_input("Time Period", placeholder="e.g. 1995")
    tl_emoji = c1.text_input("Emoji", placeholder="🎓", max_chars=4)
    tl_title = c2.text_input("Title", placeholder="e.g. Graduated University")
    tl_desc = c2.text_input("Description", placeholder="A short sentence about this milestone…")
    if st.button("Add to Timeline", key="add_tl"):
        if tl_title:
            st.session_state.timeline.append({
                "year": tl_year or "A Special Moment",
                "emoji": tl_emoji or "⭐",
                "title": tl_title,
                "desc": tl_desc,
            })
            st.success("Milestone added! Scroll up to see it.")
            st.rerun()

st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ── MESSAGES SECTION ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section" style="padding-bottom:1rem;">
  <div class="section-label">✦ Words from the Heart</div>
  <h2 class="section-heading">Messages of Love</h2>
  <p class="section-body">Every person who loves you has something to say. Here they are.</p>
""", unsafe_allow_html=True)

# Display cards
messages = st.session_state.messages
if messages:
    cards_html = '<div class="cards-grid">'
    for i, msg in enumerate(messages):
        cards_html += f"""
        <div class="msg-card">
          <div class="msg-author">{msg['name']} <span class="msg-relation">— {msg.get('relation','')}</span></div>
          <p class="msg-text">{msg['message']}</p>
          <div class="msg-date">{msg.get('date','')}</div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="font-family:'DM Sans',sans-serif; color:rgba(232,197,160,0.4); font-style:italic; text-align:center; padding:3rem 0;">
      No messages yet — be the first to leave one below 💛
    </p>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

# ── ADD MESSAGE FORM ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section" style="padding-top:3rem;">
  <div class="section-label">✦ Your Turn</div>
  <h2 class="section-heading">Leave a Message for Dad</h2>
  <p class="section-body" style="margin-bottom:2rem;">
    Share a memory, a wish, or simply what he means to you.
  </p>
</div>
""", unsafe_allow_html=True)

with st.form("message_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name *", placeholder="e.g. Sarah")
        relation = st.selectbox("Your Relationship to Dad", [
            "Son", "Daughter", "Wife / Partner", "Sibling",
            "Friend", "Colleague", "Grandchild", "Other"
        ])
    with col2:
        st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    message = st.text_area(
        "Your Message *",
        placeholder="Write from the heart… there's no wrong thing to say.",
        height=140
    )

    submitted = st.form_submit_button("💛  Send My Love")

    if submitted:
        if name.strip() and message.strip():
            new_msg = {
                "name": name.strip(),
                "relation": relation,
                "message": message.strip(),
                "date": datetime.now().strftime("%B %d, %Y"),
                "id": random.randint(10000, 99999),
            }
            st.session_state.messages.append(new_msg)
            save_messages(st.session_state.messages)
            st.success(f"Thank you, {name}! Your message has been added 💛")
            st.rerun()
        else:
            st.warning("Please fill in your name and a message.")

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="gold-line"></div>
<div class="footer">
  Made with love — for the man who makes everything possible 🎂
</div>
""", unsafe_allow_html=True)