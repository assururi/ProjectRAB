
from PIL import Image
import io
import streamlit as st
import pandas as pd

# ========== LOGIN SECTION ==========
# Sesi pengguna
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Data akun (bisa kamu ganti nanti)
VALID_USERS = {
    "admin": "admin123",
    "plnuser": "pln2024"
}

def login():
    st.title("Login Dashboard")
    with st.form("login_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password").strip()
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.success("Login berhasil. Silakan lanjut.")
                st.rerun()
            else:
                st.error("Username atau password salah")

if not st.session_state.logged_in:
    login()
    st.stop()

# Tombol logout di sidebar jika sudah login
with st.sidebar:
    st.image("/content/drive/MyDrive/Bagian_Gardu/Logo_PLN.png", width=120)  
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
# ========== END LOGIN ==========

# ----------------------------
# KONFIGURASI DASHBOARD
# ----------------------------
st.set_page_config(layout="wide", page_title="Dashboard RAB Gardu", page_icon="⚡")
st.title("Dashboard Perencanaan RAB Beserta Visualisasi")

# ----------------------------
# DATA HARGA & GAMBAR PER GARDU
# ----------------------------
gardu_data = {
    "Gardu Tembok": {
        "material": {
            "Isolator Tumpu 20 kV": 50000,
            "Lightning Arrester": 75000,
            "Trafo 100 kVA": 5000000,

        },
        "image": "/content/drive/MyDrive/Bagian_Gardu/GarduTembok/StukturGarduTembok.JPG"
    },
    "Gardu Cantol": {
        "material": {
            "Pasang TM - 1 B/H ( TIANG TUMPU )":  105620,
            "Trafo 160 kVA": 6500000,
            "Arester + Jumper": 46824,
            "Cut Out + Jumper":  46824,
            "Pasang Cover Arrester":  10498,
            "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol":  446693,
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 70mm2":  69000,
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 240mm2":  238000,
            "Pembuatan Nama dan logo gardu": 48887,
            "Penomoran Tiang TM":  13888,
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": 72126,
            "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat":  163122,
            "Pembuatan pondasi gardu Cantol":  1894660,
            "Pasang rangka gardu Cantol":  350124,
            "Pemasangan Panel PHB-TR": 85470000,
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL":  59845,
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir":  5572770,


        },
        "image": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/StrukturGarduCantol.jpg"
    },
    "Gardu Portal": {
        "material": {
            "Pasang TM - 1 B/H ( TIANG TUMPU )":  105620,
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT":  72126,
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL":  119690,
            "Penomoran Tiang TM":  13888,
            "Pasang rangka gardu Portal":  525186,
            "Pemasangan hardware, isolator, pipa, PGTM/TR Portal":  1026850,
            "Pasang trafo 200 - 250 kVA": 795390,
            "Pasang Arrester + Jumper": 46824,
            "Pasang Cut Out + Jumper":  46824,
            "Pasang Cover Arrester":  10498,
            "Pembuatan pondasi gardu Portal": 3940092,
            "Pembuatan Nama dan logo gardu": 48887,
            "Pemasangan Panel PHB-TR": 85470000,
            "Pasang Pentanahan Ganda TM Gardu Portal":  365715,
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir":  5572770,
        },
        "image": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Full lengkap GP.drawio.png"
    },
    "Gardu Garpor": {
        "material dan jasa": {
            "Pasang Trafo 200 - 250 kVA": 795390,
            "Pasang rangka gardu Portal": 525186,
            "Pasang Arrester + Jumper": 46824,
            "Pasang Cover Arrester": 10485,
        },
        "image": "/content/drive/MyDrive/Bagian_Gardu/GarduGarpor/StrukturGarduGarpor.jpg"
    }
}

