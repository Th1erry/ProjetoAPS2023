#Importações
from tkinter import *
from tkinter import messagebox
import mysql.connector

# informações de conexão do banco de dados
config = {
    'user': 'root',
    'password': '102030',  # Verificar se o BD está com senha ou não, caso dê erro, remover a senha, deixar string vazia
    'host': 'localhost',
    'database': 'loja_suplementos',
}

# Estabeleça a conexão com o banco de dados MySQL
conn = mysql.connector.connect(**config)

# Cursor para consulta
cursor = conn.cursor()

# Consulta SQL Nome
consulta_nome = "SELECT NOME FROM LOJA_SUPLEMENTOS.PRODUTOS;"
cursor.execute(consulta_nome)

# Recupere os resultados da consulta e armazena no array = resultado_nome
resultado_nome = []

for linha in cursor.fetchall():
    resultado_nome.append(linha)

# Consulta SQL Preço
consulta_preco = "SELECT PRECO FROM LOJA_SUPLEMENTOS.PRODUTOS;"
cursor.execute(consulta_preco)

# Recupere os resultados da consulta e armazena no array = resultado_preco
resultado_preco = []

for linha in cursor.fetchall():
    resultado_preco.append(linha)

# Feche o cursor e a conexão com o banco de dados quando terminar
cursor.close()
conn.close()

produtos = []
precoProdutos = []

for i in range(5):
    produtos.append(resultado_nome[i])
    precoProdutos.append(resultado_preco[i])

#configurações da janela
janela = Tk()
janela.title("Loja de Suplementos")
janela.geometry("750x590+230+70")
janela.resizable(False,False)
janela.iconbitmap("Imagens/icon1.ico")
fundoImg = PhotoImage(file="Imagens/fundoMenu.png")
Label(janela,image=fundoImg).place(x=-10,y=90)

tituloImg = PhotoImage(file="Imagens/logo.png")
titulo = Label(
    janela,
    image=tituloImg
)

#carrinho--------------------------------------------------------
carrinhoNumero = Label(janela,text="0",font="Impact, 16",bg="white",fg="red")
carrinhoNumero.place(x=620,y=35)

#as listas precisam ser inicializadas antes
carrinhoItensGlobal = ["Vazio"]
carrinhoValorGlobal = [0]

#imagens usadas
pixImg=PhotoImage(file="Imagens\pix.png")
cartaoImg = PhotoImage(file="Imagens\cartao.png")

