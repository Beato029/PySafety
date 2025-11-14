import pygame
import sys
import random
import math
from datetime import datetime

# Inizializzazione Pygame
pygame.init()

# Dimensioni finestra (identiche al sito)
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Live Threat Map - Radware")

# Colori ESATTI dal sito Radware
BACKGROUND = (13, 22, 33)  # #0D1621
PANEL_BG = (23, 34, 49)    # #172231
PANEL_BORDER = (42, 62, 87) # #2A3E57
TEXT_COLOR = (178, 186, 202) # #B2BACA
TEXT_HIGHLIGHT = (255, 255, 255)
OCEAN_COLOR = (18, 28, 42)  # #121C2A
LAND_COLOR = (30, 45, 60)   # #1E2D3C
COASTLINE_COLOR = (50, 70, 90) # #32465A

# Colori attacchi ESATTI dal sito Radware
ATTACK_COLORS = [
    (239, 71, 58),    # Rosso - Web App Attacks #EF473A
    (252, 123, 35),   # Arancione - Network & DDoS #FC7B23
    (255, 193, 42),   # Giallo - IPS Attacks #FFC12A
    (66, 184, 221),   # Azzurro - Malware #42B8DD
    (163, 78, 188)    # Viola - Bot Attacks #A34EBC
]

# Font (simili al sito)
font_small = pygame.font.SysFont('Segoe UI', 11)
font_medium = pygame.font.SysFont('Segoe UI', 13, bold=True)
font_large = pygame.font.SysFont('Segoe UI', 16, bold=True)
font_title = pygame.font.SysFont('Segoe UI', 20, bold=True)

# Coordinate delle città basate sulla mappa Radware
cities = [
    # Nord America
    {"name": "Seattle", "pos": (220, 180), "country": "USA"},
    {"name": "San Francisco", "pos": (210, 210), "country": "USA"},
    {"name": "Los Angeles", "pos": (210, 230), "country": "USA"},
    {"name": "Denver", "pos": (250, 200), "country": "USA"},
    {"name": "Chicago", "pos": (280, 190), "country": "USA"},
    {"name": "New York", "pos": (310, 190), "country": "USA"},
    {"name": "Atlanta", "pos": (290, 220), "country": "USA"},
    {"name": "Miami", "pos": (300, 250), "country": "USA"},
    {"name": "Dallas", "pos": (260, 230), "country": "USA"},
    {"name": "Toronto", "pos": (300, 180), "country": "Canada"},
    {"name": "Montreal", "pos": (310, 170), "country": "Canada"},
    {"name": "Vancouver", "pos": (230, 170), "country": "Canada"},
    {"name": "Mexico City", "pos": (250, 260), "country": "Mexico"},
    
    # Sud America
    {"name": "Bogota", "pos": (290, 290), "country": "Colombia"},
    {"name": "Lima", "pos": (280, 320), "country": "Peru"},
    {"name": "Santiago", "pos": (290, 370), "country": "Chile"},
    {"name": "Buenos Aires", "pos": (310, 400), "country": "Argentina"},
    {"name": "Sao Paulo", "pos": (330, 350), "country": "Brazil"},
    {"name": "Rio de Janeiro", "pos": (340, 340), "country": "Brazil"},
    
    # Europa
    {"name": "London", "pos": (460, 170), "country": "UK"},
    {"name": "Paris", "pos": (470, 180), "country": "France"},
    {"name": "Amsterdam", "pos": (470, 170), "country": "Netherlands"},
    {"name": "Frankfurt", "pos": (480, 170), "country": "Germany"},
    {"name": "Berlin", "pos": (490, 170), "country": "Germany"},
    {"name": "Madrid", "pos": (450, 200), "country": "Spain"},
    {"name": "Rome", "pos": (490, 190), "country": "Italy"},
    {"name": "Moscow", "pos": (530, 160), "country": "Russia"},
    {"name": "Stockholm", "pos": (490, 150), "country": "Sweden"},
    {"name": "Oslo", "pos": (480, 150), "country": "Norway"},
    {"name": "Warsaw", "pos": (500, 170), "country": "Poland"},
    {"name": "Prague", "pos": (480, 170), "country": "Czech Republic"},
    
    # Africa
    {"name": "Casablanca", "pos": (450, 220), "country": "Morocco"},
    {"name": "Algiers", "pos": (470, 210), "country": "Algeria"},
    {"name": "Cairo", "pos": (520, 220), "country": "Egypt"},
    {"name": "Lagos", "pos": (480, 260), "country": "Nigeria"},
    {"name": "Nairobi", "pos": (540, 280), "country": "Kenya"},
    {"name": "Johannesburg", "pos": (510, 350), "country": "South Africa"},
    
    # Asia
    {"name": "Dubai", "pos": (560, 230), "country": "UAE"},
    {"name": "Istanbul", "pos": (520, 190), "country": "Turkey"},
    {"name": "Mumbai", "pos": (600, 250), "country": "India"},
    {"name": "Delhi", "pos": (610, 230), "country": "India"},
    {"name": "Bangalore", "pos": (610, 260), "country": "India"},
    {"name": "Singapore", "pos": (680, 290), "country": "Singapore"},
    {"name": "Bangkok", "pos": (670, 260), "country": "Thailand"},
    {"name": "Hong Kong", "pos": (720, 240), "country": "China"},
    {"name": "Shanghai", "pos": (740, 230), "country": "China"},
    {"name": "Beijing", "pos": (730, 210), "country": "China"},
    {"name": "Seoul", "pos": (770, 210), "country": "South Korea"},
    {"name": "Tokyo", "pos": (790, 220), "country": "Japan"},
    {"name": "Osaka", "pos": (780, 230), "country": "Japan"},
    {"name": "Taipei", "pos": (740, 250), "country": "Taiwan"},
    {"name": "Manila", "pos": (730, 270), "country": "Philippines"},
    {"name": "Jakarta", "pos": (690, 300), "country": "Indonesia"},
    {"name": "Kuala Lumpur", "pos": (670, 280), "country": "Malaysia"},
    
    # Oceania
    {"name": "Perth", "pos": (710, 370), "country": "Australia"},
    {"name": "Sydney", "pos": (810, 370), "country": "Australia"},
    {"name": "Melbourne", "pos": (800, 380), "country": "Australia"},
    {"name": "Auckland", "pos": (850, 400), "country": "New Zealand"}
]

