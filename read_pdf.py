import fitz  # PyMuPDF

# Ruta al archivo PDF
pdf_file = "./files/TicketOrder477381.pdf"

# Abre el archivo PDF
pdf_document = fitz.open(pdf_file)

# Variable para almacenar el número de orden
numero_de_orden = None

# Recorre las páginas del PDF
for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    
    # Extrae el texto de la página
    page_text = page.get_text()
    
    # Busca la cadena "Valor Tiquete:"
    if "Valor Tiquete:" in page_text:
        # Encuentra el índice de "Valor Tiquete:"
        start_index = page_text.index("Valor Tiquete:")
        
        # Extrae el número que sigue a "Valor Tiquete:"
        numero_de_orden = page_text[start_index + len("Valor Tiquete:"):].strip()

        numero_de_orden = numero_de_orden.split(' ')[0]

        numero_de_orden = numero_de_orden.split('\n')[0]
        
        # Rompe el bucle si se encuentra el número
        break

# Cierra el documento PDF
pdf_document.close()

# Comprueba si se encontró el número de orden y lo imprime
if numero_de_orden:
    print(f"Número de Orden: {numero_de_orden}")
else:
    print("No se encontró el número de orden en el PDF.")
