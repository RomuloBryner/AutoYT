import os
import time
import datetime
import json
import random
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import subprocess

# Credenciales de la API de YouTube
CLIENT_SECRETS_FILE = "./client_secret_345439363904-dmmsu8rbhf9e7ijru33eeidl0ogfpg8o.apps.googleusercontent.com.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Directorio de música
MUSIC_DIR = "./musica"

# Directorio a observar
WATCH_DIR = "C://Users//romul//Videos//Radeon ReLive//Rocket League"

# Archivo para almacenar la última vez que se subió un video
DATA_FILE = "data.json"

# Carpeta para videos redimensionados
RESIZED_VIDEOS_DIR = "./pendiente"

# Carpeta para mover los videos subidos
UPLOADED_VIDEOS_DIR = "./subidos"

# Contador de clips subidos
CLIPS_SUBIDOS = 0

# Dirección del video original
VIDEO_PATH_ORIGIN = ""

# Carpeta para videos utilizados
USED_VIDEOS_DIR = "./usados"

# Variable para almacenar la ruta del video redimensionado
RESIZED_VIDEO_PATH = ""

# Créditos de la música
music_credit = ""

def get_song_credits(song_name):
    # Define los créditos de cada canción
    song_credits = {
        "5% TINT.mp3": {
            "Canción": "5% TINT",
            "Artista": "Travis Scott",
            "Album": "ASTROWORLD",
            "Licenciado para YouTube por": "Epic Records"
        },
        "20 Min.mp3": {
            "Canción": "20 Min",
            "Artista": "Lil Uzi Vert",
            "Album": "Luv Is Rage 2",
            "Licenciado para YouTube por": "Atlantic Records"
        },
        "After Party.mp3": {
            "Canción": "After Party",
            "Artista": "Don Toliver",
            "Album": "Heaven or Hell",
            "Licenciado para YouTube por": "Atlantic Records"
        },
        "Bound 2.mp3": {
            "Canción": "Bound 2",
            "Artista": "Kanye West",
            "Album": "Yeezus",
            "Licenciado para YouTube por": "UMG (en nombre de Roc-A-Fella)"
        },
        "Cardigan - Don Toliver.mp3": {
            "Canción": "Cardigan",
            "Artista": "Don Toliver",
            "Album": "Heaven or Hell",
            "Licenciado para YouTube por": "Atlantic Records"
        },
        "fukumean.mp3": {
            "Canción": "fukumean",
            "Artista": "Fukin Uzi",
            "Album": "Desconocido",
            "Licenciado para YouTube por": "Desconocido"
        },
        "His & Hers (feat. Don Toliver & Lil Uzi Vert).mp3": {
            "Canción": "His & Hers",
            "Artista": "Internet Money",
            "Album": "B4 The Storm",
            "Licenciado para YouTube por": "TenThousand Projects, LLC under exclusive license to Internet Money Records"
        },
        "K-pop feat Bad Bunny The Weeknd - Travis Scott Bad Bunny The Weeknd": {
            "Canción": "K-pop",
            "Artista": "Travis Scott",
            "Album": "Desconocido",
            "Licenciado para YouTube por": "Desconocido"
        },
        "Like That.mp3": {
            "Canción": "Like That",
            "Artista": "Doja Cat",
            "Album": "Hot Pink",
            "Licenciado para YouTube por": "Kobalt (AWAL Digital Limited)"
        },
        "ORANGE SODA.mp3": {
            "Canción": "ORANGE SODA",
            "Artista": "Baby Keem",
            "Album": "Die for My Bitch",
            "Licenciado para YouTube por": "UMG (en nombre de Columbia)"
        },
        "OUTWEST.mp3": {
            "Canción": "OUT WEST",
            "Artista": "Jackboys",
            "Album": "JACKBOYS",
            "Licenciado para YouTube por": "SME (en nombre de Cactus Jack / Epic)"
        },
        "Popular (From The Idol Vol. 1 (Music from the HBO Original Series))": {
            "Canción": "Popular",
            "Artista": "The Kid LAROI",
            "Album": "The Idol Vol. 1",
            "Licenciado para YouTube por": "SME (en nombre de Columbia)"
        },
        "Raindrops (Insane).mp3": {
            "Canción": "Raindrops (Insane)",
            "Artista": "ZAEHD & CEO",
            "Album": "Do It Again",
            "Licenciado para YouTube por": "Create Music Group, Inc."
        },
        "See You Again.mp3": {
            "Canción": "See You Again",
            "Artista": "Tyler, The Creator",
            "Album": "Igor",
            "Licenciado para YouTube por": "SME (en nombre de Columbia)"
        },
        "Sky.mp3": {
            "Canción": "Sky",
            "Artista": "Playboi Carti",
            "Album": "Whole Lotta Red",
            "Licenciado para YouTube por": "UMG (en nombre de AWGE Label); Abramus Digital, LatinAutorPerf, UNIAO BRASILEIRA DE EDITORAS DE MUSICA - UBEM, LatinAutor - UMPG, UMPG Publishing y 3 sociedades de derechos musicales"
        },
        "Solo.mp3": {
            "Canción": "Solo",
            "Artista": "Frank Ocean",
            "Album": "Blonde",
            "Licenciado para YouTube por": "UMG (en nombre de Blonde)"
        },
        "Space Cadet.mp3": {
            "Canción": "Space Cadet",
            "Artista": "Metro Boomin",
            "Album": "NOT ALL HEROES WEAR CAPES",
            "Licenciado para YouTube por": "UMG (en nombre de Republic); AMRA, UMPI, Kobalt Music Publishing, LatinAutorPerf, LatinAutor - UMPG y 8 sociedades de derechos musicales"
        },
        "TELEKINESIS (feat. SZA & Future).mp3": {
            "Canción": "TELEKINESIS",
            "Artista": "Internet Money",
            "Album": "B4 The Storm",
            "Licenciado para YouTube por": "TenThousand Projects, LLC under exclusive license to Internet Money Records"
        },
        "Watch This - Arizonatears Pluggnb Remix - Lil Uzi Vert sped up nightcore ARIZONATEARS": {
            "Canción": "Watch This (Pluggnb Remix)",
            "Artista": "Arizonatears",
            "Album": "Watch This",
            "Licenciado para YouTube por": "Desconocido"
        },
        "Watch This (ARIZONATEARS Pluggnb Remix)": {
            "Canción": "Watch This",
            "Artista": "Arizonatears",
            "Album": "Watch This",
            "Licenciado para YouTube por": "Desconocido"
        },
    }
    return song_credits.get(song_name, {})

