from openpyxl import load_workbook
from io import BytesIO
from PIL import Image
import io
import streamlit as st
import pandas as pd

# =========================
# KONFIGURASI DASAR
# =========================
st.set_page_config(layout="wide", page_title="Dashboard RAB Gardu", page_icon="Bagian_Gardu/Logo_PLN.png")

# =========================
# ========== LOGIN =========
# =========================
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

with st.sidebar:
    st.image("Bagian_Gardu/Logo_PLN.png", width=120)
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# DATA HARGA & GAMBAR
# =========================
st.title("Dashboard Perencanaan RAB Beserta Visualisasi")

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
            "Pasang TM - 1 B/H ( TIANG TUMPU )": 105620,
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": 72126,
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": 59845,
            "Penomoran Tiang TM": 13888,
            "Pasang rangka gardu Cantol": 350124,
            "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol": 446693,
            "Pasang trafo 200 - 250 kVA": 7953990,
            "Pasang Arrester + Jumper": 46824,
            "Pasang Cut Out + Jumper": 46824,
            "Pasang Cover Arrester": 10498,
            "Pasang Cover Cut Out": 10498,
            "Pasang Cover Bushing Trafo": 19498,
            "Pembuatan pondasi gardu Cantol": 1894660,
            "Pembuatan Nama dan logo gardu": 48887,
            "Pasang Pentanahan TM Gardu Cantol": 228572,
            "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": 163122,
            "Pasang Kbl Single Core 20 kV lengkap Pipa Pelindung": 320891,
            "Tagging GPS": 3437,
            "Dokumentasi / Foto 1 album": 78539,
            "Biaya Ongkos Angkut material Pick Up": 268257,
            "Biaya Gambar Pelaksanaan Pada Millar / Kalkir 60 mikron A1 (Blue Print 4 lbr)": 288232,
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": 5572770,
            "CONDUCTOR;AAAC-S;70mm2": 15610,
            "CABLE PWR;N2XSY 1x35mm2;20kV;UG": 132390,
            "CABLE PWR;NYY;1X70mm2;0,6/1kV;OH": 117380,
            "CABLE PWR;NYY;1X120mm2;0,6/1kV;OH": 428735,
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 70mm2": 69000,
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 240mm2": 238000,
            "CABLE PWR ACC;CABLE SHOE AL ID 1H 70mm2": 62600,
            "CUT 20kV;24kV;R-VO;7-B;70-150mm2;PRS": 34500,
            "TRA DIS;24kV;400/230;25kVA;DYNS;00": 82638,
            "LVSDB;DIST;3P;400V;250A;2Line;OH": 14408190,
            "Line Post;24kV;12.5kN;Polymer SIR": 219040,
            "Insulated Top Ties": 69500,
            "LA;24-24kV;1kA;Polymer": 606990,
            "CUT OUT;24kV;100A;Polymer-125kV": 1164370.00
        },
         "image": "Bagian_Gardu/GarduCantolRevisi/StrukturGarduCantol.jpg"
    },
    "Gardu Portal": {
        "material": {
            "Pasang TM - 1 B/H ( TIANG TUMPU )": 105620,
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": 72126,
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": 59845,
            "Penomoran Tiang TM": 13888,
            "Pasang rangka gardu Portal": 525186,
            "Pemasangan hardware, isolator, pipa, PGTM/TR Portal": 1026850,
            "Pasang trafo 200 - 250 kVA": 7953990,
            "Pasang Arrester + Jumper": 46824,
            "Pasang Cut Out + Jumper": 46824,
            "Pasang Cover Arrester": 10498,
            "Pasang Cover Cut Out": 10498,
            "Pasang Cover Bushing Trafo": 19498,
            "Pembuatan pondasi gardu Portal": 3948992,
            "Pembuatan Nama dan logo gardu": 48887,
            "Pasang Pentanahan Ganda TM Gardu Portal": 365715,
            "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": 163122,
            "Tagging GPS": 3437,
            "Dokumentasi / Foto 1 album": 78539,
            "Biaya Ongkos Angkut material Pick Up": 268257,
            "Biaya Gambar Pelaksanaan Pada Millar / Kalkir 60 mikron A1 (Blue Print 4 lbr)": 288232,
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": 5572770,

            # Kabel
            "CONDUCTOR;AAAC-S;150mm2": 27240,
            "CONDUCTOR;AAAC-S;70mm2": 15610,
            "CABLE PWR;N2XSY 1x70mm2;20kV;UG": 117380,
            "CABLE PWR;NYY;1X240mm2;0,6/1kV;OH": 428735,

            # Konektor
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 70mm2": 69000,
            "CABLE PWR ACC;CABLE SHOE CU ID 1H 240mm2": 238000,
            "CABLE PWR ACC;CABLE SHOE AL ID 1H 70mm2": 62600,
            "CONN;20kV;24kV;H-35-70/70-150mm2;PRS": 34500,

            # Perlengkapan gardu
            "TRF DIS;24kV;400/230;25kVA;DYNS;00": 82638,
            "LVSDB;DIST;3P;400V;630A;4Line;OD": 28466360,

            # Perlengkapan jaringan
            "Line Post;24kV;12.5kN;Polymer SIR": 219040,
            "INSULATED TOP TIES": 69500,

            # Pelindung/pengontrol
            "LA;24-24kV;1kA;Polymer": 606990,
            "CUT OUT;24kV;6-100A;POLYMER-125kV": 1164370,
            "CUT OUT ACC;FUSE LINK 26 kV 8A": 19980
        },
        "image": "Bagian_Gardu/GarduPortalRevisi/GARDU PORTAL-Full lengkap GP.drawio.png"
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
        "Pasang TM - 1 B/H ( TIANG TUMPU )": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-TM - 1 B_H ( TIANG TUMPU ) GC.png",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-PENGHALANG PANJAT GC.png",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-TANDA KILAT KECIL GC.png",
        "Penomoran Tiang TM": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Penomoran Tiang TM GC.png",
        "Pasang rangka gardu Cantol": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Rangka gardu cantol GC.png",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-hardware, isolator, pipa, PGTM_TR Cantol GC.png",
        "Pasang trafo 200 - 250 kVA": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-trafo 200 - 250 kVA GC(1).png",
        "Pasang Arrester + Jumper": [
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Arrester + Jumper 1 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Arrester + Jumper 2 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Arrester + Jumper 3 GC.png"
        ],
        "Pasang Cut Out + Jumper": [
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL- Cut Out + Jumper 1 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL- Cut Out + Jumper 2 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL- Cut Out + Jumper 3 GC.png"
        ],
        "Pasang Cover Bushing Trafo": [
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Cover Bushing Trafo 1 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Cover Bushing Trafo 2 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Cover Bushing Trafo 3 GC.png"
        ],
        "Pembuatan pondasi gardu Cantol": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Pondasi gardu cantol GC.png",
        "Pembuatan Nama dan logo gardu": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Nama dan logo GC.png",
        "Pasang Pentanahan TM Gardu Cantol": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Pentanahan TM Gardu Cantol GC.png",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": [
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat 1 GC.png",
            "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat 2 GC.png",
        ],
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": "Bagian_Gardu/GarduCantolRevisi/Copy of GARDU CANTOL-Tiang GC.png"
    },
    "Gardu Portal":{
        "Pasang TM - 1 B/H ( TIANG TUMPU )": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-TM - 1 B_H ( TIANG TUMPU ) 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-TM - 1 B_H ( TIANG TUMPU ) 2 GP.drawio.png"
        ],
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Penghalang Panjat 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Penghalang Panjat 2 GP.drawio.png"
        ],
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Tanda Kilat Kecil 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Tanda Kilat Kecil 2 GP.drawio.png"
        ],
        "Penomoran Tiang TM": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Penomoran Tiang 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Penomoran Tiang 2 GP.drawio.png"
        ],
        "Pasang rangka gardu Portal": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Rangka Gardu Portal GP.drawio.png",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Portal": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Hardware, isolator, pipa, PGTM_TR Portal GP.drawio.png",
        "Pasang trafo 200 - 250 kVA": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Trafo 200 - 250 kVA GP.drawio.png",
        "Pasang Arrester + Jumper": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Arrester + Jumper 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Arrester + Jumper 2 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Arrester + Jumper 3 GP.drawio.png"
        ],
        "Pasang Cut Out + Jumper": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cut Out + Jumper 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cut Out + Jumper 2 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cut Out + Jumper 3 GP.drawio.png"
        ],
        "Pasang Cover Bushing Trafo": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cover Bushing Trafo 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cover Bushing Trafo 2 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Cover Bushing Trafo 3 GP.drawio.png"
        ],
        "Pembuatan pondasi gardu Portal": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-pondasi gardu Portal GP.drawio.png",
        "Pembuatan Nama dan logo gardu": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Nama dan Logo Gardu GP.drawio.png",
        "Pasang Pentanahan Ganda TM Gardu Portal": "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Pentanahan Ganda TM Gardu Portal GP.drawio.png",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat 2 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat 4 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat GP.drawio.png"
        ],
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": [
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-TIANG BETON BULAT 12m_350 daN (terpasang) + Lansir 1 GP.drawio.png",
            "Bagian_Gardu/GarduPortalRevisi/Copy of GARDU PORTAL-TIANG BETON BULAT 12m_350 daN (terpasang) + Lansir 2 GP.drawio.png"
        ]
    },
    "Gardu Garpor":{
        "Pasang Trafo 200 - 250 kVA": "path_image",
        "Pasang rangka gardu Portal": "path_image",
        "Pasang Arrester + Jumper": "path_image",
        "Pasang Cover Arrester": "path_image",
    }
}
# Jumlah maksimal per material untuk Gardu Portal
pilihan_jumlah_per_material = {
    "Gardu Tembok": {
        "material": {
            "Isolator Tumpu 20 kV": 50000,
            "Lightning Arrester": 75000,
            "Trafo 100 kVA": 5000000,
        }
    },
    "Gardu Cantol": {
        "material": {
            "Pasang TM - 1 B/H ( TIANG TUMPU )": [0,1],
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": [0,1],
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": [0,1],
            "Penomoran Tiang TM": [0,1],
            "Pasang rangka gardu Cantol": [0,1],
            "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol": [0,1],
            "Pasang trafo 200 - 250 kVA": [0,1],
            "Pasang Arrester + Jumper": [0,1,2,3],
            "Pasang Cut Out + Jumper": [0,1,2,3],
            "Pasang Cover Arrester": [0,1,2,3],
            "Pasang Cover Cut Out": [0,1,2,3],
            "Pasang Cover Bushing Trafo": [0,1,2,3],
            "Pembuatan pondasi gardu Cantol": [0,1],
            "Pembuatan Nama dan logo gardu": [0,1],
            "Pasang Pentanahan TM Gardu Cantol": [0,1],
            "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": [0,1],
            "Pasang Kbl Single Core 20 kV lengkap Pipa Pelindung": [0,1,2],
            "Tagging GPS": [0,1],
            "Dokumentasi / Foto 1 album": [0,1],
            "Biaya Ongkos Angkut material Pick Up": [0,1],
            "Biaya Gambar Pelaksanaan Pada Millar / Kalkir 60 mikron A1 (Blue Print 4 lbr)": [0,1],
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": [0,1],
            "CUT 20kV;24kV;R-VO;7-B;70-150mm2;PRS": [0,1],
            "TRA DIS;24kV;400/230;25kVA;DYNS;00": [0,1],
            "LVSDB;DIST;3P;400V;250A;2Line;OH": [0,1],
            "Line Post;24kV;12.5kN;Polymer SIR": [0,1,2,3],
            "Insulated Top Ties": [0,1,2,3],
            "LA;24-24kV;1kA;Polymer": [0,1,2,3],
            "CUT OUT;24kV;100A;Polymer-125kV": [0,1,2,3]
        }
    },
    "Gardu Portal": {
        "material": {
            "Pasang TM - 1 B/H ( TIANG TUMPU )": [0,1,2],
            "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT": [0,1,2],
            "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL": [0,1,2],
            "Penomoran Tiang TM": [0,1,2],
            "Pasang rangka gardu Portal": [0,1],
            "Pemasangan hardware, isolator, pipa, PGTM/TR Portal": [0,1],
            "Pasang trafo 200 - 250 kVA": [0,1],
            "Pasang Arrester + Jumper": [0,1,2,3],
            "Pasang Cut Out + Jumper": [0,1,2,3],
            "Pasang Cover Arrester": [0,1,2,3],
            "Pasang Cover Cut Out": [0,1,2,3],
            "Pasang Cover Bushing Trafo": [0,1,2,3],
            "Pembuatan pondasi gardu Portal": [0,1],
            "Pembuatan Nama dan logo gardu": [0,1],
            "Pasang Pentanahan Ganda TM Gardu Portal": [0,1],
            "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat": [0,1,2,3,4],
            "Tagging GPS": [0,1],
            "Dokumentasi / Foto 1 album": [0,1],
            "Biaya Ongkos Angkut material Pick Up": [0,1],
            "Biaya Gambar Pelaksanaan Pada Millar / Kalkir 60 mikron A1 (Blue Print 4 lbr)": [0,1],
            "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir": [0,1,2],

            # Perlengkapan gardu
            "TRF DIS;24kV;400/230;25kVA;DYNS;00": [0,1],
            "LVSDB;DIST;3P;400V;630A;4Line;OD": [0,1],

            # Perlengkapan jaringan
            "Line Post;24kV;12.5kN;Polymer SIR": [0,1,2,3,4,5,6],
            "INSULATED TOP TIES": [0,1,2,3,4,5,6],

            # Pelindung/pengontrol
            "LA;24-24kV;1kA;Polymer": [0,1,2,3],
            "CUT OUT;24kV;6-100A;POLYMER-125kV": [0,1,2,3],
            "CUT OUT ACC;FUSE LINK 26 kV 8A": [19980]
        }
    },
    "Gardu Garpor": {
        "material dan jasa": {
            "Pasang Trafo 200 - 250 kVA": 795390,
            "Pasang rangka gardu Portal": 525186,
            "Pasang Arrester + Jumper": 46824,
            "Pasang Cover Arrester": 10485,
        }
    }
}


