from fpdf import FPDF


def export_chat_pdf(messages):

    pdf = FPDF()

    # Create page
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(
        0,
        10,
        "Gemini AI Chat History",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # Normal text
    pdf.set_font("Arial", size=12)

    for msg in messages:

        role = msg["role"].capitalize()

        content = msg["content"]

        pdf.multi_cell(
            0,
            10,
            f"{role}: {content}"
        )

        pdf.ln(5)

    # Save PDF
    pdf.output("chat_history.pdf")