# Tipi di attacco (esatti dal sito)
attack_types = [
    "Web App Attacks",
    "Network & DDoS", 
    "IPS Attacks",
    "Malware",
    "Bot Attacks"
]

# Lista per tenere traccia degli attacchi attivi
active_attacks = []

# Statistiche
total_attacks = 0
start_time = datetime.now()

# Pre-calcolo delle superfici per le linee (ottimizzazione)
line_cache = {}

# Funzione per disegnare una mappa geografica realistica
def draw_world_map():
    # Sfondo oceano
    screen.fill(OCEAN_COLOR)
    
    # Disegna i continenti con forme realistiche
    draw_continents()
    
    # Disegna i punti delle città (come nel sito Radware)
    for city in cities:
        # Punto luminoso centrale
        pygame.draw.circle(screen, (100, 180, 255), city["pos"], 2)
        # Alone blu
        pygame.draw.circle(screen, (66, 133, 244), city["pos"], 6, 1)
        
        # Etichette solo per città principali (come nel sito)
        major_cities = ["New York", "London", "Tokyo", "Singapore", "Sydney", "San Francisco", "Frankfurt"]
        if city["name"] in major_cities:
            text = font_small.render(city["name"], True, TEXT_COLOR)
            text_rect = text.get_rect(midleft=(city["pos"][0] + 8, city["pos"][1]))
            screen.blit(text, text_rect)