# Urutan layer agar tampilan tidak tumpang tindih salah
urutan_layer_per_gardu = {
    "Gardu Cantol": [
        "Pembuatan pondasi gardu Cantol",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT",
        "Pasang rangka gardu Cantol",
        "Pasang TM - 1 B/H ( TIANG TUMPU )",
        "Pasang Pentanahan TM Gardu Cantol",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Cantol",
        "Pasang trafo 200 - 250 kVA",
        "Pasang Arrester + Jumper",
        "Pasang Cut Out + Jumper",
        "Pasang Cover Bushing Trafo",
        "Pembuatan Nama dan logo gardu",
        "Penomoran Tiang TM",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL"
    ],
    "Gardu Portal": [
        "Pembuatan pondasi gardu Portal",
        "Pasang rangka gardu Portal",
        "TIANG BETON BULAT 12m/350 daN (terpasang) + Lansir",
        "Pasang Kabel Naik TR & Pipa Pelindung untuk Jurusan Baru lengkap perbaikan Rabat",
        "Pasang TM - 1 B/H ( TIANG TUMPU )",
        "Pemasangan hardware, isolator, pipa, PGTM/TR Portal",
        "Pasang trafo 200 - 250 kVA",
        "Pasang Arrester + Jumper",
        "Pasang Cut Out + Jumper",
        "Pasang Cover Arrester",
        "Pasang Cover Cut Out",
        "Pasang Cover Bushing Trafo",
        "Pasang Pentanahan Ganda TM Gardu Portal",
        "Pembuatan Nama dan logo gardu",
        "Penomoran Tiang TM",
        "PENGADAAN DAN PEMASANGAN PENGHALANG PANJAT",
        "PENGADAAN DAN PEMASANGAN TANDA KILAT KECIL"
    ]
}
# =========================
# INISIALISASI & TOMBOL RESET
# =========================

