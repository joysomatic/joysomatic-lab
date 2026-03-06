from fpdf import FPDF
import os

BRAND = "Wisdom Synthesis Engine"

def create_wisdom_pdf(title, summary_data, filename):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, BRAND, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Title
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)

    for section, content in summary_data.items():
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, section.replace("_", " ").title(), ln=True)
        pdf.set_font("helvetica", "", 12)

        if isinstance(content, list):
            if not content:
                content = ["Reflect on the themes above."]
            formatted_text = "\n".join([f"- {item}" for item in content])
        else:
            formatted_text = str(content)

        pdf.multi_cell(0, 8, formatted_text)
        pdf.ln(5)

    # Footer
    pdf.ln(10)
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, BRAND + " — Personal research, 100% local.", ln=True, align="C")

    os.makedirs("library/wisdom_pdfs", exist_ok=True)
    pdf.output(f"library/wisdom_pdfs/{filename}.pdf")
    print(f"   PDF saved: library/wisdom_pdfs/{filename}.pdf")
