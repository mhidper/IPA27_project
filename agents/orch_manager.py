import time
from cis_worker import CISWorker

class IPA27Orchestrator:
    """
    Manager Agent: Coordina la actualización de todas las fuentes.
    Es el único que tú 'ejecutas', y él despierta a los especialistas.
    """
    def __init__(self):
        self.worker_cis = CISWorker()
        
    def update_all_sources(self):
        print("🚦 ORQUESTADOR: Iniciando ciclo de actualización 🚦")
        
        # 1. Update CIS (Microdatos)
        print("\n[Paso 1: CIS]")
        # Aquí el orchestrator sabe que el CIS publica el Barómetro sobre el día 1-10
        # zip_path = self.worker_cis.download_microdata("3544")
        # self.worker_cis.extract_and_organize(zip_path)
        
        # 2. Update INE (Esto ya es automático con tus Notebooks actuales)
        print("\n[Paso 2: INE / IECA]")
        print("Llamando a descargar_todos() de Notebook 01...")
        # En una arquitectura real, esto dispararía el kernel del notebook
        
        # 3. Procesamiento final (IPA27)
        print("\n[Paso 3: Cálculo Final IPA27]")
        print("Llamando a Notebook 02...")
        
        print("\n✅ CICLO COMPLETADO ✅")

if __name__ == "__main__":
    manager = IPA27Orchestrator()
    manager.update_all_sources()
