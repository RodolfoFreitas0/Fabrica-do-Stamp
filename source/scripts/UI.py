import pygame

from scripts.settings import *
class UIElement():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x - (width // 2), y - (height // 2), width, height)
        self.visible = True
        self.enabled = True
class UIButton(UIElement):
    def __init__(self, x, y, width, height, on_click=None):
        super().__init__(x, y, width, height)

        self.on_click = on_click
        self.hover = False
        self.clicked = False

        self.base_color = (180, 180, 180)
        self.hover_color = (255, 255, 255)
    
    def light_color(self, color, amount):
        return tuple(min(c + amount, 255) for c in color)
    
    def update(self, events):
        if not self.enabled:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hover:
                    self.clicked = True
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.hover and self.clicked:
                    if self.on_click:
                        self.on_click()
                self.clicked = False
    
    def render(self, surf):
        if not self.visible:
            return
        
        color = self.hover_color if self.hover else self.base_color
        border_color = self.light_color(color, -80)

        pygame.draw.rect(surf, border_color, self.rect.inflate(4, 4))
        pygame.draw.rect(surf, color, self.rect)
class UITextButton(UIButton):
    def __init__(self, x, y, width, height, text, font=FONT, on_click=None):
        super().__init__(x, y, width, height, on_click)

        self.text = text
        self.font = font
        self.text_color = (0, 0, 0)
    
    def render(self, surf):
        super().render(surf)

        if not self.visible:
            return
        
        text_surf = self.font.render(self.text, True, self.text_color)
        surf.blit(text_surf, text_surf.get_rect(center=self.rect.center))
    
class HUDButton(UIElement):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.base_color = (180, 180, 180)
    
    def light_color(self, color, amount):
        return tuple(min(c + amount, 255) for c in color)
    
    def render(self, surf):
        if not self.visible:
            return
        
        border_color = self.light_color(self.base_color, -80)

        pygame.draw.rect(surf, border_color, self.rect.inflate(4, 4))
        pygame.draw.rect(surf, self.base_color, self.rect)

class HUDLabel(UIElement):
    def __init__(self, x, y, text, font=FONT, color=(255, 255, 255), align="center"):
        super().__init__(x, y, 0, 0)

        self.text = text
        self.font = font
        self.text_color = color
        self.align = align

    def update(self, events):
        pass

    def set_text(self, text):
        self.text = text

    def render(self, surf):
        if not self.visible:
            return
        
        text_surf = self.font.render(self.text, True, self.text_color)

        if self.align == "center":
            text_rect = text_surf.get_rect(center=self.rect.center)

        elif self.align == "left":
            text_rect = text_surf.get_rect(topleft=(self.rect.left + 10, self.rect.top + 10))

        elif self.align == "right":
            text_rect = text_surf.get_rect(topright=(self.rect.right - 10, self.rect.top + 10))

        surf.blit(text_surf, text_rect)
    
class HUDTextButton(HUDButton):
    def __init__(self, x, y, width, height, text, font=FONT, color=(255,255,255), base_color=(180, 180, 180), align="center"):
        super().__init__(x, y, width, height)

        self.text = text
        self.font = font
        self.text_color = color
        self.base_color = base_color
        self.align = align

    def update(self):
        pass

    def set_text(self, text):
        self.text = text
    
    def render(self, surf):
        super().render(surf)
    
        text_surf = self.font.render(self.text, True, self.text_color)

        if self.align == "center":
            text_rect = text_surf.get_rect(center=self.rect.center)

        elif self.align == "left":
            text_rect = text_surf.get_rect(topleft=(self.rect.left + 10, self.rect.top + 10))

        elif self.align == "right":
            text_rect = text_surf.get_rect(topright=(self.rect.right - 10, self.rect.top + 10))

        surf.blit(text_surf, text_rect)

class HUDBar(UIElement):
    def __init__(self, x, y, width, height, max_value):
        super().__init__(x, y, width, height)

        self.max_value = max_value
        self.current_value = max_value

        self.bg_color = (100, 0, 0)
        self.fill_color = (255, 0, 0)

    def update(self, value):
        self.current_value = max(0, min(value, self.max_value))

    def render(self, surf):
        if not self.visible:
            return

        pygame.draw.rect(surf, self.bg_color, self.rect)

        fill_width = (self.current_value / self.max_value) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)

        pygame.draw.rect(surf, self.fill_color, fill_rect)

class UIManager():
    def __init__(self):
        self.elements = []
    
    def new_hud_button(self, x, y, width, height):
        button = HUDButton(x, y, width, height)
        self.elements.append(button)
        return button
    
    def new_hud_textbutton(self, x, y, width, height, text, font, color, base_color, align):
        button = HUDTextButton(x, y, width, height, text, font, color, base_color, align)
        self.elements.append(button)
        return button
    
    def new_ui_textbutton(self, x, y, width, height, text, font, on_click=None):
        button = UITextButton(x, y, width, height, text, font, on_click)
        self.elements.append(button)
        return button
    
    def new_hud_textlabel(self, x, y, text, font, color, align):
        button = HUDLabel(x, y, text, font, color, align)
        self.elements.append(button)
        return button
    
    def new_hud_bar(self, x, y, width, height, max_value):
        button = HUDBar(x, y, width, height, max_value)
        self.elements.append(button)
        return button

    def mouse_over_ui(self):
        mouse_pos = pygame.mouse.get_pos()
        for element in self.elements:
            if element.rect.collidepoint(mouse_pos):
                return True
        return False

    def update(self, events):
        for element in reversed(self.elements):
            element.update(events)
    
    def clear(self):
        self.elements.clear()
    
    def render(self, surf):
        for element in self.elements:
            element.render(surf)

def get_scaled_mouse_pos(base_width, base_height, window_width, window_height):
    mx, my = pygame.mouse.get_pos()

    scale_x = window_width / base_width
    scale_y = window_height / base_height

    return mx / scale_x, my / scale_y