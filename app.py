import streamlit as st
from google import genai
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="QiTabot - Pembelajaran Maharah Kalam X MA",
    page_icon="🔮",
    layout="centered"
)

# --- CUSTOM CSS ELEGAN: TEMA UTAMA UNGU VIOLET GLAMOR  ---
st.markdown("""
    <style>
    /* 1. Latar Belakang Utama Violet Velvet */
    .stApp {
        background: linear-gradient(135deg, #18051a 0%, #290d2b 50%, #110212 100%);
        background-attachment: fixed;
    }
    
    /* 2. Desain Judul Utama (Glowing Gold & Pearl White) */
    .main-title {
        color: #ffffff; 
        font-family: 'Playfair Display', 'Inter', sans-serif;
        text-align: center;
        font-weight: 900;
        letter-spacing: 1.5px;
        margin-top: 25px;
        margin-bottom: 0px;
        text-shadow: 0px 4px 15px rgba(223, 177, 69, 0.4);
    }
    .sub-title {
        color: #dfb145; /* Emas */
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 35px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    /* 3. Kartu Form Akses Terpusat */
    .luxury-form-container {
        background: rgba(36, 12, 38, 0.8);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(223, 177, 69, 0.2);
        border-top: 5px solid #dfb145;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }

    /* 4. Grid Kotak Fitur Awal (Warna Selaras Violet) */
    .feature-card {
        background: rgba(56, 21, 59, 0.4);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(223, 177, 69, 0.15);
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    .feature-card h3 {
        color: #dfb145 !important;
        font-weight: 700;
        margin-bottom: 8px;
        font-size: 1.15rem;
    }
    .feature-card p {
        color: #e1bee7 !important; /* Ungu pastel cerah agar terbaca */
        font-size: 0.9rem;
        margin-bottom: 0px;
    }
    
    /* 5. FIXING HOVER & KOMPONEN TOMBOL STREAMLIT (ANTI-NYARU) */
    /* Tombol Utama (Buka Akses) */
    div.stButton > button:first-child {
        background-color: #dfb145 !important;
        color: #18051a !important;
        font-weight: bold !important;
        border: 1px solid #dfb145 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #6a1b71 !important; /* Berubah jadi ungu cerah saat dihover */
        color: #ffffff !important;
        border: 1px solid #dfb145 !important;
        box-shadow: 0 0 15px rgba(223, 177, 69, 0.5) !important;
    }
    
    /* Tombol Merah (Tutup Sesi) */
    div.stButton > button[kind="primary"] {
        background-color: #7b1fa2 !important; /* Ungu gelap royal */
        color: #ffffff !important;
        border: 1px solid rgba(223, 177, 69, 0.4) !important;
        border-radius: 10px !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #e91e63 !important; /* Efek tegas saat mau keluar sesi */
        color: #ffffff !important;
        box-shadow: 0 0 15px rgba(233, 30, 99, 0.5) !important;
    }

    /* 6. FIXING INPUT FIELD & DROPDOWN TEXT (KONTRAST TINGGI) */
    input, select, textarea {
        color: #ffffff !important; /* Teks ketikan wajib putih */
        background-color: #240c26 !important; /* Kolom warna ungu tua */
        border: 1px solid rgba(223, 177, 69, 0.3) !important;
    }
    /* Mengubah label teks bawaan menjadi emas */
    label, .stMarkdown p, p {
        color: #ffffff !important;
    }
    span[data-testid="stWidgetLabel"] p {
        color: #dfb145 !important;
        font-weight: 600;
    }
    
    /* Menyembunyikan footer bawaan streamlit agar tidak memutih polos */
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_persona" not in st.session_state:
    st.session_state.current_persona = ""
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

# --- HALAMAN UTAMA APPLICATION ---
st.markdown("<h1 class='main-title'>🔮 QiTabot (كِتَابَات)</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Platform Eksklusif Latihan Maharah Kalam Interaktif — Kelas X MA</p>", unsafe_allow_html=True)

# --- FORM AKSES & PENGATURAN ---
if not st.session_state.logged_in:
    st.markdown("<div class='luxury-form-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top:0; color:#ffffff;'>👑 Akses QiTabot</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.85rem; color: #dfb145; margin-bottom:20px;'>Membentuk Generasi Aliyah Berwawasan Global</p>", unsafe_allow_html=True)
    
    username = st.text_input("Username / Nama Siswa", placeholder="Nama lengkap siswa")
    api_key = st.text_input("Google AI Studio API Key", type="password", placeholder="AIzaSy...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Buka Akses Ruang Belajar ✨", use_container_width=True):
        if username and api_key:
            st.session_state.username = username
            st.session_state.api_key = api_key
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Mohon isi Username dan API Key terlebih dahulu!")
    st.markdown("</div>", unsafe_allow_html=True)

    # Info Kotak Peringatan (Disesuaikan dengan warna Violet Cerah)
    st.markdown("<div style='background-color: rgba(106, 27, 113, 0.3); padding: 12px; border-radius: 10px; border-left: 4px solid #dfb145; color: #ffffff; font-size:0.9rem; margin-bottom:20px;'>💡 <b>Akses Terkunci:</b> Silakan lakukan proses autentikasi di atas untuk mengaktifkan asisten virtual.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h3>💎 High-Class Kalam</h3>
            <p>Simulasi interaksi bahasa Arab tingkat Aliyah untuk mengasah kelancaran.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h3>⚜️ Materi Esensial</h3>
            <p>Eksplorasi mendalam pada pilar utama: At-Ta'aruf, Al-Usroh, dan Al-Mihnah.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <h3>👑 Tatap Muka</h3>
            <p>Dipandu penuh oleh mentor dengan pendekatan koreksi yang lembut dan santun.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # --- TAMPILAN JIKA SUDAH LOGIN ---
    st.markdown(f"<div style='text-align: center; font-size: 1.1rem; color: #ffffff; margin-bottom: 20px;'>Selamat Datang di Sesi Premium, <span style='color: #dfb145; font-weight: bold;'>⚜️ {st.session_state.username}</span></div>", unsafe_allow_html=True)
    
    config_col1, config_col2 = st.columns(2)
    with config_col1:
        ustadz_pilihan = st.selectbox(
            "Pilih Mentor Pembimbing:",
            ["Ustadz Khalid", "Ustadzah Khaulah"]
        )
    with config_col2:
        materi_pilihan = st.selectbox(
            "Pilih Topik Pembelajaran:",
            [
                "At-Ta'aruf (Perkenalan / التعارف)", 
                "Al-Usroh (Kehidupan Keluarga / الأسرة)", 
                "Al-Mihnah (Profesi / المهنة)"
            ]
        )
        
    # Prompt Sistem untuk AI
    gender_pembimbing = "seorang Ustadz laki-laki bernama Ustadz Khalid" if ustadz_pilihan == "Ustadz Khalid" else "seorang Ustadzah perempuan bernama Ustadzah Khaulah"
    
    system_instruction = f"""
    Anda adalah {gender_pembimbing}, seorang guru bahasa Arab yang sangat lemah lembut, sabar, santun, dan penuh kasih sayang dalam mendidik siswa kelas X MA.
    Tugas Anda adalah melatih 'Maharah Kalam' (keterampilan berbicara) siswa bernama {st.session_state.username} mengenai topik: {materi_pilihan}.
    
    Aturan Percakapan:
    1. Selalu gunakan bahasa Arab yang sesuai untuk tingkat MA, sertakan harakat, dan berikan terjemahan bahasa Indonesia di bawahnya.
    2. Berikan koreksi yang sangat lembut jika siswa salah dalam menyusun kalimat atau kosakata.
    3. Ajukan satu pertanyaan pendek di setiap akhir pesan untuk memicu siswa membalas.
    4. Selalu tunjukkan apresiasi seperti 'ممتاز!' atau 'Barakallahu fiik'.
    """

    if st.session_state.current_persona != ustadz_pilihan or st.session_state.current_topic != materi_pilihan:
        st.session_state.current_persona = ustadz_pilihan
        st.session_state.current_topic = materi_pilihan
        
        greeting_msg = f"Assalamu'alaikum wr. wb. {st.session_state.username}. ✨ Kaifa haluk? Saya {ustadz_pilihan} akan menemani kamu mengasah Maharah Kalam tentang *{materi_pilihan}*. Mari kita mulai percakapan kita, silakan sapa saya terlebih dahulu ya!"
        st.session_state.messages = [{"role": "assistant", "content": greeting_msg}]

    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.15);'>", unsafe_allow_html=True)

    # JENDELA OBROLAN CHAT (TAMPIL DI TENGAH)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Obrolan Siswa
    user_input = st.chat_input("Ketik respons bahasa Arab atau Indonesia kamu di sini...")
    
    # TOMBOL TUTUP SESI DI BAWAH TEPAT INPUT CHAT
    st.markdown("<div style='margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)
    if st.button("Tutup Sesi Belajar ❌", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Logika eksekusi jika user mengirim chat input
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # --- KODE LOGIKA API GEMINI ANTI-LAG / AUTO-RETRY (100% UTUH) ---
        try:
            client = genai.Client(api_key=st.session_state.api_key)
            
            full_context = system_instruction + "\n\nBerikut riwayat percakapan:\n"
            for msg in st.session_state.messages:
                full_context += f"{msg['role']}: {msg['content']}\n"
            
            bot_response = ""
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{full_context}\nSiswa mengatakan: {user_input}\nBerikan respons Anda sebagai pengajar:"
                    )
                    bot_response = response.text
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < 2:
                        time.sleep(2)
                        continue
                    else:
                        raise e

            if bot_response:
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.rerun()
            
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi API: {e}. Silakan coba kirim ulang pesan beberapa saat lagi.")
