from fpdf import FPDF
import os

BRAND = "Wisdom Synthesis Engine"

def clean_text(text):
    """
    FPDF core fonts (like Helvetica) are limited to Latin-1.
    This helper normalizes common “smart” punctuation to ASCII.
    """
    if text is None:
        return ""
    text = str(text)

    replacements = {
        "—": "-",   # em dash
        "–": "-",   # en dash
        "’": "'",   # right single quote
        "‘": "'",   # left single quote
        "“": "\"",  # left double quote
        "”": "\"",  # right double quote
        "…": "...", # ellipsis
        "•": "-",   # bullet
        "\u00A0": " ",  # non-breaking space
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)

    # Strip stray JSON structural characters that may leak from AI output
    for char in ("{", "}", "[", "]"):
        text = text.replace(char, "")

    # Last-resort safety: strip remaining non-ASCII chars.
    return text.encode("ascii", "ignore").decode("ascii")

def create_wisdom_pdf(title, summary_data, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=20)  # flow long content onto new pages
    pdf.add_page()

    # Header
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, clean_text(BRAND), ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Title
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 10, clean_text(title), ln=True, align="C")
    pdf.ln(10)

    for section, content in summary_data.items():
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, clean_text(section.replace("_", " ").title()), ln=True)
        pdf.set_font("helvetica", "", 12)

        if isinstance(content, list):
            if not content:
                content = ["No items extracted for this section."]
            formatted_text = "\n".join([f"- {clean_text(item)}" for item in content])
        else:
            formatted_text = clean_text(content)

        # Long lists wrap and flow to new pages via multi_cell + set_auto_page_break
        pdf.multi_cell(0, 8, clean_text(formatted_text))
        pdf.ln(5)

    # Footer
    pdf.ln(10)
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, clean_text(BRAND + " - Personal research, 100% local."), ln=True, align="C")

    os.makedirs("library/wisdom_pdfs", exist_ok=True)
    pdf.output(f"library/wisdom_pdfs/{filename}.pdf")
    print(f"   PDF saved: library/wisdom_pdfs/{filename}.pdf")
