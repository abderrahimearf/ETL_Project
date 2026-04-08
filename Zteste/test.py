import sqlalchemy
from sqlalchemy import create_engine, text
import urllib.parse
import pandas as pd

# --- PARAMÈTRES LOCAUX (WINDOWS) ---
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "admin", # Ton mot de passe défini dans pgAdmin
    "database": "postgres" # On commence par se connecter à la base par défaut
}

def run_test():
    print(f"--- 🔍 TEST DE CONNEXION LOCALE ---")
    
    # 1. Préparation de l'URL
    # quote_plus est important si le mot de passe contient des caractères spéciaux
    encoded_pass = urllib.parse.quote_plus(DB_CONFIG["password"])
    url = f"postgresql://{DB_CONFIG['user']}:{encoded_pass}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    
    try:
        # 2. Création de l'engine
        engine = create_engine(url)
        
        # 3. Tentative de connexion et lecture de la version
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print("✅ SUCCÈS : Connexion établie avec PostgreSQL !")
            print(f"🐘 Version détectée : {version}")
            
            # 4. Test de lecture simple (Information Schema)
            df = pd.read_sql("SELECT datname FROM pg_database LIMIT 5;", conn)
            print("\n📊 Bases de données trouvées sur ton serveur :")
            print(df)

    except Exception as e:
        print("\n❌ ÉCHEC DE LA CONNEXION")
        # On affiche l'erreur proprement
        print(f"Détail de l'erreur : {e}")
        
        print("\n💡 Pistes de résolution :")
        print("1. Vérifie que le service PostgreSQL est bien 'Démarré' dans Windows (services.msc).")
        print("2. Vérifie que le mot de passe est bien 'admin' dans pgAdmin.")
        print("3. Vérifie que le port est bien 5432 dans les propriétés du serveur pgAdmin.")

if __name__ == "__main__":
    run_test()