from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from repositories.ConsentTermRepository import ConsentTermRepository
from repositories.UserConsentRepository import UserConsentRepository
from models.ConsentTermModel import ConsentTermModel
import json
from utils.mongodb_indexes import create_indexes, drop_indexes

# Configuração do Flask
app = Flask(__name__)

# Instâncias dos Repositories
consent_repo = ConsentTermRepository()
user_consent_repo = UserConsentRepository()

class ConsentManager:
    """Gerencia termos de consentimento e suas versões."""

    def create_new_term(self, name: str, description: str, mandatory: bool):
        """Cria um novo termo ou adiciona uma nova versão, garantindo consistência dos dados."""

        existing_term = consent_repo.get_term_by_name(name)

        if existing_term:
            # Criar nova versão do termo
            new_version = {
                "version": len(existing_term.versions) + 1,
                "description": description,
                "created_at": datetime.utcnow(),
                "active": True
            }

            # Desativar todas as versões anteriores dentro do próprio objeto
            for version in existing_term.versions:
                version["active"] = False

            # Adicionar nova versão
            existing_term.versions.append(new_version)
            existing_term.active = True  
            existing_term.mandatory = mandatory  # Atualiza a obrigatoriedade  

            # Atualizar no banco de dados
            consent_repo.update_term(existing_term)

            print(f"✅ Nova versão adicionada ao termo: {name}, agora na versão {new_version['version']}.")

            term_id = existing_term.id
            version = new_version["version"]
        else:
            # Criar um novo termo do zero
            new_term = ConsentTermModel(
                name=name,
                description=description,
                mandatory=mandatory,
                created_at=datetime.utcnow(),
                active=True,
                versions=[{
                    "version": 1,
                    "description": description,
                    "created_at": datetime.utcnow(),
                    "active": True
                }]
            )

            consent_repo.insert_term(new_term)

            print(f"✅ Novo termo criado: {name}.")

            term_id = new_term.id
            version = 1

        # Atualizar os consentimentos dos usuários para refletir a nova versão
        self.update_user_consents(term_id, version)

    def update_user_consents(self, term_id, version):
        """Atualiza os consentimentos dos usuários com a nova versão."""

        users = user_consent_repo.find_all()

        for user_data in users:
            user_id = user_data.user_id

            # Se o termo for obrigatório, o status do consentimento deve ser "granted" automaticamente.
            status = "pending"

            user_consent_repo.update_or_insert_user_consent(
                user_id=str(user_id),
                term_id=str(term_id),
                status=status,
                version=version
            )

        print(f"✅ Atualizados os consentimentos para a nova versão {version} do termo {term_id}.")

    def list_terms_update_suggestions(self, prompt = bool):
        """Lista todas as sugestões de atualização dos termos presentes em arquivo JSON"""

        try:
            # Ler os dados do arquivo JSON
            with open("terms_update_suggestions.json", "r", encoding="utf-8") as file:
                update_suggestions = json.load(file)

            count = 0
            if prompt:
                for update in update_suggestions:
                    update["id"] = count
                    print(f'\nID: {update["id"]}')
                    print(f'Name: {update["name"]}')
                    print(f'Description: {update["description"]}\n')
                    print("---")
                    count = count + 1

                print('\n')
                decision = input("• Deseja implementar alguma das sugestões? (s/n): ").strip().lower() == "s"
                
                if decision:
                    id = int(input("Digite o ID da sugestão desejada: ").strip()) 
                    mandatory = input("Deseja que seja obrigatório? (s/n): ").strip().lower() == "s"

                    result = next((update for update in update_suggestions if update["id"] == id), None)
                    print(f'\n{result}\n')

                    if result is not None:
                        self.create_new_term(name=result["name"], description=result["description"], mandatory=mandatory)
                    else:
                        print("❌ ID inválido! Tente novamente.")

            else:
                return update_suggestions

        except Exception as e:
            print(f"❌ Erro ao carregar as sugestões de atualização de versão dos termos: {str(e)}")

    def list_terms(self):
        """Lista todos os termos de consentimento cadastrados."""
        terms = consent_repo.get_all_terms()
        for term in terms:
            print(f"📜 {term.name} (Ativo: {term.active}) - Versões: {len(term.versions)}")

    def list_user_consents(self):
        """Lista os consentimentos de todos os usuários."""
        terms = user_consent_repo.find_all()
        for term in terms:
            print(f"👤 {term.to_dict()}")

    def save_terms_to_json(filename="terms_database.json"):
        """Salva os termos existentes no MongoDB em um arquivo JSON."""

        terms_objects = consent_repo.get_all_terms()

        terms_json = []
        for term in terms_objects:
            term = term.to_dict()
            terms_json.append(term)
    
        for term in terms_json:
            del term['id']

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(terms_json, file, indent=4, ensure_ascii=False)
            print(f"✅ Termos presentes no MongoDB salvos em {filename} com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao salvar termos presentes no MongoDB: {e}")

    def save_user_consents_to_json(filename="user_consents_database.json"):
        """Salva os consentimentos de usuários existentes no MongoDB em um arquivo JSON."""

        terms_objects = user_consent_repo.find_all()

        terms_json = []
        for term in terms_objects:
            term = term.to_dict()
            terms_json.append(term)

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(terms_json, file, indent=4, ensure_ascii=False)
            print(f"✅ Consentimentos de usuários presentes no MongoDB salvos em {filename} com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao salvar consentimentos de usuários presentes no MongoDB: {e}")

