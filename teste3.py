import gspread
from google.oauth2.service_account import Credentials
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurações para autenticação com o Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Caminho para o arquivo JSON de credenciais
credentials_path = 'C:/Users/guiga/Downloads/vaulted-bonsai-401514-655924858dac.json'

# Carrega as credenciais do arquivo JSON
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

# Autoriza o cliente gspread com as credenciais
client = gspread.authorize(credentials)

# Identificador da planilha
spreadsheet_id = '1TT7zN2oq1WUdbufbPuq6PLL93KDNNgWh9Tet3zFP5AI'

# Abre a planilha
try:
    worksheet = client.open_by_key(spreadsheet_id).sheet1
    print("Planilha aberta com sucesso!")

except Exception as e:
    print("Erro ao abrir a planilha:", e)

# Função para agendar o horário selecionado
def agendar_horario():
    # Obter os valores inseridos pelo usuário
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    data = entry_data.get()
    horario_index = listbox_horarios.curselection()  # Obtém o índice do horário selecionado na lista

    # Verifica se todos os campos foram preenchidos
    if not nome or not email or not telefone or not data or not horario_index:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Obtém o horário selecionado
    horario_selecionado = listbox_horarios.get(horario_index[0])

    # Obter data e hora atuais
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Atualizar a planilha com as informações do agendamento
    nova_linha = [nome, email, telefone, data, horario_selecionado, data_atual]
    try:
        worksheet.append_row(nova_linha)
        messagebox.showinfo("Agendamento Confirmado", f"Agendamento realizado com sucesso para:\n\nNome: {nome}\nEmail: {email}\nTelefone: {telefone}\nData: {data}\nHorário: {horario_selecionado}")
        # Limpar os campos de entrada após o agendamento
        resetar_informacoes()
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar os dados para a planilha: {e}")

# Função para redefinir as informações após o agendamento
def resetar_informacoes():
    # Limpar os campos de entrada de nome, email e telefone
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

    # Limpar a seleção de data e horário
    entry_data.delete(0, tk.END)
    listbox_horarios.selection_clear(0, tk.END)

# Criar a interface gráfica
root = tk.Tk()
root.title("Agendamento")

# Campos de entrada para informações do usuário
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_email = tk.Label(root, text="E-mail:")
label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=5)

label_telefone = tk.Label(root, text="Telefone:")
label_telefone.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1, padx=10, pady=5)

label_data = tk.Label(root, text="Digite a data (DD/MM/AAAA):")
label_data.grid(row=3, column=0, padx=10, pady=5)
entry_data = tk.Entry(root)
entry_data.grid(row=3, column=1, padx=10, pady=5)

label_horario = tk.Label(root, text="Escolha o horário:")
label_horario.grid(row=4, column=0, padx=10, pady=5)

# Cria uma lista de horários disponíveis
hora_inicio = 10
hora_fim = 21
horarios_disponiveis = [f"{hora}:00" for hora in range(hora_inicio, hora_fim + 1)]

# Cria uma caixa de listagem para os horários disponíveis
listbox_horarios = tk.Listbox(root, selectmode=tk.SINGLE, height=len(horarios_disponiveis))
for horario in horarios_disponiveis:
    listbox_horarios.insert(tk.END, horario)
listbox_horarios.grid(row=4, column=1, padx=10, pady=5)

# Cria um botão para agendar o horário selecionado
agendar_button = tk.Button(root, text="Agendar Horário", command=agendar_horario)
agendar_button.grid(row=5, columnspan=2, padx=10, pady=10)

root.mainloop()  # Inicia o loop principal da interface gráfica
