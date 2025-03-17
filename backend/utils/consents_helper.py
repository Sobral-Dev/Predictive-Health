from repositories.UserConsentRepository import UserConsentRepository
from repositories.ConsentTermRepository import ConsentTermRepository

user_consent_repo = UserConsentRepository()
consent_term_repo = ConsentTermRepository()

def get_terms(user_id):
    """
    Obtém os termos de consentimento aplicáveis ao usuário, garantindo que ele veja a versão mais recente dos termos ativos.
    """

    # Buscar os consentimentos do usuário
    user_consent = user_consent_repo.get_user_consents(user_id)

    # Buscar todos os termos de consentimento ativos
    consent_terms = consent_term_repo.find_all({"active": True})

    # Criar um dicionário de termos de consentimento (para busca rápida por ID)
    consent_terms_dict = {str(term.id): term for term in consent_terms}

    # Criar um dicionário de consentimentos do usuário para fácil acesso
    user_consents_dict = {str(consent["term_id"]): consent for consent in user_consent.consents} if user_consent else {}

    # Criar uma lista de consentimentos para retorno ao frontend
    consents_response = []

    for term_id, term in consent_terms_dict.items():
        # Obtém a versão mais recente do termo
        latest_version = max(term.versions, key=lambda v: v["version"])
        latest_version_number = latest_version["version"]

        if latest_version_number == 1:
            latest_version['description'] = None

        # Verifica se o usuário já consentiu para esse termo
        existing_consent = user_consents_dict.get(term_id)

        if existing_consent:
            # Se o usuário aceitou uma versão antiga, e há uma nova versão ativa, ele deve consentir novamente
            if existing_consent['version'] < latest_version_number:
                status = "pending"
            else:
                status = existing_consent['status'] # Mantém o status já registrado

            consents_response.append({
                "id": term_id,
                "name": term.name,
                "term_description": term.description,
                "version_description": latest_version["description"],
                "mandatory": term.mandatory,
                "version": latest_version_number,
                "status": status,
                "timestamp": existing_consent['timestamp'].isoformat()
            })
        else:
            # Se o usuário nunca consentiu, marca como "pending"
            consents_response.append({
                "id": term_id,
                "name": term.name,
                "term_description": term.description,
                "version_description": latest_version["description"],
                "mandatory": term.mandatory,
                "version": latest_version_number,
                "status": "pending",  # Indica que o usuário ainda não respondeu
                "timestamp": None
            })

    consents_response = sorted(consents_response, key=lambda x: not x["mandatory"])

    return consents_response