# Criar instância do ConsentManager
manager = ConsentManager()

# =================== ROTAS DO FLASK ===================

# Rota Raíz
@app.route('/')
def home():

    return render_template_string(
            '<h1>Welcome to the Consent Manager!</h1>'
            '<p>Use the following endpoints:</p>'
            '<ul>'
                '<li><a href="http://127.0.0.1:5200/list_terms">Listar termos de consentimento</a></li>'
                '<li><a href="http://127.0.0.1:5200/list_user_consents">Listar consentimentos de usuários</a></li>'
                '<li><a href="http://127.0.0.1:5200/list_update_suggestions">Listar sugestões de atualização de termos</a></li>'
            '</ul>'
    )

@app.route("/list_terms", methods=["GET"])
def list_terms():
    """Endpoint para listar termos de consentimento."""
    terms = consent_repo.get_all_terms()

    list_terms = []
    for term in terms:
        term_dict = term.to_dict()
        list_terms.append(term_dict)

    return jsonify(list_terms), 200

@app.route("/list_user_consents", methods=["GET"])
def list_user_consents():
    """Endpoint para listar consentimentos de usuários."""
    terms = user_consent_repo.find_all()
    
    list_terms = []
    for term in terms:
        term_dict = term.to_dict()
        list_terms.append(term_dict)

    return jsonify(list_terms), 200

@app.route("/list_update_suggestions", methods=["GET"])
def list_update_suggestions():
    update_suggestions = manager.list_terms_update_suggestions(prompt=False)

    return jsonify(update_suggestions), 200

# =================== MODO INTERATIVO ===================
def print_options():
    print("\n📌 Opções:")
    print("1️⃣  Criar um novo Termo")
    print("2️⃣  Listar Termos")
    print("3️⃣  Listar Consentimentos de Usuários")
    print("4️⃣  Exportar JSON database de Termos")
    print("5️⃣  Exportar JSON database de Consentimentos de Usuários")
    print("6️⃣  Atualizar um termo a partir de uma das sugestões")

    return input("Escolha uma opção: \n\n")

def interactive_mode():
    """Modo interativo no terminal para gerenciar os termos de consentimento."""
    while True:
        
        option = print_options()

        if option == "1":
            name = input("Nome do termo: ")
            description = input("Descrição do termo: ")
            mandatory = input("É obrigatório? (s/n): ").strip().lower() == "s"
            manager.create_new_term(name, description, mandatory)

            option = print_options()

        elif option == "2":
            manager.list_terms()

            option = print_options()

        elif option == "3":
            manager.list_user_consents()

            option = print_options()

        elif option == "4":
            manager.save_terms_to_json()

            option = print_options()

        elif option == "5":
            manager.save_user_consents_to_json()

            option = print_options()

        elif option == "6":
            manager.list_terms_update_suggestions(prompt=True)

            option = print_options()

        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    # Iniciar o Flask em um thread separada
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(debug=True, port=5200, use_reloader=False))
    flask_thread.start()

    # Rodar modo interativo no terminal
    interactive_mode()