def draw_continents():
    # Nord America - forma realistica
    north_america = [
        (180, 120), (220, 100), (280, 90), (340, 100), (380, 130),
        (400, 170), (390, 220), (360, 260), (320, 280), (280, 290),
        (240, 280), (200, 260), (170, 230), (150, 190), (160, 150)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, north_america)
    pygame.draw.polygon(screen, COASTLINE_COLOR, north_america, 2)
    
    # Sud America
    south_america = [
        (300, 280), (320, 270), (350, 280), (370, 300), (380, 330),
        (380, 380), (360, 410), (330, 430), (300, 420), (280, 400),
        (270, 370), (280, 320)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, south_america)
    pygame.draw.polygon(screen, COASTLINE_COLOR, south_america, 2)
    
    # Europa
    europe = [
        (440, 150), (470, 140), (500, 145), (520, 160), (510, 180),
        (490, 190), (460, 185), (440, 170)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, europe)
    pygame.draw.polygon(screen, COASTLINE_COLOR, europe, 2)
    
    # Africa
    africa = [
        (440, 180), (470, 170), (510, 175), (540, 190), (550, 220),
        (550, 270), (530, 300), (500, 320), (460, 310), (430, 290),
        (420, 250), (420, 210)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, africa)
    pygame.draw.polygon(screen, COASTLINE_COLOR, africa, 2)
    
    # Asia
    asia = [
        (500, 120), (560, 110), (630, 120), (690, 140), (730, 170),
        (750, 210), (750, 250), (730, 290), (690, 310), (640, 300),
        (590, 280), (550, 250), (520, 220), (500, 180), (490, 150)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, asia)
    pygame.draw.polygon(screen, COASTLINE_COLOR, asia, 2)
    
    # Australia
    australia = [
        (750, 350), (780, 340), (810, 350), (820, 370), (810, 400),
        (780, 420), (750, 410), (740, 380)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, australia)
    pygame.draw.polygon(screen, COASTLINE_COLOR, australia, 2)
    
    # Groenlandia
    greenland = [
        (420, 80), (460, 70), (490, 80), (500, 100), (480, 120), (440, 110)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, greenland)
    pygame.draw.polygon(screen, COASTLINE_COLOR, greenland, 2)
    
    # Giappone
    japan = [
        (780, 200), (790, 190), (800, 195), (805, 210), (795, 220), (785, 215)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, japan)
    pygame.draw.polygon(screen, COASTLINE_COLOR, japan, 2)
    
    # Isole britanniche
    uk = [
        (440, 155), (450, 150), (460, 155), (455, 165), (445, 165)
    ]
    pygame.draw.polygon(screen, LAND_COLOR, uk)
    pygame.draw.polygon(screen, COASTLINE_COLOR, uk, 2)

# Funzione per generare un nuovo attacco (come nel sito)
def generate_attack():
    global total_attacks
    
    if random.random() < 0.15:  # Aumentata probabilità al 15%
        source = random.choice(cities)
        target = random.choice([c for c in cities if c != source and random.random() < 0.4])
        
        if target:
            attack_type = random.choices(attack_types, weights=[0.25, 0.25, 0.2, 0.15, 0.15])[0]
            color = ATTACK_COLORS[attack_types.index(attack_type)]
            
            # Punto di controllo per curva
            mid_x = (source["pos"][0] + target["pos"][0]) // 2
            mid_y = (source["pos"][1] + target["pos"][1]) // 2
            
            # Aggiungi curvatura casuale
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(30, 80)
            control_x = mid_x + math.cos(angle) * distance
            control_y = mid_y + math.sin(angle) * distance
            
            active_attacks.append({
                "source": source,
                "target": target,
                "type": attack_type,
                "color": color,
                "progress": 0,
                "start_time": pygame.time.get_ticks(),
                "control_point": (control_x, control_y),
                "particles": [],
                "id": total_attacks,
                "speed": random.uniform(0.015, 0.025)  # Velocità variabile
            })
            total_attacks += 1

# Funzione Bezier quadratica (per curve fluide come nel sito)
def quadratic_bezier(p0, p1, p2, t):
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return (int(x), int(y))

# Funzione ottimizzata per disegnare linee con alpha
def draw_alpha_line(surface, color, start_pos, end_pos, width):
    key = (color, start_pos, end_pos, width)
    if key not in line_cache:
        # Crea una superficie per la linea
        line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(line_surface, color, start_pos, end_pos, width)
        line_cache[key] = line_surface
    surface.blit(line_cache[key], (0, 0))

