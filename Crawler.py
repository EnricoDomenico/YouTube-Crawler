from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--incognito")
options.add_argument("--disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


driver = webdriver.Chrome(options=options)
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

try:
    # Abre o YouTube
    driver.get("https://www.youtube.com")
    
    
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "search_query"))
    )
    print("YouTube carregado com sucesso!")

    #Pesquisa 
    search_term = "vermillion Slipknot" 
    search_box.send_keys(search_term)
    search_box.submit()

   
    videos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "video-title"))
    )
    print(f"Encontrados {len(videos)} vídeos para o termo: {search_term}")

    
    video_link = videos[0].get_attribute("href")
    print(f"Baixando o vídeo")

   
    if video_link:
        ydl_opts = {
            'format': 'bestaudio/best',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  
                'preferredquality': '192',  
            }],
            'outtmpl': '%(title)s.%(ext)s',  
            'ffmpeg_location': r"E:\Users\ENRICO\FFMPEG\ffmpeg-7.1-full_build\bin"  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
    else:
        print("Nenhum link")

finally:
    
    driver.quit()
