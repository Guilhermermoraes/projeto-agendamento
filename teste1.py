import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Definindo o intervalo de horários disponíveis (das 10h às 21h)
hora_inicio = 10
hora_fim = 21

# Dicionário para armazenar os horários selecionados
horarios_selecionados = {}


def validar_horario_funcionamento():
    # Função para validar se o horário atual está dentro do horário de funcionamento
    hora_atual = datetime.now().hour
    return hora_inicio <= hora_atual <= hora_fim


def exibir_tela_horarios_disponiveis():
    # Função para exibir a tela com os horários de atendimento disponíveis
    root2 = tk.Tk()
    root2.title("Horários de Atendimento Disponíveis")

    label_titulo = tk.Label(root2, text="Horários de Atendimento Disponíveis:", font=("Helvetica", 14, "bold"))
    label_titulo.pack(pady=10)

    for hora in range(hora_inicio, hora_fim + 1):
        horario_str = "{}:00".format(hora)
        if horario_str in horarios_selecionados:
            continue
        button_horario = tk.Button(root2, text=horario_str, command=lambda h=horario_str: selecionar_horario(h))
        button_horario.pack()

    root2.mainloop()


def selecionar_horario(horario):
    # Função para selecionar um horário
    horarios_selecionados[horario] = True
    messagebox.showinfo("Horário Selecionado", "Horário {} selecionado com sucesso!".format(horario))


def coletar_informacoes():
    # Função para coletar as informações da pessoa
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    if not nome or not email or not telefone:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Exibir as informações do usuário
    messagebox.showinfo("Informações do Usuário", "Nome: {}\nEmail: {}\nTelefone: {}".format(nome, email, telefone))

    # Verificar a data e o horário de funcionamento
    if not validar_horario_funcionamento():
        messagebox.showinfo("Horário Indisponível", "Desculpe, estamos fechados no momento.")
        return

    # Exibir os horários de atendimento disponíveis
    exibir_tela_horarios_disponiveis()


root = tk.Tk()
root.title("Coleta de Informações")

# Widgets para coletar informações da pessoa
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_email = tk.Label(root, text="Email:")
label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=5)

label_telefone = tk.Label(root, text="Telefone:")
label_telefone.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1, padx=10, pady=5)

button_continuar = tk.Button(root, text="Continuar", command=coletar_informacoes)
button_continuar.grid(row=3, columnspan=2, padx=10, pady=10)

root.mainloop()
