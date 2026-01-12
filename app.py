import streamlit as st
import requests
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="RAG Semantic Search",
    page_icon="🔍",
    layout="wide"
)

# URL de base de l'API
API_BASE_URL = "http://127.0.0.1:8000/api"

# Session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Fonction pour obtenir les headers avec token
def get_headers():
    if st.session_state.token:
        return {
            "Authorization": f"Bearer {st.session_state.token}",
            "Content-Type": "application/json"
        }
    return {"Content-Type": "application/json"}


# Sidebar - Authentification
with st.sidebar:
    st.title("🔐 Authentification")

    if not st.session_state.token:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Se connecter")

            if submit:
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/token/",
                        json={"username": username, "password": password}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data.get('access')
                        st.success("✅ Connecté avec succès!")
                        st.rerun()
                    else:
                        st.error("❌ Échec de connexion")
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
    else:
        st.success("✅ Connecté")
        if st.button("Se déconnecter"):
            st.session_state.token = None
            st.session_state.chat_history = []
            st.rerun()

    st.divider()

    # Configuration de l'API
    st.subheader("⚙️ Configuration")
    api_url = st.text_input("URL de l'API", value=API_BASE_URL)
    if api_url != API_BASE_URL:
        API_BASE_URL = api_url

# Titre principal
st.title("🔍 RAG Semantic Search Interface")
st.markdown("Interface complète pour votre API de recherche sémantique avec RAG")

# Tabs principales
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📤 Upload",
    "💬 RAG Chat",
    "🔍 Recherche",
    "📚 Documents",
    "🔗 Similaires",
    "📜 Historique"
])

# TAB 1 : Upload de documents
with tab1:
    st.header("📤 Uploader un document PDF")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choisissez un fichier PDF",
            type=['pdf'],
            help="Sélectionnez un document PDF à uploader"
        )

        title = st.text_input(
            "Titre du document",
            placeholder="Ex: Rapport sur la violence conjugale"
        )

        if st.button("📤 Uploader", type="primary", disabled=not uploaded_file):
            if not title:
                st.warning("⚠️ Veuillez entrer un titre")
            else:
                try:
                    files = {'file': uploaded_file}
                    data = {'title': title}

                    headers = {}
                    if st.session_state.token:
                        headers["Authorization"] = f"Bearer {st.session_state.token}"

                    with st.spinner("Upload en cours..."):
                        response = requests.post(
                            f"{API_BASE_URL}/documents/",
                            files=files,
                            data=data,
                            headers=headers
                        )

                    if response.status_code in [200, 201]:
                        st.success("✅ Document uploadé avec succès!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Erreur: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")

    with col2:
        st.info("""
        **Instructions:**
        1. Sélectionnez un PDF
        2. Donnez-lui un titre
        3. Cliquez sur Uploader

        Le document sera traité et indexé automatiquement.
        """)

