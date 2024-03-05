import gspread
from google.oauth2.service_account import Credentials
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Configurações para autenticação com o Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Caminho para o arquivo JSON de credenciais
credentials_path = 'C:/Users/guiga/Downloads/vaulted-bonsai-401514-655924858dac.json'

# Carrega as credenciais do arquivo JSON
credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)

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

# Função para verificar os horários disponíveis para agendamento
def load_available_hours():
    # Limpa a listbox de horários
    listbox_horarios.delete(0, tk.END)

    # Obtém a data atual
    data_atual = datetime.now().strftime('%d/%m/%Y')

    # Preenche automaticamente o campo de data
    entry_data.delete(0, tk.END)
    entry_data.insert(0, data_atual)

    # Obtém todos os agendamentos para a data selecionada
    data_texto = entry_data.get()
    agendamentos = worksheet.get_all_records()
    horarios_agendados = [agendamento["Horario Agendamento"] for agendamento in agendamentos if agendamento["Data"] == data_texto]

    # Lista de horários disponíveis
    hora_inicio = 10
    hora_fim = 21
    horarios_disponiveis = [f"{hora}:00" for hora in range(hora_inicio, hora_fim + 1) if f"{hora}:00" not in horarios_agendados]

    # Exibe os horários disponíveis na listbox
    for horario in horarios_disponiveis:
        listbox_horarios.insert(tk.END, horario)

# Função para agendar o horário selecionado
def agendar_horario():
    # Obter os valores inseridos pelo usuário
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    data = entry_data.get()
    horario_selecionado = listbox_horarios.get(listbox_horarios.curselection()[0])

    # Verifica se todos os campos foram preenchidos
    if not nome or not email or not telefone or not data or not horario_selecionado:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    # Atualizar a planilha com as informações do agendamento
    nova_linha = [nome, email, telefone, data, horario_selecionado]
    try:
        worksheet.append_row(nova_linha)
        messagebox.showinfo("Agendamento Confirmado", f"Agendamento realizado com sucesso para:\n\nNome: {nome}\nEmail: {email}\nTelefone: {telefone}\nData: {data}\nHorário: {horario_selecionado}")
        resetar_informacoes()  # Resetar as informações após o agendamento
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao enviar os dados para a planilha: {e}")

# Função para limpar os campos após o agendamento
def resetar_informacoes():
    # Limpa os campos de entrada
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    listbox_horarios.delete(0, tk.END)  # Limpa a listbox de horários

# Criar a interface gráfica
root = tk.Tk()
root.title("Agendamento")

# Obtém a data atual
data_atual = datetime.now().strftime('%d/%m/%Y')

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

label_data = tk.Label(root, text="Data (DD/MM/AAAA):")
label_data.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_data = tk.Entry(root)
entry_data.grid(row=3, column=1, padx=10, pady=5)
entry_data.insert(0, data_atual)  # Preenche automaticamente o campo de data

# Botão para verificar horários disponíveis
btn_verificar_horarios = tk.Button(root, text="Verificar Horários Disponíveis", command=load_available_hours)
btn_verificar_horarios.grid(row=4, columnspan=2, padx=10, pady=5)

# Lista de horários disponíveis
listbox_horarios = tk.Listbox(root, selectmode=tk.SINGLE, height=10)
listbox_horarios.grid(row=5, columnspan=2, padx=10, pady=5)

# Botão para agendar o horário
btn_agendar_horario = tk.Button(root, text="Agendar Horário", command=agendar_horario)
btn_agendar_horario.grid(row=6, columnspan=2, padx=10, pady=5)

root.mainloop()  # Inicia o loop principal da interface gráfica
#Fim do Codigo