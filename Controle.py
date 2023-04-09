from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

# cria um banco de dados
banco = mysql.connector.connect(
    host = "localhost",
    username = "root",
    passwd = "",
    database = "controle_estoque"
)
print(banco)

# Função que chama segunda tela e lista dados já inseridos
def lista_estoque():
    telaLista.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    telaLista.tableWidget.setRowCount(len(dados_lidos))
    telaLista.tableWidget.setColumnCount(6)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
           telaLista.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

# Função que imprime os dados da lista em PDF
def salvar_pdf():

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0

    pdf = canvas.Canvas("estoque.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "Produto")
    pdf.drawString(210,750, "Quantidade")
    pdf.drawString(310,750, "Código")
    pdf.drawString(410,750, "Preço")
    pdf.drawString(510,750, "Categoria")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(510,750 - y, str(dados_lidos[i][5]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")

# Função que exclui um produto
def exclui_dado():

    linha = telaLista.tableWidget.currentRow()
    telaLista.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))


# Função principal
def main():

    line1 = formulario.lineEdit.text()
    line2 = formulario.lineEdit_2.text()
    line3 = formulario.lineEdit_3.text()
    line4 = formulario.lineEdit_4.text()

    categoria  = ""

    if formulario.radioButton.isChecked() :
        print("Categoria 'Não Perecível' selecionada")
        categoria  = "Não Perecível"
    elif formulario.radioButton_2.isChecked() :
        print("Categoria 'Perecível' selecionada")
        categoria  = "Perecível"
    elif formulario.radioButton_3.isChecked() :
        print("Categoria 'Bebida' selecionada")
        categoria  = "Bebida"
    elif formulario.radioButton_4.isChecked() :
        print("Categoria 'Outros' selecionada")
        categoria  = "Outros"
    else : print("Não foi selecionada categoria")

    print("Produto: " , line1)
    print("Codigo: " , line2)
    print("Quantidade: " , line3)
    print("Preco: " , line4 )

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (produto,codigo,quantidade, preco,categoria) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(line1),str(line2),str(line3),str(line4),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")


app = QtWidgets.QApplication([])
formulario = uic.loadUi("Form.ui")
telaLista = uic.loadUi("TelaLista.ui")
formulario.pushButton.clicked.connect(main)
formulario.pushButton_2.clicked.connect(lista_estoque)
telaLista.pushButton.clicked.connect(salvar_pdf)
telaLista.pushButton_2.clicked.connect(exclui_dado)

formulario.show()
app.exec()

# cria tabelinha pono mysql
""" create table produtos (
    id INT NOT NULL AUTO_INCREMENT,
    produto VARCHAR(100),
    codigo INT,
    quantidade INT,
    preco DOUBLE,
    categoria VARCHAR(50),
    PRIMARY KEY (id)
); """