# Aggiorna e disegna attacchi (OTTIMIZZATO per velocità)
def update_attacks():
    current_time = pygame.time.get_ticks()
    
    for attack in active_attacks[:]:
        # Aumenta la velocità di progressione
        attack["progress"] += attack["speed"]
        
        if attack["progress"] >= 1:
            active_attacks.remove(attack)
        else:
            # Posizione corrente sulla curva
            current_pos = quadratic_bezier(
                attack["source"]["pos"],
                attack["control_point"], 
                attack["target"]["pos"],
                attack["progress"]
            )
            
            # DISEGNO OTTIMIZZATO: meno segmenti ma più veloci
            # Disegna solo 5 segmenti invece di 10
            segments = 5
            for i in range(segments):
                t1 = max(0, attack["progress"] - (i * 0.05))  # Incremento maggiore
                t2 = max(0, attack["progress"] - ((i+1) * 0.05))
                if t1 > 0 and t2 > 0:
                    p1 = quadratic_bezier(attack["source"]["pos"], attack["control_point"], attack["target"]["pos"], t1)
                    p2 = quadratic_bezier(attack["source"]["pos"], attack["control_point"], attack["target"]["pos"], t2)
                    
                    # Alpha più aggressivo per ridurre il calcolo
                    alpha = 200 - (i * 40)  # Alpha più alto, meno calcoli
                    if alpha > 0:
                        color_with_alpha = (*attack["color"], alpha)
                        # Usa la funzione ottimizzata
                        draw_alpha_line(screen, color_with_alpha, p1, p2, 2)
            
            # Punto principale dell'attacco
            pygame.draw.circle(screen, attack["color"], current_pos, 3)
            
            # EFFETTO PARTICELLARE OTTIMIZZATO: meno particelle
            if random.random() < 0.3:  # Ridotta probabilità
                attack["particles"].append({
                    "pos": current_pos,
                    "velocity": (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),  # Velocità ridotta
                    "life": 0.8,  # Vita più breve
                    "size": random.randint(1, 2)
                })
            
            # Aggiorna particelle (ottimizzato)
            for particle in attack["particles"][:]:
                particle["pos"] = (
                    particle["pos"][0] + particle["velocity"][0],
                    particle["pos"][1] + particle["velocity"][1]
                )
                particle["life"] -= 0.08  # Decadimento più veloce
                
                if particle["life"] <= 0:
                    attack["particles"].remove(particle)
                else:
                    alpha = int(255 * particle["life"])
                    color = (*attack["color"], alpha)
                    # Disegno diretto senza superficie per particelle piccole
                    pygame.draw.circle(screen, color, 
                                     (int(particle["pos"][0]), int(particle["pos"][1])), 
                                     particle["size"])

# Pannello sinistro (identico al sito)
def draw_left_panel():
    # Sfondo pannello
    panel_rect = pygame.Rect(20, 20, 280, HEIGHT - 40)
    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, panel_rect, 2, border_radius=8)
    
    # Titolo
    title = font_title.render("LIVE THREAT MAP", True, TEXT_HIGHLIGHT)
    screen.blit(title, (40, 40))
    
    # Logo Radware (testuale)
    radware_text = font_medium.render("RADWARE", True, (66, 133, 244))
    screen.blit(radware_text, (40, 70))
    
    # Separatore
    pygame.draw.line(screen, PANEL_BORDER, (40, 100), (260, 100), 2)
    
    # Legenda attacchi
    legend_y = 120
    legend_title = font_large.render("ATTACK TYPES", True, TEXT_HIGHLIGHT)
    screen.blit(legend_title, (40, legend_y))
    
    for i, attack_type in enumerate(attack_types):
        # Icona colore
        pygame.draw.rect(screen, ATTACK_COLORS[i], (40, legend_y + 35 + i*30, 12, 12))
        
        # Nome attacco
        name_text = font_medium.render(attack_type, True, TEXT_COLOR)
        screen.blit(name_text, (60, legend_y + 35 + i*30))
        
        # Contatore
        count = sum(1 for a in active_attacks if a["type"] == attack_type)
        count_text = font_medium.render(str(count), True, TEXT_HIGHLIGHT)
        screen.blit(count_text, (250 - count_text.get_width(), legend_y + 35 + i*30))
    
    # Separatore
    sep_y = legend_y + 35 + len(attack_types)*30 + 10
    pygame.draw.line(screen, PANEL_BORDER, (40, sep_y), (260, sep_y), 1)
    
    # Statistiche globali
    stats_y = sep_y + 20
    stats_title = font_large.render("GLOBAL STATISTICS", True, TEXT_HIGHLIGHT)
    screen.blit(stats_title, (40, stats_y))
    
    # Tempo di attività
    elapsed = datetime.now() - start_time
    hours = elapsed.seconds // 3600
    minutes = (elapsed.seconds % 3600) // 60
    uptime_text = font_medium.render(f"Uptime: {hours:02d}:{minutes:02d}", True, TEXT_COLOR)
    screen.blit(uptime_text, (40, stats_y + 30))
    
    # Attacchi totali
    total_text = font_medium.render(f"Total Attacks: {total_attacks}", True, TEXT_COLOR)
    screen.blit(total_text, (40, stats_y + 55))
    
    # Attacchi attivi
    active_text = font_medium.render(f"Active Threats: {len(active_attacks)}", True, TEXT_COLOR)
    screen.blit(active_text, (40, stats_y + 80))
    
    # Top paesi
    countries = {}
    for attack in active_attacks:
        countries[attack["target"]["country"]] = countries.get(attack["target"]["country"], 0) + 1
    
    if countries:
        top_country = max(countries, key=countries.get)
        country_text = font_medium.render(f"Top Target: {top_country}", True, TEXT_COLOR)
        screen.blit(count_text, (40, stats_y + 105))

