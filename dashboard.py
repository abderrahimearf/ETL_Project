import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Olist Business Intelligence", layout="wide", page_icon="📊")

# 1. PARAMÈTRES DE CONNEXION
DB_URL = "postgresql://postgres:admin@localhost:5432/Olist"

@st.cache_resource
def get_engine():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        st.stop()

engine = get_engine()

# --- FONCTION DE CHARGEMENT ---
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

# --- NAVIGATION LATERALE ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b3/Olist_logo.png", width=120)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir une vue :", ["📈 Performance Commerciale", "🚚 Logistique & Délais", "👥 Analyse Clients"])

# --- CHARGEMENT INITIAL DES DONNÉES ---
try:
    df_orders = load_data("SELECT * FROM gold.fct_orders")
    
    # --- GESTION SÉCURISÉE DU FILTRE (Correction de l'erreur) ---
    st.sidebar.divider()
    available_status = df_orders['order_status'].unique().tolist()
    
    # On vérifie si 'delivered' existe, sinon on prend tout par défaut
    default_selection = ['delivered'] if 'delivered' in available_status else available_status
    
    status_filter = st.sidebar.multiselect(
        "Filtrer par Statut :", 
        options=available_status, 
        default=default_selection
    )
    
    # Application du filtre
    df_filtered = df_orders[df_orders['order_status'].isin(status_filter)]

    # ---------------------------------------------------------
    # PAGE 1 : PERFORMANCE COMMERCIALE
    # ---------------------------------------------------------
    if page == "📈 Performance Commerciale":
        st.title("🚀 Dashboard de Performance")
        
        # KPIs en haut
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Commandes", f"{len(df_filtered)}")
        with c2:
            st.metric("Chiffre d'Affaires", f"{df_filtered['total_paid'].sum():,.0f} R$")
        with c3:
            st.metric("Panier Moyen", f"{(df_filtered['total_paid'].mean() if len(df_filtered)>0 else 0):.1f} R$")
        with c4:
            late_rate = (df_filtered['is_late'].mean() * 100) if len(df_filtered)>0 else 0
            st.metric("% Retards", f"{late_rate:.1f}%")

        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Série Temporelle des Ventes")
            df_filtered['purchase_at'] = pd.to_datetime(df_filtered['purchase_at'])
            sales_trend = df_filtered.resample('M', on='purchase_at')['total_paid'].sum().reset_index()
            fig1 = px.line(sales_trend, x='purchase_at', y='total_paid', labels={'total_paid': 'Ventes (R$)'})
            st.plotly_chart(fig1, width='stretch')
        
        with col_b:
            st.subheader("Répartition des Paiements")
            fig2 = px.histogram(df_filtered, x='max_installments', nbins=10, title="Nombre d'échéances")
            st.plotly_chart(fig2, width='stretch')

    # ---------------------------------------------------------
    # PAGE 2 : LOGISTIQUE
    # ---------------------------------------------------------
    elif page == "🚚 Logistique & Délais":
        st.title("📦 Analyse des Livraisons")
        
        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("Délai Moyen par État (jours)")
            state_data = df_filtered.groupby('order_status')['delivery_time_days'].mean().reset_index()
            fig3 = px.bar(state_data, x='order_status', y='delivery_time_days', color='delivery_time_days')
            st.plotly_chart(fig3, width='stretch')
            
        with col_r:
            st.subheader("Respect des Délais")
            late_counts = df_filtered['is_late'].value_counts().reset_index()
            late_counts['label'] = late_counts['is_late'].map({True: 'En retard', False: 'À l\'heure'})
            fig4 = px.pie(late_counts, names='label', values='count', color='label',
                          color_discrete_map={'À l\'heure': '#2ecc71', 'En retard': '#e74c3c'})
            st.plotly_chart(fig4, width='stretch')

    # ---------------------------------------------------------
    # PAGE 3 : ANALYSE CLIENTS
    # ---------------------------------------------------------
    elif page == "👥 Analyse Clients":
        st.title("👥 Profiling Clients")
        
        try:
            df_cust = load_data("SELECT * FROM gold.dim_customers")
            
            c_left, c_right = st.columns([1, 2])
            with c_left:
                st.subheader("Top 10 Villes")
                top_cities = df_cust['city'].value_counts().head(10)
                st.table(top_cities)
                
            with c_right:
                st.subheader("Répartition par État")
                fig5 = px.treemap(df_cust, path=['state_code', 'city'], title="Densité Géographique")
                st.plotly_chart(fig5, width='stretch')
        except:
            st.info("La table dim_customers n'est pas encore disponible dans le schéma gold.")

    # --- FOOTER ---
    st.sidebar.divider()
    st.sidebar.caption("Ingénierie de Données - Olist Project 2026")

except Exception as e:
    st.error("Impossible de charger les données Gold.")
    st.info("Vérifiez que vos modèles dbt ont bien été exécutés (`dbt run`).")
    st.exception(e)