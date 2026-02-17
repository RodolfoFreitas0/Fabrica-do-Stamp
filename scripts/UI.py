import pygame

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
    
    def update(self, events):
        if not self.enabled or not self.visible:
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
        pygame.draw.rect(surf, color, self.rect)
class UITextButton(UIButton):
    def __init__(self, x, y, width, height, text, font, on_click=None):
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

class UILabel(UIElement):
    def __init__(self, x, y, text, font, color=(255, 255, 255)):
        super().__init__(x, y, 0, 0)

        self.text = text
        self.font = font
        self.text_color = color

    def update(self, text):
        self.text = text

    def render(self, surf):
        if not self.visible:
            return
        
        text_surf = self.font.render(self.text, True, self.text_color)
        surf.blit(text_surf, text_surf.get_rect(center=self.rect.center))

class UIBar(UIElement):
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
    
    def new_ui_textbutton(self, x, y, width, height, text, font, on_click=None):
        button = UITextButton(x, y, width, height, text, font, on_click)
        self.elements.append(button)
        return button
    
    def new_hud_textlabel(self, x, y, text, font):
        button = UILabel(x, y, text, font)
        self.elements.append(button)
        return button
    
    def new_hud_bar(self, x, y, width, height, max_value):
        button = UIBar(x, y, width, height, max_value)
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