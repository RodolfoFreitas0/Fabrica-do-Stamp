import pygame
import random
import sys

from scripts.UI import UIManager
from scripts.loader import load_img, load_img_2x
from scripts.dialogue_story import DialogueSystem, StoryManager
from scripts.cutscene import CutsceneManager

from scripts.settings import *

class Screen:
    def __init__(self, game):
        self.game = game
        self.uimanager = UIManager()
    
    def update(self, events):
        self.uimanager.update(events)

    def render(self, surf):
        self.uimanager.render(surf)

class StartScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.title = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH - 255,
            200,
            "Fabrica do\nStamp",
            FONT,
            (0, 0, 0),
            "center"
        )

        self.play_button = self.uimanager.new_ui_textbutton(
             WINDOW_WIDTH - 225,
             300,
             200,
             60,
             "Jogar",
             FONT,
             self.start_game,
        )

        self.quit_button = self.uimanager.new_ui_textbutton(
             WINDOW_WIDTH - 225,
             530,
             200,
             60,
             "Sair",
             FONT,
             self.leave_game,
        )

        self.plaqueta = load_img("MenuPlaqueta.png")

        background = load_img("BackGround.png")
        self.background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def leave_game(self):
        pygame.quit()
        sys.quit()
    
    def start_game(self):
        self.game.change_state("cutscene")
    
    def render(self, surf):
        surf.blit(self.background, (0, 0))

        plaqueta_menor = pygame.transform.scale(self.plaqueta, (348, 567))

        surf.blit(plaqueta_menor, (WINDOW_WIDTH - 400, 90))

        super().render(surf)

class GameOverScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.title = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 140,
            "VOCÊ FALHOU",
            FONT,
            (255, 50, 50),
            "center"
        )

        self.subtitle = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 30,
            "Stamp da Silva Jr. observou sua incompetência...",
            FONT,
            (255, 100, 100),
            "center"
        )

        self.punishment = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            "E decidiu aplicar a PUNIÇÃO DIVINA.",
            FONT,
            (255, 100, 100),
            "center"
        )

        self.punishment = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 60,
            "(Não tive tempo de elaborar essa cena :( ))",
            FONT,
            (255, 255, 255),
            "center"
        )

        self.back_button = self.uimanager.new_ui_textbutton(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 + 120,
            220,
            60,
            "Aceitar Destino",
            FONT,
            self.go_back
        )

    def go_back(self):
        self.game.change_state("start")

    def render(self, surf):
        surf.fill((15, 15, 15))
        super().render(surf)

class VictoryScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.back_button = self.uimanager.new_ui_textbutton(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            200,
            60,
            "Voltar ao Menu",
            FONT,
            self.go_back
        )

        self.victory_label = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 120,
            "VOCÊ VENCEU!",
            FONT,
            (255, 255, 0),
            "center"
        )

        self.victory_label = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2 - 60,
            "(Não tive tempo de elaborar essa cena :( ))",
            FONT,
            (255, 255, 0),
            "center"
        )

    def go_back(self):
        self.game.change_state("start")

    def render(self, surf):
        surf.fill((20, 20, 20))
        super().render(surf)
    
class CutsceneScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.dialogue = DialogueSystem()
        self.cutscene = CutsceneManager(game, self)

    def update(self, events):
        self.cutscene.update(events)
        self.dialogue.update(events)

    def render(self, surf):
        self.cutscene.render(surf)
        self.dialogue.render(surf)