def carrinhoCompras():
    #configura a janela do carrinho
    carrinhoJanela = Toplevel(janela)
    carrinhoJanela.title("Carrinho de compras")
    carrinhoJanela.geometry("500x350+430+250")
    carrinhoJanela.resizable(False, False)
    carrinhoJanela.iconbitmap("Imagens/icon2.ico")

    #Campo de texto onde fica os itens
    carrinhoItens = Text(carrinhoJanela,font="arial, 13",width=51,height=13)
    carrinhovalor = 0

    Label(carrinhoJanela,text="Itens do Carrinho:",font="arial, 13").place(x=8,y=3)

    indice = 0
    for indice in range(len(carrinhoItensGlobal)):
        carrinhoItens.insert(INSERT,carrinhoItensGlobal[indice])
        carrinhoItens.insert(INSERT,"   VALOR: R$")
        carrinhoItens.insert(INSERT,carrinhoValorGlobal[indice])
        carrinhoItens.insert(INSERT,"\n")
    
    Label(carrinhoJanela,text="Valor Total: R$",font="Arial, 15").place(x=25,y=300)
    valorTotal = Label(carrinhoJanela,text=sum(carrinhoValorGlobal),font="arial, 18",fg="green")

    #comando que faz limpar o carrinho
    def limparCarrinho():
        carrinhoItens.delete('1.0', END)
        tamanhoLista = len(carrinhoValorGlobal)
        for _ in range(tamanhoLista):
            carrinhoItensGlobal.pop()  # Remove o último elemento
            carrinhoValorGlobal.pop()  # Remove o último elemento
        carrinhoItensGlobal.append("Vazio")
        carrinhoValorGlobal.append(0)
        valorTotal.config(text=0)
        carrinhoNumero.config(text="0")
    limpar = Button(carrinhoJanela, text="LIMPAR", bg="red", command=limparCarrinho)

    #Comando de compra
    def comprarProdutos():
        #configurando a janela do pagamento
        pagamentoJanela = Toplevel(carrinhoJanela)
        pagamentoJanela.title('Confirmação e Pagamentos')
        pagamentoJanela.geometry("600x450+500+350")
        pagamentoJanela.resizable(False, False)
        pagamentoJanela.iconbitmap("Imagens/icon2.ico")
        
        #sistema de escolher o método de pagamento
        metodoPagamento = IntVar()
        Label(pagamentoJanela, text="Métodos de Pagamento: ", font="arial, 16").place(x=15, y=10)
        #opção Pix
        Radiobutton(pagamentoJanela, text="PIX", font="Arial, 20", variable=metodoPagamento, value=1).place(x=115, y=70)
        pix = Label(pagamentoJanela, image=pixImg)
        pix.place(x=15, y=45)
        #opção cartão
        cartao = Label(pagamentoJanela, image=cartaoImg)
        cartao.place(x=300, y=45)
        Radiobutton(pagamentoJanela, text="Cartão", font="Arial, 20", variable=metodoPagamento, value=2).place(x=400, y=70)
        #Endereços de entrega
        Label(pagamentoJanela, text="Insira o endereço de entrega:",font="Arial, 14").place(x=12,y=170)
        Label(pagamentoJanela, text="Rua:",font="Arial, 12").place(x=15,y=200)
        ruaEndereco = Entry(pagamentoJanela,font=("Arial,12"),width=18)
        ruaEndereco.place(x=60,y=200)
        Label(pagamentoJanela, text="NR:",font="Arial, 12").place(x=250,y=200)
        nrEndereco = Entry(pagamentoJanela,font=("Arial,12"),width=4)
        nrEndereco.place(x=285,y=200)
        Label(pagamentoJanela, text="Estado:",font="Arial, 12").place(x=15,y=240)
        estadoEndereco = Entry(pagamentoJanela,font=("Arial,12"),width=18)
        estadoEndereco.place(x=80,y=240)
        Label(pagamentoJanela, text="Cidade:",font="Arial, 12").place(x=270,y=240)
        cidadeEndereco = Entry(pagamentoJanela,font=("Arial,12"),width=18)
        cidadeEndereco.place(x=335,y=240)
        Label(pagamentoJanela, text="CEP:",font="Arial, 12").place(x=15,y=280)
        #COMANDO PARA VALIDAR O CEP DO ENDEREÇO E O PAGAMENTO
        cepValido = ""
        def validaTudo():
            #valida CEP
            global cepValido
            try:
                int(cepEndereco.get("1.0", "end-1c"))
                cepValido = "s"
            except ValueError:
                cepValido = "n"
            #Valida pagamento
            if carrinhoItensGlobal[0] == "Vazio":
                messagebox.showerror(title = "Erro no pagamento", message = "Seu carrinho de compras está vazio.")
            elif cepValido == "n":
                messagebox.showerror(title = "Erro no endereço", message = "Seu CEP é invalido, insira apenas numeros.")
            elif not ruaEndereco.get():
                messagebox.showerror(title = "Erro no endereço", message = "Insira todos os campos")
            elif not cidadeEndereco.get():
                messagebox.showerror(title = "Erro no endereço", message = "Insira todos os campos")
            elif not estadoEndereco.get():
                messagebox.showerror(title = "Erro no endereço", message = "Insira todos os campos")
            elif not nrEndereco.get():
                messagebox.showerror(title = "Erro no endereço", message = "Insira todos os campos")
            else:
                messagebox.showinfo(title = "Sucesso", message = "Compra finalizada com sucesso!")
        cepEndereco = Text(pagamentoJanela,font=("Arial,12"),width=16,height=1)
        cepEndereco.place(x=60,y=280)
        ConfirmarPagamento = Button(pagamentoJanela, text="CONFIRMAR", bg="green", width=10,height=2, command=validaTudo)
        ConfirmarPagamento.place(x=250, y=360)
        #finalização do pagamento
        
    comprar = Button(carrinhoJanela, text="COMPRAR", bg="green", command=comprarProdutos)

    limpar.place(x=330, y=300)
    comprar.place(x=400, y=300)
    valorTotal.place(x=160,y=299)
    carrinhoItens.place(x=10,y=30)

