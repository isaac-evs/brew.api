from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

class PDFService:
    @staticmethod
    def generate_sales_note_pdf(sales_note, customer, products, addresses):
        """Generate a PDF for a sales note"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        styles = getSampleStyleSheet()
        style_heading = styles['Heading1']
        style_normal = styles['Normal']

        content = []

        content.append(Paragraph("SALES NOTE", style_heading))
        content.append(Spacer(1, 20))

        content.append(Paragraph(f"Customer: {customer.company_name}", style_normal))
        content.append(Paragraph(f"Business: {customer.business_name}", style_normal))
        content.append(Paragraph(f"Email: {customer.email}", style_normal))
        content.append(Spacer(1, 10))

        billing_address = next((a for a in addresses if a.id == sales_note.billing_address_id), None)
        shipping_address = next((a for a in addresses if a.id == sales_note.shipping_address_id), None)

        if billing_address:
            content.append(Paragraph("Billing Address:", styles['Heading3']))
            content.append(Paragraph(f"{billing_address.address}", style_normal))
            content.append(Paragraph(f"{billing_address.neighborhood}, {billing_address.municipality}", style_normal))
            content.append(Paragraph(f"{billing_address.state}", style_normal))
            content.append(Spacer(1, 10))

        if shipping_address:
            content.append(Paragraph("Shipping Address:", styles['Heading3']))
            content.append(Paragraph(f"{shipping_address.address}", style_normal))
            content.append(Paragraph(f"{shipping_address.neighborhood}, {shipping_address.municipality}", style_normal))
            content.append(Paragraph(f"{shipping_address.state}", style_normal))
            content.append(Spacer(1, 10))

        product_data = [["Product", "Quantity", "Unit Price", "Amount"]]

        for item in sales_note.note_contents:
            product = next((p for p in products if p.id == item.product_id), None)
            if product:
                product_data.append([
                    product.name,
                    str(item.quantity),
                    f"${item.unit_price:.2f}",
                    f"${item.amount:.2f}"
                ])

        product_data.append(["", "", "Total:", f"${sales_note.total:.2f}"])

        table = Table(product_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))

        content.append(table)

        doc.build(content)

        pdf_data = buffer.getvalue()
        buffer.close()

        return pdf_data