# Pannello destro (attacchi recenti)
def draw_right_panel():
    panel_rect = pygame.Rect(WIDTH - 320, 20, 300, HEIGHT - 40)
    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, panel_rect, 2, border_radius=8)
    
    # Titolo
    title = font_large.render("RECENT ATTACKS", True, TEXT_HIGHLIGHT)
    screen.blit(title, (WIDTH - 300, 40))
    
    # Lista attacchi recenti (ultimi 8)
    recent_attacks = active_attacks[-8:] if len(active_attacks) > 8 else active_attacks
    
    for i, attack in enumerate(recent_attacks[::-1]):  # Più recenti in alto
        y_pos = 80 + i * 25
        
        # Icona colore
        pygame.draw.rect(screen, attack["color"], (WIDTH - 300, y_pos, 8, 8))
        
        # Descrizione attacco
        attack_text = font_small.render(
            f"{attack['source']['name']} → {attack['target']['name']}", 
            True, TEXT_COLOR
        )
        screen.blit(attack_text, (WIDTH - 285, y_pos))
        
        # Tipo attacco
        type_text = font_small.render(attack["type"], True, attack["color"])
        screen.blit(type_text, (WIDTH - 300 + 250 - type_text.get_width(), y_pos))

# Pannello inferiore (statistiche in tempo reale)
def draw_bottom_panel():
    panel_rect = pygame.Rect(320, HEIGHT - 80, WIDTH - 640, 60)
    pygame.draw.rect(screen, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, panel_rect, 2, border_radius=8)
    
    # Titolo
    title = font_medium.render("REALTIME ACTIVITY", True, TEXT_HIGHLIGHT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT - 70))
    
    # Barra attività (aggiornata per più attacchi)
    activity_level = min(len(active_attacks) / 30.0, 1.0)  # Normalizza a 30 attacchi massimi
    
    # Background barra
    bar_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 50, 200, 15)
    pygame.draw.rect(screen, PANEL_BORDER, bar_rect, border_radius=7)
    
    # Barra di progresso
    progress_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 50, int(200 * activity_level), 15)
    if activity_level > 0.7:
        color = (239, 71, 58)  # Rosso per alto carico
    elif activity_level > 0.4:
        color = (255, 193, 42)  # Giallo per medio carico
    else:
        color = (66, 184, 221)  # Blu per basso carico
    
    pygame.draw.rect(screen, color, progress_rect, border_radius=7)
    
    # Testo attività
    activity_text = font_small.render(f"Activity Level: {int(activity_level * 100)}%", True, TEXT_COLOR)
    screen.blit(activity_text, (WIDTH // 2 - activity_text.get_width() // 2, HEIGHT - 30))

# Loop principale
clock = pygame.time.Clock()
running = True

# Pulisci la cache periodicamente per evitare memory leak
last_cache_clean = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Pulisci la cache ogni 10 secondi
    current_time = pygame.time.get_ticks()
    if current_time - last_cache_clean > 10000:  # 10 secondi
        line_cache.clear()
        last_cache_clean = current_time
    
    # Disegna la mappa
    draw_world_map()
    
    # Genera attacchi
    generate_attack()
    
    # Aggiorna attacchi
    update_attacks()
    
    # Disegna i pannelli
    draw_left_panel()
    draw_right_panel()
    draw_bottom_panel()
    
    # Aggiorna schermo
    pygame.display.flip()
    clock.tick(30)  # Mantieni 30 FPS per fluidità

pygame.quit()
sys.exit()