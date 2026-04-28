import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
import tkinter as tk


class App(ctk.CTk):
    def __init__(self, database):
        super().__init__()

        self.db = database
        self.title("Cadastro de Alunos")
        self.geometry("700x550")

        self.selected_ra = None

        self.create_widgets()
        self.load_alunos()

    # =========================
    # UI
    # =========================
    def create_widgets(self):
        self.nome_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.nome_entry.pack(pady=5)

        self.data_entry = ctk.CTkEntry(self, placeholder_text="Data (DD/MM/AAAA)")
        self.data_entry.pack(pady=5)

        # eventos do campo data
        self.data_entry.bind("<KeyRelease>", self.formatar_data)
        self.data_entry.bind("<KeyPress>", self.bloquear_letras)

        self.calendar_btn = ctk.CTkButton(
            self, text="📅 Selecionar Data", command=self.abrir_calendario
        )
        self.calendar_btn.pack(pady=5)

        self.add_btn = ctk.CTkButton(self, text="Adicionar", command=self.add_aluno)
        self.add_btn.pack(pady=5)

        self.update_btn = ctk.CTkButton(self, text="Atualizar", command=self.update_aluno)
        self.update_btn.pack(pady=5)

        self.delete_btn = ctk.CTkButton(self, text="Deletar", command=self.delete_aluno)
        self.delete_btn.pack(pady=5)

        # tabela
        self.tree = ttk.Treeview(self, columns=("RA", "Nome", "Data"), show="headings")
        self.tree.heading("RA", text="RA")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data", text="Nascimento")

        self.tree.pack(pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # =========================
    # DATA (VAL + CONVERSÃO)
    # =========================
    def validar_data(self, data_str):
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            if data > datetime.now():
                return False
            return True
        except ValueError:
            return False

    def converter_para_banco(self, data_str):
        return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")

    def converter_para_interface(self, data_str):
        if not data_str:
            return ""
        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")

    # =========================
    # INPUT UX
    # =========================
    def bloquear_letras(self, event):
        if not event.char.isdigit() and event.keysym not in ("BackSpace", "Tab", "Left", "Right"):
            return "break"

    def formatar_data(self, event):
        texto = self.data_entry.get()
        numeros = "".join(filter(str.isdigit, texto))[:8]

        partes = []
        if len(numeros) >= 2:
            partes.append(numeros[:2])
        if len(numeros) >= 4:
            partes.append(numeros[2:4])
        if len(numeros) > 4:
            partes.append(numeros[4:8])

        nova_data = "/".join(partes)

        self.data_entry.delete(0, "end")
        self.data_entry.insert(0, nova_data)

    # =========================
    # CALENDÁRIO
    # =========================
    def abrir_calendario(self):
        top = tk.Toplevel(self)
        top.title("Selecionar Data")

        cal = Calendar(top, date_pattern="dd/mm/yyyy")
        cal.pack(pady=10)

        def selecionar():
            data = cal.get_date()
            self.data_entry.delete(0, "end")
            self.data_entry.insert(0, data)
            top.destroy()

        btn = ctk.CTkButton(top, text="Selecionar", command=selecionar)
        btn.pack(pady=10)

    # =========================
    # TABELA
    # =========================
    def load_alunos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for aluno in self.db.fetch_alunos():
            data_formatada = self.converter_para_interface(aluno[2])
            self.tree.insert("", "end", values=(aluno[0], aluno[1], data_formatada))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")

            self.selected_ra = values[0]

            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, values[1])

            self.data_entry.delete(0, "end")
            self.data_entry.insert(0, values[2])

    def clear_fields(self):
        self.nome_entry.delete(0, "end")
        self.data_entry.delete(0, "end")
        self.selected_ra = None

    # =========================
    # CRUD
    # =========================
    def add_aluno(self):
        nome = self.nome_entry.get()
        data = self.data_entry.get()

        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return

        if data:
            if not self.validar_data(data):
                messagebox.showerror("Erro", "Data inválida!")
                return
            data = self.converter_para_banco(data)

        self.db.insert_aluno(nome, data)
        self.load_alunos()
        self.clear_fields()

    def update_aluno(self):
        if not self.selected_ra:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        nome = self.nome_entry.get()
        data = self.data_entry.get()

        if data:
            if not self.validar_data(data):
                messagebox.showerror("Erro", "Data inválida!")
                return
            data = self.converter_para_banco(data)

        self.db.update_aluno(self.selected_ra, nome, data)
        self.load_alunos()
        self.clear_fields()

    def delete_aluno(self):
        if not self.selected_ra:
            messagebox.showwarning("Aviso", "Selecione um aluno!")
            return

        confirm = messagebox.askyesno("Confirmação", "Deseja deletar?")
        if confirm:
            self.db.delete_aluno(self.selected_ra)
            self.load_alunos()
            self.clear_fields()