if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False

def reset_all():
    st.session_state.df_dropdown_state["KEBUTUHAN"] = 0
    st.session_state.df_numeric_state["KEBUTUHAN"] = 0
if st.button("Reset Kebutuhan"):
        st.session_state.reset_trigger = True
        st.rerun()

# =========================
# PILIH GARDU
# =========================
with st.sidebar:
    st.header("Pilih Tipe Gardu")
    selected_gardu = st.selectbox("Tipe Gardu", list(gardu_data.keys()))

# Ambil dict material (handle kasus "Gardu Garpor" yang pakai key berbeda)
material_key = "material" if "material" in gardu_data[selected_gardu] else "material dan jasa"
material_dict = gardu_data[selected_gardu][material_key]
image_file = gardu_data[selected_gardu]["image"]

# =========================
# LOGIKA PEMISAHAN INPUT
# =========================
def is_length_based(item_name: str) -> bool:
    keywords = ["CABLE", "CONDUCTOR", "N2XSY", "NYY", "AAAC"]
    upper_name = item_name.upper()
    return any(k in upper_name for k in keywords)

# Buat DataFrame awal
df_input = pd.DataFrame({
    "NAMA MATERIAL": list(material_dict.keys()),
    "KEBUTUHAN": [0] * len(material_dict)
})

