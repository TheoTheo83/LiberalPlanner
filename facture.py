from fpdf import FPDF


class PDF_Invoice(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(80)
        self.cell(30, 10, 'Devis', 1, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

pdf = PDF_Invoice()
pdf.add_page()

def enteteFacture():

    pdf.set_font('Arial', 'B', 10)
    pdf.set_xy(10, 20)
    pdf.cell(80, 10, 'MaSociete', 0, 0, 'L')

    pdf.set_font('Arial', '', 8)
    pdf.set_xy(10, 30)
    pdf.multi_cell(80, 10, 'MonAdresse\n75000 PARIS\nR.C.S. PARIS \nB 000 000 007\nCapital : 18000 EURO', 0, 'L')

    pdf.set_font('Arial','B',10)
    pdf.set_xy(140, 20)
    pdf.cell(80,10,'Client: CL01',0,0,'L')

    pdf.set_font('Arial', '',8)
    pdf.set_xy(140, 30)
    pdf.multi_cell(80, 10, 'Ste\nM. XXXX\n3ème étage\n33, rue d\'ailleurs\n75000 PARIS', 0, 'L')
    
    return pdf



def contenueFacture():
    pdf.ln(20)
    pdf.cell(0, 10, 'Règlement: Chèque à réception de facture', 0, 1, 'L')

    pdf.cell(0, 10, 'Échéance: 03/12/2003', 0, 1, 'L')

    pdf.cell(0, 10, 'Numéro de TVA: FR888777666', 0, 1, 'L')

    pdf.cell(0, 10, 'Référence: Devis ... du ....', 0, 1, 'L')

    pdf.ln(20)

    cols = ['REFERENCE', 'DESIGNATION', 'MONTANT H.T.', 'TVA']
    col_width = pdf.w / 6

    pdf.set_font('Arial', 'B', 8)
    for col in cols:
        pdf.cell(col_width, 8, col, 1, 0, 'C')
    pdf.ln()

    pdf.set_font('Arial', '', 8)

    line = ['REF1',
            'Carte Mère MSI 6378\nProcesseur AMD 1Ghz\n128Mo SDRAM, 30 Go Disque, CD-ROM']
    for item in line:
        pdf.cell(col_width, 30, item, 1, 0, 'L')
    pdf.ln()

    line = ['REF2', 'Câble RS232', '1', '10.00']
    for item in line:
        pdf.cell(col_width, 10, item, 1, 0, 'L')
    pdf.ln()

    pdf.ln(10)

    pdf.cell(0, 10, 'Total HT : 660.00', 0, 1, 'R')

    pdf.cell(0, 10, 'TVA (19.6%) : 128.76', 0, 1, 'R')

    pdf.cell(0, 10, 'Total TTC : 788.76', 0, 1, 'R')

    return pdf

# Autres éléments de la facture/devis...
if '__main__' == __name__:
    enteteFacture()
    contenueFacture()
    pdf.output('output.pdf')
