
import streamlit as st
import feedparser
from datetime import datetime, timedelta

# ---------- CONFIGURATION UI ----------
st.set_page_config(page_title="Revue de presse SIEP", page_icon="📰", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f5f8fa;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2 {
        color: #002e5d;
    }
    .stButton button {
        background-color: #0072ce;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- DONNÉES DE BASE ----------
rubriques = {
    "Travail et Insertion Socio-Professionnelle": [
        "emploi", "recherche d’emploi", "législation du travail", "contrat",
        "job étudiant", "insertion socio-professionnelle", "CISP",
        "année citoyenne", "volontariat", "rédaction de CV"
    ],
    "Enseignement de plein exercice": [
        "études", "enseignement secondaire", "enseignement supérieur",
        "enseignement qualifiant", "décret", "structure scolaire"
    ]
}

# ---------- FONCTION POUR RSS ----------
def create_rss_url(keyword, start_date, end_date):
    base_url = "https://news.google.com/rss/search?"
    query = f"q={keyword.replace(' ', '+')}+after:{start_date}+before:{end_date}"
    params = "&hl=fr&gl=BE&ceid=BE:fr"
    return base_url + query + params

def get_articles(rss_url):
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.published if 'published' in entry else ""
        })
    return articles

# ---------- UI ----------
st.title("Revue de presse 📚 - SIEP Liège")
st.markdown("Choisissez une rubrique, un mot-clé et une période pour afficher les articles belges les plus récents.")

rubrique = st.selectbox("Rubrique", list(rubriques.keys()))
keyword = st.selectbox("Mot-clé", rubriques[rubrique])

today = datetime.today()
def_start = today - timedelta(days=30)
start_date = st.date_input("Date de début", def_start)
end_date = st.date_input("Date de fin", today)

if st.button("🔍 Rechercher"):
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    url = create_rss_url(keyword, start_str, end_str)
    articles = get_articles(url)

    st.subheader(f"Résultats pour '{keyword}' entre {start_str} et {end_str}")

    if articles:
        for a in articles:
            st.markdown(f"**[{a['title']}]({a['link']})**")
            st.caption(a['date'])
            st.markdown("---")
    else:
        st.info("Aucun article trouvé pour cette période.")