class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        background = load_img("Background-jogo.png")
        self.background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        chao = load_img("Chao.png")
        self.chao = pygame.transform.scale(chao, (WINDOW_WIDTH, WINDOW_HEIGHT))

        base_esteira = load_img("BaseEsteira.png")
        self.base_esteira = pygame.transform.scale(base_esteira, (WINDOW_WIDTH, WINDOW_HEIGHT))

        lixeira_frente = load_img("lixeira/LixeiraFrente.png")
        lixeira_atraz = load_img("lixeira/LixeiraAtraz.png")

        self.lixeira_frente = pygame.transform.scale(lixeira_frente, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lixeira_atraz = pygame.transform.scale(lixeira_atraz, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.stampdasilva = load_img_2x("StampDaSilvaJr.png")

        self.base_material_sprites = {
            "Base": load_img_2x("carimbo/materiais/BaseBase.png"),
            "Bétula": load_img_2x("carimbo/materiais/BaseBetula.png"),
            "Carvalho": load_img_2x("carimbo/materiais/BaseCarvalho.png"),
            "Pinheiro": load_img_2x("carimbo/materiais/BasePinheiro.png")
        }

        self.topo_sprites = {
            "Quadrado": {
                "Base": load_img_2x("carimbo/formatos/TopoBase.png"),
                "Bétula": load_img_2x("carimbo/formatos/TopoQuadradoBetula.png"),
                "Carvalho": load_img_2x("carimbo/formatos/TopoQuadradoCarvalho.png"),
                "Pinheiro": load_img_2x("carimbo/formatos/TopoQuadradoPinheiro.png")
            },
            "Redondo": {
                "Base": load_img_2x("carimbo/formatos/TopoCircular.png"),
                "Bétula": load_img_2x("carimbo/formatos/TopoCircularBetula.png"),
                "Carvalho": load_img_2x("carimbo/formatos/TopoCircularCarvalho.png"),
                "Pinheiro": load_img_2x("carimbo/formatos/TopoCircularPinheiro.png")
            },
            "Triangulo": {
                "Base": load_img_2x("carimbo/formatos/TopoTriangular.png"),
                "Bétula": load_img_2x("carimbo/formatos/TopoTriangularBetula.png"),
                "Carvalho": load_img_2x("carimbo/formatos/TopoTriangularCarvalho.png"),
                "Pinheiro": load_img_2x("carimbo/formatos/TopoTriangularPinheiro.png")
            }
        }

        self.carimbo_sprites = {
            "Felps": load_img_2x("carimbo/carimbos/FELPS.png"),
            "V": load_img_2x("carimbo/carimbos/v.png"),
            "X": load_img_2x("carimbo/carimbos/x.png")
        }

        self.cores_sprites = {
            "Rosa": load_img_2x("carimbo/cores/BaseRosa.png"),
            "Verde": load_img_2x("carimbo/cores/BaseVerde.png"),
            "Vermelho": load_img_2x("carimbo/cores/BaseVermelha.png")
        }

        self.decoracoes_sprites = {
            "Certo": load_img_2x("carimbo/decoracoes/certo.png"),
            "Errado": load_img_2x("carimbo/decoracoes/errado.png"),
            "coracao": load_img_2x("carimbo/decoracoes/Coracao.png")
        }

        self.machine_sprites = {
            "Cano": load_img_2x("maquinas/CarimboCanoEntrada.png"),
            "Maquina1": load_img_2x("maquinas/Maquina1.png"),
            "Maquina2": load_img_2x("maquinas/Maquina2.png"),
            "Maquina3": load_img_2x("maquinas/Maquina3.png"),
            "Maquina4": load_img_2x("maquinas/Maquina4.png")
        }

        self.extensaoCano = load_img_2x("maquinas/CanoExtensao.png")
        self.tv = load_img_2x("Tv.png")

        self.machine_pos = {
            1: ("Cano", pygame.Vector2(151, -10)),
            2: ("Maquina1", pygame.Vector2(336, 0)),
            3: ("Maquina2", pygame.Vector2(529, -10)),
            4: ("Maquina3", pygame.Vector2(658, -10)),
            5: ("Maquina4", pygame.Vector2(787, -10))
        }

        self.machine_offset = {
            belt: 0 for belt in self.machine_pos
        }

        self.belt_positions = {
            1: pygame.Vector2(161, 335),
            2: pygame.Vector2(321, 335),
            3: pygame.Vector2(479, 335),
            4: pygame.Vector2(638, 335),
            5: pygame.Vector2(797, 335),
            6: pygame.Vector2(915, 335)
        }

        self.carimbo_state = "normal"
        self.discard_stage = 0
        self.discard_pos = {
            1: pygame.Vector2(1125, 335),
            2: pygame.Vector2(1125, 900)
        }

        self.dialogue = DialogueSystem()
        self.story = StoryManager(self)
        self.story.reset()
        self.story.trigger(None)

        self.score = 0

        self.game_duration = 240
        self.timer_started = False
        self.start_time = 0
        self.time_left = self.game_duration

        self.timer_label = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2 + WINDOW_WIDTH // 4,
            20,
            "4:00",
            FONT,
            (255, 255, 255),
            "center"
        )

        self.current_belt = 1

        self.carimbo_pos = pygame.Vector2(self.belt_positions[self.current_belt])
        self.target_pos = pygame.Vector2(self.carimbo_pos)

        self.carimbos = ["Felps", "X", "V"]
        self.formatos = ["Quadrado", "Redondo", "Triangulo"]        
        self.materiais = ["Carvalho", "Bétula", "Pinheiro"]
        self.cores = ["Rosa", "Vermelho", "Verde"]
        self.decoracoes = ["Coração", "Errado", "Certo"]

        self.order = {}
        self.carimbo = {
            "carimbo": None,
            "formato": None,
            "material": "Base",
            "cor": None,
            "decoracao": None
        }

        self.generate_order()
        
        self.belt_changer_left = self.uimanager.new_ui_textbutton(
            35,
            WINDOW_HEIGHT // 2 + 70,
            45,
            45,
            "<",
            FONT,
            self.change_belt_l
        )

        self.belt_changer_right = self.uimanager.new_ui_textbutton(
            35,
            WINDOW_HEIGHT // 2 + 200,
            45,
            45,
            ">",
            FONT,
            self.change_belt_r
        )

        self.order_label = self.uimanager.new_hud_textlabel(
            WINDOW_WIDTH // 2,
            50,
            "",
            FONT,
            (255,255,255),
            "center"
        )

        self.confirm_button = self.uimanager.new_ui_textbutton(
            963,
            520,
            135,
            60,
            f"Confirmar\n carimbo",
            FONT,
            self.confirm_order
        )

        y = 470
        for carimbis in self.carimbos:
            self.uimanager.new_ui_textbutton(
                171, 
                y,
                125,
                40,
                carimbis,
                FONT,
                lambda c=carimbis: self.select_carimbo(c)
            )
            y += 50

        y = 470
        for formato in self.formatos:
            self.uimanager.new_ui_textbutton(
                331,
                y,
                125,
                40,
                formato,
                FONT,
                lambda f=formato: self.select_formato(f)
            )
            y += 50

        y = 470
        for material in self.materiais:
            self.uimanager.new_ui_textbutton(
                489,
                y,
                125,
                40,
                material,
                FONT,
                lambda m=material: self.select_material(m)
            )
            y += 50
        
        y = 470
        for cor in self.cores:
            self.uimanager.new_ui_textbutton(
                648,
                y,
                125,
                40,
                cor,
                FONT,
                lambda c=cor: self.select_cor(c)
            )
            y += 50

        y = 470
        for decoracao in self.decoracoes:
            self.uimanager.new_ui_textbutton(
                807,
                y,
                125,
                40,
                decoracao,
                FONT,
                lambda d=decoracao: self.select_decoracao(d)
            )
            y += 50
    
    def generate_order(self):
        self.order = {
            "carimbo": random.choice(self.carimbos),
            "formato": random.choice(self.formatos),
            "material": random.choice(self.materiais),
            "cor": random.choice(self.cores),
            "decoracao": random.choice(self.decoracoes)
        }

    def select_carimbo(self, carimbo):
        if self.current_belt == 1:
            self.carimbo["carimbo"] = carimbo
            self.carimbo["formato"] = None
            self.machine_offset[1] = 10
        else:
            self.machine_offset[1] = 5
    
    def select_formato(self, formato):
        if self.current_belt == 2: 
            self.carimbo["formato"] = formato
            self.machine_offset[2] = 80
        else:
            self.machine_offset[2] = 5

    def select_material(self, material):
        if self.current_belt == 3 and self.carimbo["formato"] != None:
            self.carimbo["material"] = material
            self.machine_offset[3] = 10
        else:
            self.machine_offset[3] = 5

    def select_cor(self, cor):
        if self.current_belt == 4:
            self.carimbo["cor"] = cor
            self.machine_offset[4] = 10
        else:
            self.machine_offset[4] = 5

    def select_decoracao(self, decoracao):
        if self.current_belt == 5:
            self.carimbo["decoracao"] = decoracao
            self.machine_offset[5] = 10
        else:
            self.machine_offset[5] = 5

    def change_belt_l(self):
        if not self.carimbo["carimbo"]:
            return
        
        if self.current_belt > 1:
            self.current_belt -= 1
        else:
            self.current_belt = 1

        self.update_carimbo_target()
        
    def change_belt_r(self):
        if not self.carimbo["carimbo"]:
            return
        
        if self.current_belt < 6:
            self.current_belt += 1
        else:
            self.current_belt = 6

        self.update_carimbo_target()


    def confirm_order(self):
        if self.current_belt != 6:
            return
        
        if self.carimbo == self.order:
            self.score += 1

            if self.score >= 10:
                self.time_left = 1000000
                self.game.change_state("victory")
                return

            self.reset_carimbo()
            self.generate_order()
        else:
            self.score -= 1
            self.start_discard_anim()

    def start_discard_anim(self):
        self.carimbo_state = "discard"
        self.discard_stage = 1

    def render_order(self, surf):
        x, y = 1100, 132

        carimbo = self.order["carimbo"]
        formato = self.order["formato"]
        material = self.order["material"]
        cor = self.order["cor"]
        decoracao = self.order["decoracao"]

        surf.blit(self.tv, (x - 12, y - 132))

        if decoracao == "Coração":
            decoracao = "coracao"

        if cor:
            cor_sprite = self.cores_sprites[cor]
            surf.blit(cor_sprite, (x, y))
        
        base_sprite = self.base_material_sprites[material]
        surf.blit(base_sprite, (x, y))

        if decoracao:
            decoracao_sprite = self.decoracoes_sprites[decoracao]
            surf.blit(decoracao_sprite, (x + 12, y + 1))

        carimbo_sprite = self.carimbo_sprites[carimbo]
        surf.blit(carimbo_sprite, (x + 15, y + 36))

        topo_sprite = self.topo_sprites[formato][material]
        surf.blit(topo_sprite, (x + 35, y - 80))

    def render_machines(self, surf):

        surf.blit(self.extensaoCano, (364, 0))

        for belt,(machine, pos) in self.machine_pos.items():
            sprite = self.machine_sprites[machine]
            offset = self.machine_offset[belt]

            surf.blit(sprite, (pos.x, pos.y + offset))

    def render_carimbo(self, surf):
        x, y = self.carimbo_pos

        carimbo = self.carimbo["carimbo"]
        formato = self.carimbo["formato"]
        material = self.carimbo["material"]
        cor = self.carimbo["cor"]
        decoracao = self.carimbo["decoracao"]

        if decoracao == "Coração":
            decoracao = "coracao"

        if not carimbo:
            return
        
        if cor:
            cor_sprite = self.cores_sprites[cor]
            surf.blit(cor_sprite, (x, y))

        base_sprite = self.base_material_sprites[material]
        surf.blit(base_sprite, (x, y))

        if decoracao:
            decoracao_sprite = self.decoracoes_sprites[decoracao]
            surf.blit(decoracao_sprite, (x + 12, y + 1))

        carimbo_sprite = self.carimbo_sprites[carimbo]
        surf.blit(carimbo_sprite, (x + 15, y + 36))

        if formato:
            topo_sprite = self.topo_sprites[formato][material]
            surf.blit(topo_sprite, (x + 35, y - 80))
        
    def update_carimbo_target(self):
        self.target_pos = pygame.Vector2(
            self.belt_positions[self.current_belt]
        )

    def reset_carimbo(self):
        self.carimbo = {
            "carimbo": None,
            "formato": None,
            "material": "Base",
            "cor": None,
            "decoracao": None
        }

        self.current_belt = 1
        self.update_carimbo_target()

    def update(self, events):

        if not self.dialogue.active and not self.timer_started:
            self.timer_started = True
            self.start_time = pygame.time.get_ticks()
        
        if self.timer_started:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
            self.time_left = max(0, self.game_duration - elapsed)

            minutes = int(self.time_left) // 60
            seconds = int(self.time_left) % 60

            self.timer_label.set_text(f"{minutes:02}:{seconds:02}")

        if self.time_left <= 0:
            pass

        if self.carimbo_state == "discard":
            target = self.discard_pos[self.discard_stage]
            self.carimbo_pos = self.carimbo_pos.lerp(target, 0.12)

            if self.carimbo_pos.distance_to(target) < 5:
                self.discard_stage += 1

                if self.discard_stage > 2:
                    self.carimbo_state = "normal"
                    self.reset_carimbo()
                    self.generate_order()
            
            return

        self.carimbo_pos = self.carimbo_pos.lerp(self.target_pos, 0.10)

        for belt in self.machine_offset:
            self.machine_offset[belt] = pygame.math.lerp(
                self.machine_offset[belt],
                0,
                0.09
            )

        if self.dialogue.active:
            self.dialogue.update(events)
        else:
            super().update(events)

    def render(self, surf):
        surf.fill((30, 30, 30))

        surf.blit(self.background, (0, 0))

        surf.blit(self.lixeira_atraz, (0, 0))

        self.render_carimbo(surf)
        
        surf.blit(self.chao, (0, 0))

        surf.blit(self.lixeira_frente, (0, 0))

        surf.blit(self.base_esteira, (0, 0))

        super().render(surf)

        self.render_machines(surf)

        self.render_order(surf)

        if self.dialogue.active:
            surf.blit(self.stampdasilva, (50, WINDOW_HEIGHT // 2))
            self.dialogue.render(surf)