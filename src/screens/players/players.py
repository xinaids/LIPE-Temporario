import pygame
from src.datatypes.player import Player
from database.students.students import add_student, select_max_id

pygame.init()




class PlayerScreen:
    def __init__(self, largura=1920, altura=1080):
        self.cursor_visible = True
        self.cursor_timer = 0
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        fundo_tela = pygame.image.load("images/lipe2.0.png").convert()
        self.tela.blit(fundo_tela, (0, 0))
        pygame.display.set_caption("Cadastro de Jogadores")
        self.fonte = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(700, 300, 500, 40)
        self.texto_input = ""
        self.ativo = False
        self.nomes_jogadores = []

    def Show(self):
        clock = pygame.time.Clock()
        rodando = True

        while rodando:
            fundo_tela = pygame.image.load("images/lipe2.0.png").convert()
            if pygame.time.get_ticks() - self.cursor_timer > 50:
               self.cursor_visible = not self.cursor_visible
               self.cursor_timer = pygame.time.get_ticks()
               self.tela.blit(fundo_tela, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                if pygame.time.get_ticks() - self.cursor_timer > 50:
                  self.cursor_visible = not self.cursor_visible
                  self.cursor_timer = pygame.time.get_ticks()
                  self.tela.blit(fundo_tela, (0, 0))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.ativo = True
                    else:
                        self.ativo = False

                if event.type == pygame.KEYDOWN and self.ativo:
                    if event.key == pygame.K_RETURN:
                        if self.texto_input.strip():
                            self.nomes_jogadores.append(self.texto_input.strip())
                            self.texto_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.texto_input = self.texto_input[:-1]
                    else:
                        self.texto_input += event.unicode

            
            
            instrucoes = self.fonte.render("Digite os nomes e pressione Enter:", True, (255, 255, 255))
            self.tela.blit(instrucoes, (750, 200))

            
            pygame.draw.rect(self.tela, (255, 255, 255), self.input_box, 2)
            txt_surface = self.fonte.render(self.texto_input, True, (255, 255, 255))
            self.tela.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
            if self.ativo and self.cursor_visible:
               cursor_x = self.input_box.x + 5 + txt_surface.get_width() + 2
               cursor_y = self.input_box.y + 5
               pygame.draw.line(self.tela, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + txt_surface.get_height()), 2)


            
            y_base = self.input_box.y + 60
            for i, nome in enumerate(self.nomes_jogadores[-5:]):  # mostra últimos 5
                nome_render = self.fonte.render(f"{i+1}. {nome}", True, (200, 200, 200))
                self.tela.blit(nome_render, (self.input_box.x, y_base + i * 30))

            
            botao_concluir = pygame.Rect(1050, 400, 160, 50)
            cor = (0, 200, 0) if botao_concluir.collidepoint(pygame.mouse.get_pos()) else (0, 255, 0)
            pygame.draw.rect(self.tela, cor, botao_concluir)
            texto = self.fonte.render("Concluir", True, (255, 255, 255))
            self.tela.blit(texto, (botao_concluir.x + 25, botao_concluir.y + 10))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_concluir.collidepoint(pygame.mouse.get_pos()):
                    rodando = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return self.salvar_jogadores()

    def salvar_jogadores(self):
        jogadores = []
        last_id = select_max_id()
        for i, nome in enumerate(self.nomes_jogadores, start=1):
            jogador = Player(last_id + i, nome, "", [], True)
            add_student(jogador)
            jogadores.append(jogador)
        return jogadores
