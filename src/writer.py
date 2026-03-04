from fpdf import FPDF
import os

def create_wisdom_pdf(title, summary_data, filename):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)
    
    for section, content in summary_data.items():
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, section.replace("_", " ").capitalize(), ln=True)
        pdf.set_font("helvetica", "", 12)
        
        # Ensure we handle the "empty exercise" bug
        if isinstance(content, list):
            if not content: # If list is empty
                content = ["Reflect on the themes above."]
            formatted_text = "\n".join([f"- {item}" for item in content])
        else:
            formatted_text = str(content)
            
        pdf.multi_cell(0, 8, formatted_text)
        pdf.ln(5)
        
    os.makedirs("library/wisdom_pdfs", exist_ok=True)
    pdf.output(f"library/wisdom_pdfs/{filename}.pdf")