def fazerLogin():
    janelaLogin = Toplevel(janela)
    janelaLogin.title("Fazer login")
    janelaLogin.geometry("400x250+430+250")
    janelaLogin.resizable(False, False)
    janelaLogin.iconbitmap("Imagens/icon3.ico")

    Label(janelaLogin, text="Usuario: ",font="Arial,12").place(x=70,y=30)
    usuarioLogin = Entry(janelaLogin)
    usuarioLogin.place(x=140,y=31)
    Label(janelaLogin, text="Senha: ",font="Arial,12").place(x=70,y=80)
    usuarioSenha = Entry(janelaLogin, show='*')
    usuarioSenha.place(x=140,y=80)

    adm = Checkbutton(janelaLogin, text="Sou adminstrador", onvalue=1, offvalue=0)
    adm.place(x=70,y=120)

    def fazer_login(username, senha):
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print(str(username))
        print(str(senha))
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, senha))
        user = cursor.fetchone()
        cursor.close()
        # Devolve o objeto user com os dados encontrados, caso usuario e senha esteja errados -> 
        # retorna none
        if (user == None):
            # Executa a logica a baixo caso o usuario e senha esteja ERRADO
            print("Usuario Invalido")
        else:
            # Executa a logica a baixo caso o usuario e senha esteja CORRETO
            print("Usuario Logado")
        return user

    def logar():
        #Parte de verificar se existe o login no banco de dados
        login = str(usuarioLogin.get())
        senha = str(usuarioSenha.get())
        fazer_login(login, senha)
        a = 1
    def CadastraDados():
        #Marcos aqui sua parte de fazer os dados do input ser levado pro banco de dados
        a = 1
    cadastrar = Button(janelaLogin, text="Cadastrar")
    entrar = Button(janelaLogin, text=" Entrar ", command=logar)
    cadastrar.place(x=120,y=200)
    entrar.place(x=220,y=200)

loginImg = PhotoImage(file="Imagens\login.png")
login = Button(janela,image=loginImg,command=fazerLogin,bg="white",relief='flat')


carrinhoImg = PhotoImage(file="Imagens\carrinho.png")
carrinho = Button(janela,image=carrinhoImg,command=carrinhoCompras,relief='flat',bg="white")

#produtos
wheyImg = PhotoImage(file="Imagens\whey.png")
whey = Label(janela,image=wheyImg,width=130)
wheyPreco = Label(
    janela,
    text="R$" + str(resultado_preco[0][0]),
    font=("arial", 20),
    bg="green",
    width=8
)

bcaaImg = PhotoImage(file="Imagens/bcaa.png")
bcaa = Label(janela,image=bcaaImg,width=130)
bcaaPreco = Label(
    janela,
    text="R$" + str(resultado_preco[3][0]),
    font=("arial", 20),
    bg="green",
    width=8
)

creatinaImg = PhotoImage(file="Imagens\creatina.png")
creatina = Label(janela,image=creatinaImg,width=130)
creatinaPreco = Label(
    janela,
    text="R$" + str(resultado_preco[2][0]),
    font=("arial", 20),
    bg="green",
    width=8
)


cafeinaImg = PhotoImage(file="Imagens\cafeina.png")
cafeina = Label(janela,image=cafeinaImg,width=130)
cafeinaPreco = Label(
    janela,
    text="R$" + str(resultado_preco[4][0]),
    font=("arial", 20),
    bg="green",
    width=8
)


mvImg = PhotoImage(file="Imagens\multivitaminico.png")
mv = Label(janela,image=mvImg,width=130)
mvPreco = Label(
    janela,
    text="R$" + str(resultado_preco[1][0]),
    font=("arial", 20),
    bg="green",
    width=8
)


