import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='252931Didd$',  # Altere aqui conforme necessário
        database='estacionamento'
    )

def criar_banco_e_tabelas():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='252931Didd$'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS estacionamento")
    cursor.execute("USE estacionamento")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            endereco VARCHAR(200),
            cpf VARCHAR(14) UNIQUE NOT NULL,
            telefone VARCHAR(20)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT NOT NULL,
            marca VARCHAR(50),
            modelo VARCHAR(50),
            ano VARCHAR(4),
            placa VARCHAR(10) UNIQUE,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

# ---------------------------- CLIENTES ----------------------------

def cadastrar_cliente():
    def salvar_cliente():
        nome = entry_nome.get()
        endereco = entry_endereco.get()
        cpf = entry_cpf.get()
        telefone = entry_telefone.get()

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nome, endereco, cpf, telefone) VALUES (%s, %s, %s, %s)",
                           (nome, endereco, cpf, telefone))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            janela.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro: {err}")
        conn.close()

    janela = tk.Toplevel(root)
    janela.title("Cadastrar Cliente")

    tk.Label(janela, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela, text="Endereço:").grid(row=1, column=0)
    entry_endereco = tk.Entry(janela)
    entry_endereco.grid(row=1, column=1)

    tk.Label(janela, text="CPF:").grid(row=2, column=0)
    entry_cpf = tk.Entry(janela)
    entry_cpf.grid(row=2, column=1)

    tk.Label(janela, text="Telefone:").grid(row=3, column=0)
    entry_telefone = tk.Entry(janela)
    entry_telefone.grid(row=3, column=1)

    tk.Button(janela, text="Salvar", command=salvar_cliente).grid(row=4, column=0, columnspan=2, pady=10)

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    janela = tk.Toplevel(root)
    janela.title("Lista de Clientes")

    for c in clientes:
        tk.Label(janela, text=f"ID: {c[0]} | Nome: {c[1]} | CPF: {c[3]} | Telefone: {c[4]}").pack()

def editar_cliente():
    id = simpledialog.askstring("Editar Cliente", "ID do cliente:")
    if not id:
        return
    nome = simpledialog.askstring("Editar Cliente", "Novo nome:")
    endereco = simpledialog.askstring("Editar Cliente", "Novo endereço:")
    cpf = simpledialog.askstring("Editar Cliente", "Novo CPF:")
    telefone = simpledialog.askstring("Editar Cliente", "Novo telefone:")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nome=%s, endereco=%s, cpf=%s, telefone=%s WHERE id=%s",
                   (nome, endereco, cpf, telefone, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Cliente atualizado.")

def excluir_cliente():
    id = simpledialog.askstring("Excluir Cliente", "ID do cliente:")
    if not id:
        return
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Cliente excluído.")

# ---------------------------- VEÍCULOS ----------------------------

def cadastrar_veiculo():
    def salvar_veiculo():
        cliente_id = entry_cliente_id.get()
        marca = entry_marca.get()
        modelo = entry_modelo.get()
        ano = entry_ano.get()
        placa = entry_placa.get()

        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO veiculos (cliente_id, marca, modelo, ano, placa) 
                VALUES (%s, %s, %s, %s, %s)
            """, (cliente_id, marca, modelo, ano, placa))
            conn.commit()
            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
            janela.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro: {err}")
        conn.close()

    janela = tk.Toplevel(root)
    janela.title("Cadastrar Veículo")

    tk.Label(janela, text="ID Cliente:").grid(row=0, column=0)
    entry_cliente_id = tk.Entry(janela)
    entry_cliente_id.grid(row=0, column=1)

    tk.Label(janela, text="Marca:").grid(row=1, column=0)
    entry_marca = tk.Entry(janela)
    entry_marca.grid(row=1, column=1)

    tk.Label(janela, text="Modelo:").grid(row=2, column=0)
    entry_modelo = tk.Entry(janela)
    entry_modelo.grid(row=2, column=1)

    tk.Label(janela, text="Ano:").grid(row=3, column=0)
    entry_ano = tk.Entry(janela)
    entry_ano.grid(row=3, column=1)

    tk.Label(janela, text="Placa:").grid(row=4, column=0)
    entry_placa = tk.Entry(janela)
    entry_placa.grid(row=4, column=1)

    tk.Button(janela, text="Salvar", command=salvar_veiculo).grid(row=5, column=0, columnspan=2, pady=10)

def listar_veiculos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, c.nome, v.marca, v.modelo, v.ano, v.placa 
        FROM veiculos v 
        JOIN clientes c ON v.cliente_id = c.id
    """)
    veiculos = cursor.fetchall()
    conn.close()

    janela = tk.Toplevel(root)
    janela.title("Lista de Veículos")

    for v in veiculos:
        tk.Label(janela, text=f"ID: {v[0]} | Cliente: {v[1]} | {v[2]} {v[3]} {v[4]} - Placa: {v[5]}").pack()

def editar_veiculo():
    id = simpledialog.askstring("Editar Veículo", "ID do veículo:")
    marca = simpledialog.askstring("Editar Veículo", "Nova marca:")
    modelo = simpledialog.askstring("Editar Veículo", "Novo modelo:")
    ano = simpledialog.askstring("Editar Veículo", "Novo ano:")
    placa = simpledialog.askstring("Editar Veículo", "Nova placa:")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE veiculos SET marca=%s, modelo=%s, ano=%s, placa=%s WHERE id=%s",
                   (marca, modelo, ano, placa, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Veículo atualizado.")

def excluir_veiculo():
    id = simpledialog.askstring("Excluir Veículo", "ID do veículo:")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM veiculos WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Veículo excluído.")

# ---------------------------- GUI PRINCIPAL ----------------------------

criar_banco_e_tabelas()

root = tk.Tk()
root.title("Sistema de Estacionamento")

# Botões
tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente, width=30).pack(pady=5)
tk.Button(root, text="Listar Clientes", command=listar_clientes, width=30).pack(pady=5)
tk.Button(root, text="Editar Cliente", command=editar_cliente, width=30).pack(pady=5)
tk.Button(root, text="Excluir Cliente", command=excluir_cliente, width=30).pack(pady=5)

tk.Label(root, text="").pack()  # Separador

tk.Button(root, text="Cadastrar Veículo", command=cadastrar_veiculo, width=30).pack(pady=5)
tk.Button(root, text="Listar Veículos", command=listar_veiculos, width=30).pack(pady=5)
tk.Button(root, text="Editar Veículo", command=editar_veiculo, width=30).pack(pady=5)
tk.Button(root, text="Excluir Veículo", command=excluir_veiculo, width=30).pack(pady=5)

tk.Button(root, text="Sair", command=root.quit, width=30).pack(pady=10)

root.mainloop()