# Clase para manejar eventos de cambio en el sistema de archivos
class MyHandler(FileSystemEventHandler):
    print("Iniciando observador de cambios en el sistema de archivos...")

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp4"):
            print(f"Detectado nuevo video: {event.src_path}")
            # Redimensionar el video y agregar música
            try:
                resize_and_add_music(event.src_path)
                VIDEO_PATH_ORIGIN = event.src_path
                move_resized_video(VIDEO_PATH_ORIGIN, USED_VIDEOS_DIR)
            except Exception as e:
                print(f"Error al redimensionar y agregar música al video: {str(e)}")

    def redimensionar_videos_existente(self):
        for file in os.listdir(WATCH_DIR):
            if file.endswith(".mp4"):
                print(f"Redimensionando video existente: {file}")
                try:
                    resize_and_add_music(os.path.join(WATCH_DIR, file))
                    VIDEO_PATH_ORIGIN = os.path.join(WATCH_DIR, file)
                    move_resized_video(VIDEO_PATH_ORIGIN, USED_VIDEOS_DIR)
                except Exception as e:
                    print(f"Error al redimensionar y agregar música al video existente: {str(e)}")
    
    def realentizar_y_agregar_reverb(self):
        for file in os.listdir(MUSIC_DIR):
            if file.endswith(".mp3") and "_slowed_reverb.mp3" not in file:
                print(f"Realentizando música existente y agregando reverb: {file}")
                try:
                    music_path = os.path.join(MUSIC_DIR, file)
                    output_path = os.path.join(MUSIC_DIR, os.path.splitext(file)[0] + "_slowed_reverb.mp3")
                    cmd = f'ffmpeg -i "{music_path}" -af "aecho=0.8:0.9:1000:0.3" -filter:a "atempo=0.8" -vn "{output_path}"'
                    subprocess.run(cmd, shell=True)
                except Exception as e:
                    print(f"Error al realentizar música existente y agregar reverb: {str(e)}")



# Función para seleccionar una canción aleatoria del directorio de música
def select_random_song():
    music_dir = "./musica"
    music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]
    if music_files:
        selected_song = random.choice(music_files)
        song_path = os.path.join(music_dir, selected_song)
        # Obtener los créditos de la canción seleccionada
        song_credits = get_song_credits(selected_song)
        return song_path, song_credits
    else:
        print("No se encontraron archivos de música en el directorio especificado.")
        return None, None

