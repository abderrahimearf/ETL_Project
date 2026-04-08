import kagglehub
import shutil
import os
import glob

# --- CONFIGURATION ---
# Le dossier où tu veux stocker tes CSV sur ton PC
TARGET_FOLDER = os.path.join(os.getcwd(), 'data')

def download_and_organize():
    print("🌍 Démarrage du téléchargement depuis Kaggle...")
    
    # 1. Téléchargement (dans le cache système)
    cache_path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")
    print(f"   ⬇️  Données récupérées dans le cache.")

    # 2. Préparation du dossier local 'data'
    # On supprime le dossier s'il existe déjà pour repartir à zéro (propre)
    if os.path.exists(TARGET_FOLDER):
        shutil.rmtree(TARGET_FOLDER)
    os.makedirs(TARGET_FOLDER)
    print(f"   📂 Dossier local créé : {TARGET_FOLDER}")

    # 3. Copie des fichiers CSV
    csv_files = glob.glob(os.path.join(cache_path, "*.csv"))
    
    if not csv_files:
        print("   ❌ Erreur : Aucun fichier CSV trouvé dans le téléchargement.")
        return

    print(f"   🚚 Copie de {len(csv_files)} fichiers...")
    for file in csv_files:
        shutil.copy(file, TARGET_FOLDER)
        print(f"      📄 {os.path.basename(file)}")

    print("\n✅ Téléchargement terminé. Les fichiers sont dans le dossier 'data'.")

if __name__ == "__main__":
    download_and_organize()