# TAB 2 : RAG Chat
with tab2:
    st.header("💬 RAG - Question-Réponse sur vos documents")

    st.markdown("""
    Posez des questions et obtenez des réponses basées sur vos documents avec les sources.
    """)

    # Zone de chat
    chat_container = st.container()

    with chat_container:
        # Afficher l'historique des messages
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"**🧑 Vous:** {message['content']}")
            else:
                st.markdown(f"**🤖 Assistant:** {message['content']}")
                if 'sources' in message:
                    with st.expander("📚 Sources utilisées"):
                        for i, source in enumerate(message['sources'], 1):
                            st.markdown(f"**{i}. {source.get('title')}** (Score: {source.get('score', 0):.3f})")
                            st.text(source.get('excerpt', ''))
                st.divider()

    # Formulaire de question
    with st.form(key="rag_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            question = st.text_area(
                "Posez votre question",
                placeholder="Ex: Quelles sont les mesures de protection pour les victimes de violence conjugale?",
                height=100,
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            num_sources = st.number_input("Sources", min_value=1, max_value=10, value=3)
            submit = st.form_submit_button("💬 Envoyer", type="primary", use_container_width=True)

        if submit and question:
            # Ajouter la question à l'historique
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question
            })

            try:
                with st.spinner("🔍 Recherche dans les documents et génération de la réponse..."):
                    # Étape 1: Recherche sémantique
                    search_response = requests.post(
                        f"{API_BASE_URL}/seacrh/semantic/",
                        json={
                            "query": question,
                            "limit": num_sources,
                            "threshold": 0.3
                        },
                        headers=get_headers()
                    )

                    if search_response.status_code == 200:
                        search_data = search_response.json()
                        results = search_data.get('results', [])

                        if results:
                            # Construire le contexte à partir des résultats
                            context = "\n\n".join([
                                f"Document: {r.get('title')}\n{r.get('excerpt', '')}"
                                for r in results
                            ])

                            # Étape 2: Appel à l'endpoint RAG (si vous l'avez)
                            # Sinon, on simule une réponse basée sur le contexte
                            try:
                                rag_response = requests.post(
                                    f"{API_BASE_URL}/rag/ask/",
                                    json={
                                        "question": question,
                                        "context": context
                                    },
                                    headers=get_headers()
                                )

                                if rag_response.status_code == 200:
                                    answer = rag_response.json().get('answer', 'Pas de réponse générée')
                                else:
                                    # Réponse de secours si l'endpoint RAG n'existe pas
                                    answer = f"Voici les informations trouvées dans {len(results)} documents pertinents."
                            except:
                                # Réponse de secours
                                answer = f"Voici les informations trouvées dans {len(results)} documents pertinents."

                            # Ajouter la réponse à l'historique
                            st.session_state.chat_history.append({
                                'role': 'assistant',
                                'content': answer,
                                'sources': results
                            })

                            st.rerun()
                        else:
                            st.warning("⚠️ Aucun document pertinent trouvé pour répondre à votre question")
                    else:
                        st.error("❌ Erreur lors de la recherche")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

    # Bouton pour effacer l'historique
    if st.session_state.chat_history:
        if st.button("🗑️ Effacer l'historique du chat"):
            st.session_state.chat_history = []
            st.rerun()