def delete_original_video(video_path):
    print("Eliminando video original...")
    os.remove(video_path)

def move_resized_video(video_path, destination_dir):
    try:
        if os.path.exists(video_path):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            move(video_path, os.path.join(destination_dir, os.path.basename(video_path)))
            print(f"Video movido a la carpeta de videos utilizados: {os.path.join(destination_dir, os.path.basename(video_path))}")
            return True
        else:
            print("El video redimensionado no existe en la ubicación especificada.")
            return False
    except Exception as e:
        print(f"Error al mover el video redimensionado: {str(e)}")
        return False

def resize_and_add_music(video_path):
    global CLIPS_SUBIDOS
    global RESIZED_VIDEO_PATH
    print("Redimensionando video al formato 9:16, agregando marca de agua y concatenando con el outro...")
    
    # Obtener la duración total del video
    duration_cmd = f'ffprobe -i "{video_path}" -show_entries format=duration -v quiet -of csv="p=0"'
    duration = float(subprocess.check_output(duration_cmd, shell=True))

    # Calcular el punto de inicio para los últimos 15 segundos
    start_time = max(0, duration - 20)

    # Obtener la ruta de la música y los créditos de la canción
    music_path, song_credits = select_random_song()
    if music_path:
        # Redimensionar el video y agregar música
        output_path = os.path.join(RESIZED_VIDEOS_DIR, os.path.basename(video_path) + "_resized_with_music.mp4")
        cmd = f'ffmpeg -ss {start_time} -i "{video_path}" -t 00:00:30 -i "{music_path}" -filter:v "scale=-1:1920,crop=1080:1920" -c:v libx264 -preset veryfast -c:a aac -strict experimental -b:a 192k -shortest -map 0:v -map 1:a "{output_path}"'
        subprocess.run(cmd, shell=True)
        RESIZED_VIDEO_PATH1 = output_path
        
        # Agregar la marca de agua al video redimensionado
        watermark_path = "./logo.png"  # Reemplaza con la ruta de tu marca de agua
        output_with_watermark_path = os.path.splitext(output_path)[0] + "_with_watermark.mp4"
        cmd = (
            f'ffmpeg -i "{output_path}" -i "{watermark_path}" '
            '-filter_complex "[0:v][1:v]overlay=W-w-10:10[v]" '
            '-map "[v]" -map 0:a -c:v libx264 -preset veryfast -c:a copy '
            f'"{output_with_watermark_path}"'
        )
        subprocess.run(cmd, shell=True)
        RESIZED_VIDEO_PATH = output_with_watermark_path
        
        # Eliminar el video original
        os.remove(RESIZED_VIDEO_PATH1)


# Función para generar un título dinámico
def generate_dynamic_title():
    options = [
        "¡Los mejores momentos de Rocket League!",
        "Increíbles jugadas en Rocket League",
        "Domina el campo de juego en Rocket League",
        "Rocket League: ¡Aéreos impresionantes!",
        "Las jugadas más épicas de Rocket League",
        "¡Goles alucinantes en Rocket League!",
        "Desafía la gravedad en Rocket League",
        "Rocket League: ¡Acción sin límites!",
        "La emoción de Rocket League en cada gol",
        "¡Prepárate para la adrenalina de Rocket League!"
    ]
    return random.choice(options)

# Función para generar una descripción dinámica
def generate_dynamic_description():
    options = [
        "¡Disfruta de este emocionante clip de Rocket League! ¿Quién dijo que el fútbol y los coches no van juntos?",
        "¡No te pierdas estas jugadas asombrosas en Rocket League! ¡Prepárate para la acción más intensa!",
        "Entra en el mundo de Rocket League con este increíble clip. ¡Prepárate para la acción y los goles más emocionantes!",
        "¿Buscas adrenalina? ¡Este clip de Rocket League es justo lo que necesitas! ¡Goles, aéreos y mucha acción te esperan!",
        "¡Rocket League en su máxima expresión! Prepara tus reflejos y disfruta de este emocionante clip lleno de jugadas impresionantes.",
        "¿Listo para emociones fuertes? Este clip de Rocket League te dejará sin aliento. ¡Prepárate para la acción más intensa y los goles más emocionantes!",
        "¡No te pierdas estas jugadas espectaculares en Rocket League! Acción, habilidad y mucha emoción te esperan en este clip.",
        "Rocket League nunca decepciona, y este clip es la prueba. ¡Disfruta de las jugadas más emocionantes y los goles más espectaculares!",
        "¡Siente la emoción de Rocket League en cada segundo de este clip! Acción, habilidad y goles te esperan en este emocionante partido.",
        "¿Quieres experimentar la emoción de Rocket League? ¡Este clip te llevará directo al corazón de la acción! No te lo pierdas."
    ]
    return random.choice(options)

