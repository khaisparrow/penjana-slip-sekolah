import streamlit as st
import pandas as pd
from jinja2 import Template
from weasyprint import HTML
import io
import zipfile

st.title("Sistem Penjana Slip Peperiksaan 🏫")

uploaded_file = st.file_uploader("Muat naik fail Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if st.button("Jana Slip & Muat Turun"):
        # Kita guna buffer untuk simpan fail zip dalam memori
        zip_buffer = io.BytesIO()
        
        with open("template.html", "r") as f:
            template = Template(f.read())

        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            for index, row in df.iterrows():
                html_out = template.render(
                    nama=row['Nama'], 
                    kelas=row['Kelas'], 
                    ask=row['ASK'], 
                    rbt=row['RBT']
                )
                
                # Jana PDF dalam memori (BytesIO)
                pdf_buffer = io.BytesIO()
                HTML(string=html_out).write_pdf(pdf_buffer)
                
                # Masukkan PDF ke dalam fail zip
                zf.writestr(f"Slip_{row['Nama']}.pdf", pdf_buffer.getvalue())
        
        # Sediakan butang untuk download zip
        st.download_button(
            label="Klik untuk Muat Turun Semua Slip (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="Semua_Slip.zip",
            mime="application/zip"
        )
        st.success("Slip sedia untuk dimuat turun!")