# TAB 3 : Recherche sémantique
with tab3:
    st.header("🔍 Recherche sémantique avancée")

    query = st.text_area(
        "Entrez votre texte de recherche",
        placeholder="Ex: Je recherche des informations sur la violence conjugale et les mesures de protection...",
        height=150
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        limit = st.number_input("Nombre de résultats", min_value=1, max_value=20, value=5)

    with col2:
        threshold = st.slider("Seuil de similarité", 0.0, 1.0, 0.3, 0.05)

    with col3:
        search_mode = st.selectbox("Mode de recherche", ["documents", "chunks"])

    if st.button("🔍 Rechercher", type="primary", disabled=not query):
        try:
            with st.spinner("Recherche en cours..."):
                response = requests.post(
                    f"{API_BASE_URL}/search/semantic/",
                    json={
                        "query": query,
                        "limit": limit,
                        "threshold": threshold,
                        "search_mode": search_mode
                    },
                    headers=get_headers()
                )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                if results:
                    st.success(f"✅ {len(results)} résultats trouvés")

                    for i, result in enumerate(results, 1):
                        with st.expander(
                                f"#{i} - {result.get('title', 'Sans titre')} - Score: {result.get('score', 0):.3f}"):
                            st.markdown(f"**ID:** {result.get('id')}")
                            st.markdown(f"**Score de similarité:** {result.get('score', 0):.3f}")
                            st.markdown(f"**Extrait:**")
                            st.text(result.get('excerpt', 'Pas d\'extrait disponible'))
                else:
                    st.warning("⚠️ Aucun résultat trouvé")
            else:
                st.error(f"❌ Erreur: {response.status_code}")
                st.json(response.json())
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

# TAB 4 : Liste des documents
with tab4:
    st.header("📚 Mes documents")

    if st.button("🔄 Rafraîchir la liste"):
        try:
            response = requests.get(
                f"{API_BASE_URL}/documents/",
                headers=get_headers()
            )
            if response.status_code == 200:
                st.session_state.documents = response.json()
                st.success("✅ Liste mise à jour")
            else:
                st.error("❌ Erreur lors de la récupération")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

    if st.session_state.documents:
        st.write(f"**Total: {len(st.session_state.documents)} documents**")

        for doc in st.session_state.documents:
            with st.expander(f"📄 {doc.get('title', 'Sans titre')}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**ID:** {doc.get('id')}")
                    st.markdown(f"**Titre:** {doc.get('title')}")
                    st.markdown(f"**Uploadé le:** {doc.get('uploaded_at', 'N/A')}")
                    if doc.get('file'):
                        st.markdown(f"**Fichier:** [{doc.get('file')}]({doc.get('file')})")

                with col2:
                    if st.button(f"🗑️ Supprimer", key=f"del_{doc.get('id')}"):
                        try:
                            response = requests.delete(
                                f"{API_BASE_URL}/documents/{doc.get('id')}/",
                                headers=get_headers()
                            )
                            if response.status_code == 204:
                                st.success("✅ Supprimé")
                                st.rerun()
                            else:
                                st.error("❌ Erreur")
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
    else:
        st.info("ℹ️ Aucun document disponible. Cliquez sur 'Rafraîchir' ou uploadez un document.")

# TAB 5 : Documents similaires
with tab5:
    st.header("🔗 Trouver des documents similaires")

    st.markdown("""
    Cette fonction trouve les documents similaires à un document donné en utilisant les embeddings.
    """)

    doc_id = st.number_input(
        "ID du document de référence",
        min_value=1,
        step=1,
        help="Entrez l'ID du document pour lequel vous voulez trouver des documents similaires"
    )

    if st.button("🔗 Trouver des similaires", type="primary"):
        try:
            with st.spinner("Recherche en cours..."):
                response = requests.get(
                    f"{API_BASE_URL}/documents/{doc_id}/similar/",
                    headers=get_headers()
                )

            if response.status_code == 200:
                similar_docs = response.json()

                if similar_docs:
                    st.success(f"✅ {len(similar_docs)} documents similaires trouvés")

                    for i, doc in enumerate(similar_docs, 1):
                        with st.expander(
                                f"#{i} - {doc.get('title', 'Sans titre')} - Distance: {doc.get('distance', 0):.3f}"):
                            st.markdown(f"**ID:** {doc.get('id')}")
                            st.markdown(f"**Titre:** {doc.get('title')}")
                            st.markdown(f"**Distance cosinus:** {doc.get('distance', 0):.4f}")
                            st.markdown(f"**Similarité:** {(1 - doc.get('distance', 0)) * 100:.2f}%")
                else:
                    st.warning("⚠️ Aucun document similaire trouvé")
            else:
                st.error(f"❌ Erreur: {response.status_code}")
                st.json(response.json())
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

# TAB 6 : Historique des recherches
with tab6:
    st.header("📜 Historique des recherches")

    if st.button("🔄 Charger l'historique"):
        try:
            response = requests.get(
                f"{API_BASE_URL}/search/history/",
                headers=get_headers()
            )

            if response.status_code == 200:
                history = response.json()

                if history:
                    st.success(f"✅ {len(history)} recherches dans l'historique")

                    for i, search in enumerate(history, 1):
                        with st.expander(
                                f"#{i} - {search.get('query', 'Sans titre')[:50]}... ({search.get('created_at', 'N/A')})"):
                            st.markdown(f"**Query:** {search.get('query')}")
                            st.markdown(f"**Date:** {search.get('created_at')}")
                            st.markdown(f"**Nombre de résultats:** {search.get('results_count', 0)}")

                            if search.get('results'):
                                st.markdown("**Résultats:**")
                                for res in search.get('results', []):
                                    st.markdown(f"- {res.get('title')} (Score: {res.get('score', 0):.3f})")
                else:
                    st.info("ℹ️ Aucune recherche dans l'historique")
            else:
                st.error(f"❌ Erreur: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

    st.divider()

    if st.button("🗑️ Effacer tout l'historique", type="secondary"):
        try:
            response = requests.delete(
                f"{API_BASE_URL}/search/history/clear/",
                headers=get_headers()
            )
            if response.status_code == 204:
                st.success("✅ Historique effacé")
            else:
                st.error("❌ Erreur lors de la suppression")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>RAG Semantic Search Interface v2.0 | Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)