# Función para subir el video a YouTube en un horario específico
def upload_video(video_path, scheduled_time):
    print(f"Programando la subida de video para: {scheduled_time}")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": f"{generate_dynamic_description()}",
                "title": f"{generate_dynamic_title()}",  # Utiliza el contador de clips subidos en el título
                "tags": ["Rocket League", "Gaming", "rocket league","rocket league montage","rocket league best goals","rocket league freestyle","rocket league fx","rocket league best","rocket league best of","rocket league insanity","rocket league pro","rocket league impossible","rocket league epic","rocket league moments"],  # Agrega etiquetas relevantes si lo deseas
                "defaultLanguage": "en",  # Cambia según tu idioma
                "madeForKids": False,
                "defaultAudioLanguage": "en",  # Cambia según tu idioma
                "privacyStatus": "private",  # Programar como privado
                "embeddable": True,  # Permitir la inserción del video
                "license": "youtube",
                "recordingDate": datetime.datetime.now().isoformat() + "Z",  # Agregar la fecha de grabación
                "width": 1080,  # Anchura del video (en píxeles)
                "height": 1920,  # Altura del video (en píxeles) para formato vertical (9:16)
            },
            "status": {
                "privacyStatus": "private",  # Programar como privado
                "publishAt": scheduled_time.isoformat() + "Z"  # Programar la fecha y hora de publicación
            }
        },
        media_body=video_path  # Usar el archivo redimensionado
    )
    response = request.execute()
    print("Video programado para su subida:", response["id"])

# Función para programar la subida de los videos en diferentes horarios
def schedule_video_uploads():
    print("Programando la subida de videos a YouTube...")
    scheduled_times = [
        datetime.datetime.now().replace(hour=8, minute=0),
        datetime.datetime.now().replace(hour=12, minute=0),
        datetime.datetime.now().replace(hour=14, minute=0),
        datetime.datetime.now().replace(hour=18, minute=0)
    ]
    for i, file in enumerate(os.listdir(RESIZED_VIDEOS_DIR)):
        if i >= 4:
            break  # Salir del bucle si ya hemos programado 4 videos
        if file.endswith(".mp4"):
            video_path = os.path.join(RESIZED_VIDEOS_DIR, file)
            print(f"Subiendo video: {video_path}")
            # Programar la subida del video en uno de los horarios predefinidos
            upload_video(video_path, scheduled_times[i])
            move_uploaded_video(video_path, UPLOADED_VIDEOS_DIR)
    print("Subida de videos programada.")

# Función para mover un video subido a la carpeta correspondiente
def move_uploaded_video(video_path, destination_dir):
    try:
        if os.path.exists(video_path):
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            move(video_path, os.path.join(destination_dir, os.path.basename(video_path)))
            print(f"Video movido a la carpeta de videos subidos: {os.path.join(destination_dir, os.path.basename(video_path))}")
            return True
        else:
            print("El video no existe en la ubicación especificada.")
            return False
    except Exception as e:
        print(f"Error al mover el video: {str(e)}")
        return False

# Función para cargar los datos desde el archivo JSON
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            print("Cargando datos...")
            return json.load(file)
    else:
        print("Archivo de datos no encontrado. Creando uno nuevo...")
        return {"last_upload_time": None}

# Función para guardar los datos en el archivo JSON
def guardar_datos(datos):
    with open(DATA_FILE, "w") as file:
        json.dump(datos, file)

# Función principal para manejar las opciones del usuario
def main():
    print("1. Redimensionar videos disponibles")
    print("2. Subir videos a YouTube (de los videos pendientes)")
    print("3. Realentizar musica existente")
    opcion = input("Selecciona una opción (1/3): ")

    if opcion == "1":
        handler = MyHandler()
        handler.redimensionar_videos_existente()
    elif opcion == "2":
        schedule_video_uploads()
    elif opcion == "3":
        handler = MyHandler()
        handler.realentizar_y_agregar_reverb()
    else:
        print("Opción no válida. Por favor, selecciona 1 o 2.")

if __name__ == "__main__":
    main()
