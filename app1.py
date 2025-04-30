import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from fpdf import FPDF
import os
import tempfile

st.set_page_config(page_title="Limpiar PDF (sin logo)", layout="centered")

st.title("📄 Conversor PDF sin Logos")
st.write("Sube tu archivo PDF y obtendrás un nuevo documento con las páginas como imagen, sin el encabezado (logo).")

uploaded_file = st.file_uploader("🔽 Sube un archivo PDF", type="pdf")

if uploaded_file:
    with st.spinner("Procesando PDF..."):

        # Crear carpeta temporal para imágenes
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = os.path.join(tmp_dir, "input.pdf")
            output_path = os.path.join(tmp_dir, "output.pdf")
            img_dir = os.path.join(tmp_dir, "images")
            os.makedirs(img_dir, exist_ok=True)

            # Guardar el archivo subido
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            # Abrir PDF
            doc = fitz.open(input_path)
            pdf = FPDF(unit="pt")

            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=200)
                img_path = os.path.join(img_dir, f"page_{i+1}.png")
                pix.save(img_path)

                # Recortar logo (parte superior 12%)
                img = Image.open(img_path)
                width, height = img.size
                crop_top = int(height * 0.12)
                img_cropped = img.crop((0, crop_top, width, height))

                cropped_path = os.path.join(img_dir, f"cropped_{i+1}.png")
                img_cropped.save(cropped_path)

                # Insertar en PDF final
                new_width, new_height = img_cropped.size
                pdf.add_page(format=(new_width, new_height))
                pdf.image(cropped_path, x=0, y=0, w=new_width, h=new_height)

            pdf.output(output_path)

            # Mostrar descarga
            with open(output_path, "rb") as f:
                st.success("✅ PDF procesado exitosamente.")
                st.download_button(
                    label="📥 Descargar PDF sin logo",
                    data=f,
                    file_name="documento_sin_logo.pdf",
                    mime="application/pdf"
                )