def comprarWhey():
    for indice in range(len(carrinhoItensGlobal)):
        if carrinhoValorGlobal[indice] == 0:
            carrinhoItensGlobal[indice] = resultado_nome[0][0]
            carrinhoValorGlobal[indice] = resultado_preco[0][0]
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break
        else:
            carrinhoItensGlobal.append(resultado_nome[0][0])
            carrinhoValorGlobal.append(resultado_preco[0][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break

wheyComprar = Button(janela,text="COMPRAR",command=comprarWhey,relief='solid',font="Verdana")

def comprarBcaa():
    for indice in range(len(carrinhoItensGlobal)):
        if carrinhoValorGlobal[indice] == 0:
            carrinhoItensGlobal[indice] = resultado_nome[3][0]
            carrinhoValorGlobal[indice] = resultado_preco[3][0]
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break
        else:
            carrinhoItensGlobal.append(resultado_nome[3][0])
            carrinhoValorGlobal.append(resultado_preco[3][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break

bcaaComprar = Button(janela,text="COMPRAR",command=comprarBcaa,relief='solid',font="Verdana")

def comprarCreatina():
    for indice in range(len(carrinhoItensGlobal)):
        if carrinhoValorGlobal[indice] == 0:
            carrinhoItensGlobal[indice] = resultado_nome[2][0]
            carrinhoValorGlobal[indice] = resultado_preco[2][0]
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break
        else:
            carrinhoItensGlobal.append(resultado_nome[2][0])
            carrinhoValorGlobal.append(resultado_preco[2][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break

creatinaComprar = Button(janela,text="COMPRAR",command=comprarCreatina,relief='solid',font="Verdana")

def comprarCafeina():
    for indice in range(len(carrinhoItensGlobal)):
        if carrinhoValorGlobal[indice] == 0:
            carrinhoItensGlobal[indice] = (resultado_nome[4][0])
            carrinhoValorGlobal[indice] = (resultado_preco[4][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break
        else:
            carrinhoItensGlobal.append(resultado_nome[4][0])
            carrinhoValorGlobal.append(resultado_preco[4][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break

cafeinaComprar = Button(janela,text="COMPRAR",command=comprarCafeina,relief='solid',font="Verdana")

def comprarMV():
    for indice in range(len(carrinhoItensGlobal)):
        if carrinhoValorGlobal[indice] == 0:
            carrinhoItensGlobal[indice] = (resultado_nome[1][0])
            carrinhoValorGlobal[indice] = (resultado_preco[1][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break
        else:
            carrinhoItensGlobal.append(resultado_nome[1][0])
            carrinhoValorGlobal.append(resultado_preco[1][0])
            carrinhoNumero.config(text=len(carrinhoItensGlobal))
            break

mvComprar = Button(janela,text="COMPRAR",command=comprarMV,relief='solid',font="Verdana")

#AREA DE NAVEGAÇÃO
def filtrarWhey():
    creatina.place(x=1000,y=1000)
    creatinaPreco.place(x=1000,y=1000)
    creatinaComprar.place(x=1000,y=1000)
    bcaa.place(x=5000,y=1300)
    bcaaPreco.place(x=5000,y=2500)
    bcaaComprar.place(x=5200,y=2900)
    cafeina.place(x=2000,y=1030)
    cafeinaPreco.place(x=2000,y=2050)
    cafeinaComprar.place(x=2200,y=2900)
    mv.place(x=1500,y=3050)
    mvPreco.place(x=1500,y=1470)
    mvComprar.place(x=1170,y=1510)
    whey.place(x=50,y=130)
    wheyPreco.place(x=50,y=250)
    wheyComprar.place(x=70,y=290)

def filtrarBCAA():
    creatina.place(x=1000,y=1000)
    creatinaPreco.place(x=1000,y=1000)
    creatinaComprar.place(x=1000,y=1000)
    cafeina.place(x=2000,y=1030)
    cafeinaPreco.place(x=2000,y=2050)
    cafeinaComprar.place(x=2200,y=2900)
    mv.place(x=1500,y=3050)
    mvPreco.place(x=1500,y=1470)
    mvComprar.place(x=1170,y=1510)
    whey.place(x=1150,y=1130)
    wheyPreco.place(x=1150,y=2150)
    wheyComprar.place(x=1170,y=2190)
    bcaa.place(x=50,y=130)
    bcaaPreco.place(x=50,y=250)
    bcaaComprar.place(x=70,y=290)

def filtrarVitamina():
    creatina.place(x=1000,y=1000)
    creatinaPreco.place(x=1000,y=1000)
    creatinaComprar.place(x=1000,y=1000)
    cafeina.place(x=2000,y=1030)
    cafeinaPreco.place(x=2000,y=2050)
    cafeinaComprar.place(x=2200,y=2900)
    wheyPreco.place(x=1150,y=2150)
    wheyComprar.place(x=1170,y=2190)
    bcaa.place(x=2000,y=1030)
    bcaaPreco.place(x=2000,y=1030)
    bcaaComprar.place(x=2000,y=1030)
    mv.place(x=50,y=130)
    mvPreco.place(x=50,y=250)
    mvComprar.place(x=70,y=290)

def filtrarCreatina():
    cafeina.place(x=2000,y=1030)
    cafeinaPreco.place(x=2000,y=2050)
    cafeinaComprar.place(x=2200,y=2900)
    wheyPreco.place(x=1150,y=2150)
    wheyComprar.place(x=1170,y=2190)
    bcaa.place(x=2000,y=1030)
    bcaaPreco.place(x=2000,y=1030)
    bcaaComprar.place(x=2000,y=1030)
    mv.place(x=2000,y=1030)
    mvPreco.place(x=2000,y=1030)
    mvComprar.place(x=2000,y=1030)
    creatina.place(x=50,y=130)
    creatinaPreco.place(x=50,y=250)
    creatinaComprar.place(x=70,y=290)

def filtrarCafeina():
    wheyPreco.place(x=1150,y=2150)
    wheyComprar.place(x=1170,y=2190)
    bcaa.place(x=2000,y=1030)
    bcaaPreco.place(x=2000,y=1030)
    bcaaComprar.place(x=2000,y=1030)
    mv.place(x=2000,y=1030)
    mvPreco.place(x=2000,y=1030)
    mvComprar.place(x=2000,y=1030)
    creatina.place(x=2000,y=1030)
    creatinaPreco.place(x=2000,y=1030)
    creatinaComprar.place(x=2000,y=1030)
    cafeina.place(x=50,y=130)
    cafeinaPreco.place(x=50,y=250)
    cafeinaComprar.place(x=70,y=290)

def filtrarTodos():
    whey.place(x=50,y=130)
    wheyPreco.place(x=50,y=250)
    wheyComprar.place(x=70,y=290)
    creatina.place(x=350,y=130)
    creatinaPreco.place(x=350,y=250)
    creatinaComprar.place(x=370,y=290)
    bcaa.place(x=500,y=130)
    bcaaPreco.place(x=500,y=250)
    bcaaComprar.place(x=520,y=290)
    cafeina.place(x=200,y=130)
    cafeinaPreco.place(x=200,y=250)
    cafeinaComprar.place(x=220,y=290)
    mv.place(x=50,y=350)
    mvPreco.place(x=50,y=470)
    mvComprar.place(x=70,y=510)


wheys = Button(janela,text="WHEY",command=filtrarWhey,width=14,height=2,font="Bahnschrift",bg="orange")
bcaas = Button(janela,text="BCAA",command=filtrarBCAA,width=14,height=2,font="Bahnschrift",bg="orange")
vitaminas = Button(janela,text="VITAMINA",command=filtrarVitamina,width=14,height=2,font="Bahnschrift",bg="orange")
creatinas = Button(janela,text="CREATINA",command=filtrarCreatina,width=14,height=2,font="Bahnschrift",bg="orange")
cafeinas = Button(janela,text="CAFEINAS",command=filtrarCafeina,width=14,height=2,font="Bahnschrift",bg="orange")
limparFiltro = Button(janela,text="TODOS",command=filtrarTodos,width=10,height=2,font="Bahnschrift",bg="orange")

#local dos botões da navegação
wheys.place(x=0,y=64)
bcaas.place(x=130,y=64)
vitaminas.place(x=260,y=64)
creatinas.place(x=390,y=64)
cafeinas.place(x=520,y=64)
limparFiltro.place(x=652,y=64)

#local dos objetos
titulo.place(x=-10, y=-2)
whey.place(x=50,y=130)
wheyPreco.place(x=50,y=250)
wheyComprar.place(x=70,y=290)
creatina.place(x=350,y=130)
creatinaPreco.place(x=350,y=250)
creatinaComprar.place(x=370,y=290)
bcaa.place(x=500,y=130)
bcaaPreco.place(x=500,y=250)
bcaaComprar.place(x=520,y=290)
cafeina.place(x=200,y=130)
cafeinaPreco.place(x=200,y=250)
cafeinaComprar.place(x=220,y=290)
mv.place(x=50,y=350)
mvPreco.place(x=50,y=470)
mvComprar.place(x=70,y=510)
login.place(x=30,y=1)
carrinho.place(x=650,y=1)

#mantem a janela aberta
janela.mainloop()