# Bagi material berdasarkan jenis input
dropdown_items = [m for m in df_input["NAMA MATERIAL"] if not is_length_based(m)]
numeric_items  = [m for m in df_input["NAMA MATERIAL"] if is_length_based(m)]


df_dropdown = pd.DataFrame({"NAMA MATERIAL": dropdown_items, "KEBUTUHAN": [0] * len(dropdown_items)})
df_numeric  = pd.DataFrame({"NAMA MATERIAL": numeric_items,  "KEBUTUHAN": [0] * len(numeric_items)})


# Inisialisasi state untuk menyimpan input
if "df_dropdown_state" not in st.session_state:
    st.session_state.df_dropdown_state = df_dropdown.copy()

if "df_numeric_state" not in st.session_state:
    st.session_state.df_numeric_state = df_numeric.copy()

if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False

# Pilihan dropdown sesuai gardu
if selected_gardu == "Gardu Portal":
    pilihan_jumlah = [0, 1, 2, 3, 4]
elif selected_gardu == "Gardu Cantol":
    pilihan_jumlah = [0, 1, 2, 3]
else:
    pilihan_jumlah = [0, 1]  # default untuk tipe lain



# =========================
# INPUT USER
# =========================
col_input, col_vis = st.columns([1.2, 1])
with col_input:
    st.markdown("### Input Kebutuhan Material")
    if st.session_state.reset_trigger:
            st.session_state.df_dropdown_state["KEBUTUHAN"] = 0
            st.session_state.df_numeric_state["KEBUTUHAN"] = 0
            st.session_state.reset_trigger = False
    if len(df_dropdown):
        st.markdown("**Jenis Pekerjaan / Material (Tabel Volume Pemborong)**")
        edited_dropdown = st.data_editor(
            df_dropdown,
            use_container_width=True,
            column_config={
                "KEBUTUHAN": st.column_config.SelectboxColumn(
                "KEBUTUHAN", options=pilihan_jumlah, default=0
                ),
                "NAMA MATERIAL": st.column_config.TextColumn("NAMA MATERIAL", disabled=True)
            },
            hide_index=True
        )
    else:
        edited_dropdown = pd.DataFrame(columns=df_dropdown.columns)
    if len(df_numeric):            
        st.markdown("Material Kabel / Konduktor (Tabel Volume PLN )")
        edited_numeric = st.data_editor(
                df_numeric,
                use_container_width=True,
                column_config={
                    "KEBUTUHAN": st.column_config.NumberColumn("KEBUTUHAN", min_value=0, step=1),
                    "NAMA MATERIAL": st.column_config.TextColumn("NAMA MATERIAL", disabled=True)
                },
            hide_index=True
        )
    else:
        edited_numeric = pd.DataFrame(columns=df_numeric.columns)

    # Gabungkan kembali & urut sesuai df_input awal
    edited_df = pd.concat([edited_dropdown, edited_numeric], ignore_index=True)
    edited_df = edited_df.set_index("NAMA MATERIAL").reindex(df_input["NAMA MATERIAL"]).reset_index()
    

