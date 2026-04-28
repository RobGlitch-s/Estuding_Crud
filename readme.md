# 📚 Projeto: App CRUD de Alunos  
**Tecnologias:** Python + SQLite + CustomTkinter  

---

## 🚀 1. Início do Projeto

**Requisito inicial:**
Criar um aplicativo simples com operações CRUD utilizando:
- Python
- SQLite
- CustomTkinter

**Arquitetura definida:**
- `database.py` → Backend (operações com banco de dados)
- `app.py` → Frontend (interface gráfica)
- `main.py` → Inicialização do sistema

**Modelo inicial de dados:**
- `id` (automático)
- `nome`
- `idade`

---

## 🧱 2. Definição do Modelo Real

**Alteração de requisito:**
A aplicação passou a trabalhar com uma tabela de alunos contendo:
- `nome`
- `RA` (chave primária)
- `data de nascimento`

**Mudanças aplicadas:**
- `RA` definido como `PRIMARY KEY`
- Estrutura da tabela ajustada para `alunos`

---

## 🖱️ 3. Melhoria: Seleção de Registros

**Requisito:**
Adicionar seleção de registros na interface

**Implementação:**
- Componente `Treeview` (tabela)
- Seleção de aluno via clique
- Preenchimento automático dos campos do formulário
- Função `on_select`

**Resultado:**
CRUD passou a operar com seleção real de registros

---

## 🔢 4. Alteração do RA (Automático)

**Requisito:**
RA deve ser automático e único

**Implementação:**
- `RA` alterado para `INTEGER AUTOINCREMENT`
- Remoção do campo RA do formulário
- Controle totalmente interno pelo banco

---

## 📅 5. Melhoria na Data de Nascimento

**Problema:**
- Formato inválido
- Dependência do uso de `/`

**Solução:**
- Validação com `datetime`
- Conversão de formatos:
  - Interface: `DD/MM/AAAA`
  - Banco: `YYYY-MM-DD`
- Rejeição de:
  - Datas inválidas
  - Datas futuras

---

## ✍️ 6. UX da Data (Máscara)

**Requisito:**
Permitir digitação sem precisar inserir `/`

**Implementação:**
- Máscara automática de data
- Entrada apenas de números
- Formatação automática

**Exemplo:**
Entrada: 18082000
Saída: 18/08/2000

---

## 🔒 7. Boas Práticas (UX + Segurança)

**Melhorias:**
- Bloqueio de letras no campo de data
- Validação com `datetime.strptime`
- Verificação de data futura

---

## 📆 8. Melhorias Opcionais Implementadas

**Recurso adicional:**
Date Picker (calendário)

**Implementação:**
- Biblioteca `tkcalendar`
- Botão "Selecionar Data"
- Popup com calendário
- Preenchimento automático do campo

---

## ✅ 9. Versão Final do Sistema

### Funcionalidades

- CRUD completo de alunos
- RA automático (chave primária)
- Nome obrigatório
- Data de nascimento com:
  - Máscara automática
  - Validação
  - Calendário interativo
  - Conversão de formatos

### Interface

- CustomTkinter
- Treeview (tabela)
- Seleção de registros

---

## 🔄 Fluxo do Sistema

```text
CREATE → VALIDAR → CONVERTER → INSERIR  
READ   → LISTAR NA TABELA  
UPDATE → SELECIONAR → EDITAR → SALVAR  
DELETE → SELECIONAR → CONFIRMAR → REMOVER  
