import streamlit as st
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
import io
import zipfile
import os

st.title("Sistem Penjana Slip Peperiksaan 🏫")

uploaded_file = st.file_uploader("Muat naik fail Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # --- PROSES PEMBERSIHAN DATA ---
    # 1. Ganti sel kosong (NaN) dengan tanda sengkang (-)
    df = df.fillna("-")
    
    # 2. Buang titik perpuluhan (.0) supaya nombor nampak bulat
    df = df.astype(str).replace(r'\.0$', '', regex=True)
    
    st.write("Pratonton Data Murid:", df.head())

    if st.button("Jana Slip & Muat Turun"):
        zip_buffer = io.BytesIO()
        
        # --- CARI LOKASI FAIL TEMPLATE ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "template.html")
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = Template(f.read())

        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            for index, row in df.iterrows():
                # --- GABUNGKAN DATA EXCEL KE DALAM HTML ---
                html_out = template.render(
                    nama=row['Nama'], 
                    kelas=row['Kelas'], 
                    rbt=row['RBT'],
                    ask=row['ASK'],
                    sejarah=row['Sejarah'],
                    geografi=row['Geografi'],
                    pendidikan_islam=row['Pendidikan Islam'],
                    moral=row['Moral'],
                    seni=row['Seni'],
                    pjpk=row['PJPK']
                )
                
                # --- TUKAR KEPADA PDF DAN MASUK DALAM ZIP ---
                pdf_buffer = io.BytesIO()
                HTML(string=html_out).write_pdf(pdf_buffer)
                
                # Nama fail PDF mengikut nama murid
                zf.writestr(f"Slip_{row['Nama']}.pdf", pdf_buffer.getvalue())
        
        # --- BUTANG MUAT TURUN ---
        st.download_button(
            label="Klik untuk Muat Turun Semua Slip (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="Semua_Slip.zip",
            mime="application/zip"
        )
        st.success("Slip berjaya dijana! Sila klik butang di atas untuk muat turun.")