# =========================
# VISUALISASI DINAMIS
# =========================
with col_vis:
    st.subheader("Visualisasi Komponen Sesuai Kebutuhan")

    gambar_material = gambat_material_per_gardu.get(selected_gardu, {})
    urutan_layer = urutan_layer_per_gardu.get(selected_gardu, list(gambar_material.keys()))

    canvas_size = (600, 600)
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    kebutuhan_terisi = pd.to_numeric(edited_df["KEBUTUHAN"], errors="coerce").fillna(0).astype(int).sum()

    if kebutuhan_terisi == 0:
        st.warning("Silakan masukkan jumlah kebutuhan pada tabel untuk melihat visualisasi komponen gardu.")
    else:
        for nama in urutan_layer:
            if nama in gambar_material:
                jumlah = int(edited_df.loc[edited_df["NAMA MATERIAL"] == nama, "KEBUTUHAN"].fillna(0).values[0])
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

import openpyxl
from io import BytesIO

# Load template Excel dari dictionary atau path lokal
template_path = "Bagian_Gardu/TemplateRAB_Percobaan1.xlsx"  # sesuaikan lokasi jika dari dictionary

# Hitung ulang total harga
edited_df["HARGA SATUAN"] = edited_df["NAMA MATERIAL"].map(material_dict)
edited_df["KEBUTUHAN"] = pd.to_numeric(edited_df["KEBUTUHAN"], errors="coerce").fillna(0)
edited_df["TOTAL HARGA"] = edited_df["KEBUTUHAN"] * edited_df["HARGA SATUAN"]