gambat_material_per_gardu = {
    "Gardu Tembok": {
        "Isolator Tumpu 20 kV": "path_image",
        "Lightning Arrester": "path_iamge",
        "Trafo 100 kVA": "path_image",
    },
    "Gardu Cantol": {
        "Pasang TM - 1 B/H ( TIANG TUMPU )":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-tiang tumpu GC.png",
        "Trafo 160 kVA": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Trafo GC.png",
        "Arester + Jumper": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Arrester GC.png",
        "Cut Out + Jumper":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-cut out GC.png",
        "Pasang Cover Arrester":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-cover arrester GC.png",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-isolator GC.png",
        "CABLE PWR ACC;CABLE SHOE CU ID 1H 70mm2": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-kabel arrester-utama GC.png",
        "CABLE PWR ACC;CABLE SHOE CU ID 1H 240mm2": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-kabel fasa GC.png",
        "Pembuatan Nama dan logo gardu": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Nama dan logo GC.png",
        "Penomoran Tiang TM":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-nomor gardu GC.png",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Penghalang panjat GC.png",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Pentanahan GC.png",
        "Pembuatan pondasi gardu Cantol":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Pondasi GC.png",
        "Pasang rangka gardu Cantol":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Rangka gardu GC.png",
        "Pemasangan Panel PHB-TR": "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-PHBTR GC.png",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-tanda kilat kecil GC.png",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir":  "/content/drive/MyDrive/Bagian_Gardu/GarduCantol/GARDU CANTOL-Tiang GC.png",
    },
    "Gardu Portal": {
        "Pasang TM - 1 B/H ( TIANG TUMPU )": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Connector(2) GP.drawio.png",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Penghalang Panjat GP.drawio.png",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Tanda Kilat Kecil GP.drawio.png",
        "Penomoran Tiang TM": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Penomoran Tiang GP.drawio.png",
        "Pasang rangka gardu Portal": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Rangka Gardu GP.drawio.png",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Portal": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Jaringan TR & Pipa GP.drawio.png",
        "Pasang trafo 200 - 250 kVA": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Trafo GP.drawio.png",
        "Pasang Arrester + Jumper": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Arrester GP.drawio.png",
        "Pasang Cut Out + Jumper": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-FCO GP.drawio.png",
        "Pasang Cover Arrester": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Cover Arrester GP.drawio.png",
        "Pembuatan pondasi gardu Portal":"/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-pondasi GP.drawio.png",
        "Pemasangan Panel PHB-TR": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-PHBTR GP.drawio.png",
        "Pembuatan Nama dan logo gardu": "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Nama dan Logo Gardu GP.drawio.png",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir":[
            "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-Tiang KANAN GP.drawio.png",
            "/content/drive/MyDrive/Bagian_Gardu/GarduPortal/GARDU PORTAL-tiang KIRI GP.drawio.png"
        ]

    },
    "Gardu Garpor":{
        "Pasang Trafo 200 - 250 kVA": "path_image",
        "Pasang rangka gardu Portal": "path_image",
        "Pasang Arrester + Jumper": "path_image",
        "Pasang Cover Arrester": "path_image",
    }
}
# Urutan layer agar tampilan tidak tumpang tindih salah
urutan_layer_per_gardu = {
    "Gardu Cantol": [
        "Pembuatan pondasi gardu Cantol",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir",
        "Pasang TM - 1 B/H ( TIANG TUMPU )",
        "Pasang rangka gardu Cantol",
        "Pemasangan Panel PHB-TR",
        "Trafo 160 kVA",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat",
        "Arester + Jumper",
        "Cut Out + Jumper",
        "Pasang Cover Arrester",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol",
        "CABLE PWR ACC;CABLE SHOE CU ID 1H 240mm2",
        "CABLE PWR ACC;CABLE SHOE CU ID 1H 70mm2",
        "Pembuatan Nama dan logo gardu",
        "Penomoran Tiang TM",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL"
    ],
    "Gardu Portal": [
        "Pembuatan pondasi gardu Portal",
        "Pasang rangka gardu Portal",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir",
        "Pasang TM - 1 B/H ( TIANG TUMPU )",      
        "Pemasangan Panel PHB-TR",
        "Pasang trafo 200 - 250 kVA",
        "Pasang Arrester + Jumper",
        "Pasang Cut Out + Jumper",
        "Pasang Cover Arrester",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Portal",
        "Pembuatan Nama dan logo gardu",
        "Penomoran Tiang TM",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL"
    ]
}

