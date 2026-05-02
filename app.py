import streamlit as st
import pandas as pd
from jinja2 import Template
from weasyprint import HTML

st.title("Sistem Penjana Slip Peperiksaan 🏫")

# 1. Muat Naik Fail
uploaded_file = st.file_uploader("Muat naik fail Excel markah", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Data Murid:", df.head())

    # 2. Proses Jana PDF
    if st.button("Jana Semua Slip"):
        with open("template.html", "r") as f:
            template_content = f.read()
            template = Template(template_content)

        for index, row in df.iterrows():
            # Masukkan data ke dalam template
            html_out = template.render(
                nama=row['Nama'], 
                kelas=row['Kelas'], 
                ask=row['ASK'], 
                rbt=row['RBT']
            )
            
            # Simpan sebagai PDF
            HTML(string=html_out).write_pdf(f"Slip_{row['Nama']}.pdf")
            
        st.success("Slip berjaya dijana!")
