import asyncio
import os
import random
from playwright.async_api import async_playwright
from pathlib import Path

async def run_cis_worker(study_map=None, user_info=None):
    output_dir = Path("G:/Mi unidad/Proyectos/IPA27_project/data/raw/cis/barómetro/")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if study_map is None:
        study_map = {
            "3540": "https://www.cis.es/es/estudios/barometro-de-enero-2026",
            "3544": "https://www.cis.es/es/estudios/barometro-de-febrero-2026"
        }
    
    if user_info is None:
        user_info = {
            "nombre": "manuel alejandro",
            "apellidos": "Hidalgo Pérez",
            "email": "mhidper@upo.es",
            "empresa": "Universidad Pablo de Olavide"
        }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for study_id, study_url in study_map.items():
            try:
                print(f"\n🚀 --- ESTUDIO {study_id} ---")
                await page.goto(study_url, wait_until="domcontentloaded")
                
                try: await page.click("button:has-text('Aceptar')", timeout=4000)
                except: pass

                # 1. Información del estudio
                print("📁 Pestaña de datos...")
                selector_tab = 'button:has-text("Información del estudio")'
                await page.wait_for_selector(selector_tab, timeout=10000)
                await page.click(selector_tab, force=True)
                
                # 2. Formulario
                print("📥 Abriendo formulario...")
                await page.click('a:has-text("Fichero datos")', timeout=10000)
                
                print(f"📝 Rellenando para {user_info['nombre']}...")
                await page.wait_for_selector("#email", timeout=10000)
                await page.fill("#email", user_info["email"])
                await page.fill("#name", user_info["nombre"])
                await page.fill("#lastName", user_info["apellidos"])
                await page.fill("#organizationName", user_info["empresa"])
                await page.click('label:has-text("Investigación")', force=True)
                await page.click('label:has-text("acepta los terminos")', force=True)
                
                print("📩 Enviando (Paso 1/2)...")
                await page.click("button:has-text('Enviar solicitud')", force=True)
                
                # 3. VERDADERA DESCARGA
                print("📩 Buscando botón final de descarga (Paso 2/2)...")
                # Selector ultra-robusto: cualquier elemento habilitado que diga 'Descargar' dentro del modal/página
                final_btn = page.locator('button:has-text("Descargar"), a:has-text("Descargar"), .btn-success').filter(visible=True).first
                await final_btn.wait_for(state="visible", timeout=30000)
                
                print("🚀 Iniciando transferencia...")
                async with page.expect_download(timeout=60000) as download_info:
                    await final_btn.click(force=True)

                download = await download_info.value
                path_zip = output_dir / f"cis_{study_id}.zip"
                await download.save_as(str(path_zip))
                print(f"✅ ¡ÉXITO! -> {path_zip.name}")
                
            except Exception as e:
                print(f"⚠️ Fallo: {e}")
                await page.screenshot(path=f"agents/error_{study_id}.png")
                continue

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_cis_worker())