# ----------------------------
# PILIH GARDU
# ----------------------------
with st.sidebar:
    st.header("Pilih Tipe Gardu")
    selected_gardu = st.selectbox("Tipe Gardu", list(gardu_data.keys()))
material_dict = gardu_data[selected_gardu]["material"]
image_file = gardu_data[selected_gardu]["image"]

# ----------------------------
# INPUT USER: JUMLAH KEBUTUHAN
# ----------------------------
col_input, col_vis = st.columns([1.2, 1])
with col_input:
    st.markdown("### Input Kebutuhan Material")
    
    # Buat DataFrame awal
    df_input = pd.DataFrame({
        "NAMA MATERIAL": list(material_dict.keys()),
        "KEBUTUHAN": [0] * len(material_dict)
    })
    harga_satuan_dict = material_dict

    # Tampilkan tabel input editable
    edited_df = st.data_editor(
        df_input,
        use_container_width=True,
        column_config={
            "KEBUTUHAN": st.column_config.NumberColumn("KEBUTUHAN", min_value=0, step=1),
            "NAMA MATERIAL": st.column_config.TextColumn("NAMA MATERIAL", disabled=True)
        },
        hide_index=True
    )

# ----------------------------
# VISUALISASI DINAMIS BERDASARKAN JUMLAH
# ----------------------------
with col_vis:
    st.subheader("Visualisasi Komponen Sesuai Kebutuhan")

    # Mapping nama material ke file gambar
    gambar_material = gambat_material_per_gardu.get(selected_gardu, {})
    urutan_layer = urutan_layer_per_gardu.get(selected_gardu, list(gambar_material.keys()))
    
    canvas_size = (600, 600)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    # Cek apakah semua kebutuhan masih kosong (nol)
    kebutuhan_terisi = edited_df["KEBUTUHAN"].astype(int).sum()

    if kebutuhan_terisi == 0:
        st.warning("Silakan masukkan jumlah kebutuhan pada tabel untuk melihat visualisasi komponen gardu.")
    else:

        for nama in urutan_layer:
            if nama in gambar_material:
                jumlah = edited_df[edited_df["NAMA MATERIAL"] == nama]["KEBUTUHAN"].values[0]
                path_gambar = gambar_material[nama]

                if isinstance(path_gambar, str):
                    path_gambar = [path_gambar]
                gambar_terpakai = path_gambar[:jumlah]

                for path in gambar_terpakai:
                    try:
                        layer = Image.open(path).convert("RGBA").resize(canvas_size)
                        canvas = Image.alpha_composite(canvas, layer)
                    except Exception as e:
                        st.warning(f"Gagal load gambar: {nama} ({path}) → {e}")

        if canvas:
            buf = io.BytesIO()
            canvas.save(buf, format="PNG")
            st.image(buf.getvalue(), caption=f"Rekonstruksi Gardu {selected_gardu}", width=400)

edited_df["HARGA SATUAN"] = edited_df["NAMA MATERIAL"].map(harga_satuan_dict)
edited_df["TOTAL HARGA"] = edited_df["KEBUTUHAN"] * edited_df["HARGA SATUAN"]

# ----------------------------
# HITUNG TOTAL
# ----------------------------
edited_df["TOTAL HARGA"] = edited_df["KEBUTUHAN"] * edited_df["HARGA SATUAN"]
df = edited_df.copy()
total_anggaran = df["TOTAL HARGA"].sum()

# ----------------------------
# TAMPILKAN HASIL
# ----------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Tabel RAB")
    st.dataframe(df, use_container_width=True)

    st.markdown(f"### **Total Anggaran: Rp {total_anggaran:,.0f}**")

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download Laporan RAB",
        data=csv,
        file_name=f"laporan_rab_{selected_gardu.replace(' ', '_').lower()}.csv",
        mime='text/csv'
    )

with col2:
    st.markdown("### Visualisasi Gardu Lengkap")
    st.image(image_file, caption=f"Diagram {selected_gardu}", width=350)