df = edited_df.copy()
total_anggaran = df["TOTAL HARGA"].sum()
st.write("Isi DataFrame yang akan ditulis:", df)
# =============== #
# TAMBAHKAN KE XLSX
# =============== #
template_path = "Bagian_Gardu/TemplateRAB_Percobaan1.xlsx"
output = BytesIO()

# Load template
wb = load_workbook(template_path)
ws = wb.active

# Mulai menulis dari baris 43
start_row = 43

for i, (_, row) in enumerate(df.iterrows()):
    row_num = start_row + i
    ws[f'D{row_num}'] = str(row["NAMA MATERIAL"])
    ws[f'G{row_num}'] = float(row["KEBUTUHAN"])
    ws[f'I{row_num}'] = float(row["HARGA SATUAN"])
    ws[f'K{row_num}'] = float(row["TOTAL HARGA"])

# Simpan ke BytesIO
wb.save(output)
output.seek(0)  # <-- Penting!

# Tombol Download
st.download_button(
    label="📥 Download Laporan RAB (Excel)",
    data=output,
    file_name=f"laporan_rab_{selected_gardu.replace(' ', '_').lower()}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
# Tampilan DataFrame dan total anggaran
st.markdown("### Tabel RAB")
st.dataframe(df, use_container_width=True)
st.markdown(f"### **Total Anggaran: Rp {total_anggaran:,.0f}**")

with col2:
    st.markdown("### Visualisasi Gardu Lengkap")
    st.image(image_file, caption=f"Diagram {selected_gardu}", width=350)


