import pygame

class Estado:
    def __init__(self):
        self.energia = 100
        self.felicidade = 100
        self.saude = 100
        self.comida = 100
        self.fome = 0
        self.vivo = True

class Inventario:
    def __init__(self):
        self.items = []

    def adicionar(self, items):
        self.items.append(items)

    def mostrar(self):
        for i in self.items:
            print(f"Nome: {i.nome} | Qtd: {i.qtd}, Valor Nutricional: {i.nutricao}")

class Item:
    def __init__(self, nome, qtd, nutricao):
        self.nome = nome
        self.qtd = qtd
        self.nutricao = nutricao
        

class DiaNoGame:
    def __init__(self):
        self.dia = 1
        self.hora = 8
        self.acumulador = 0
        self.segundos_por_hora = 5

    def avancar(self):
        self.hora +=1 
        if self.hora >= 24:
            self.hora = 0
            self.dia += 1  

    def atualizar_dia(self, dt):
        self.acumulador += dt
        if self.acumulador >= 5:
            self.avancar()
            self.acumulador = 0

            
    @property
    def periodo(self):
        if 5 <= self.hora <= 11:
            return "Manhã"

        elif 12 <= self.hora <= 17:
            return "Tarde"

        elif 18 <= self.hora <= 23:
            return "Noite"

        elif 00 <= self.hora <= 4:
            return "Madrugada"


    def mostrar(self):
        return f"Dia {self.dia} - {self.hora:02d}:00"

    def desenhar_na_tela(self):
        pass
        

class Mapa:
    def __init__(self):
        self.chao = 500 



class Player:
    def __init__(self, type_animal , nome_falado, img, estado, y=0, x=0):
        self.type_animal = type_animal
        self.nome_falado = nome_falado
        self.img = img
        self.estado = estado
        self.y = y
        self.x = x
        self.velocidade_y = 0
        self.gravidade = 900
        self.y_chao = 500 #deve vir do mapa talvez nao precise disto assim
        self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -500
            self.no_chao = False

    def mover_direita(self):
        self.x += 5
        print(self.x)

    def mover_esquerda(self):
        self.x -= 5
        print(self.x)

    def comer(self):
        #aumentar comida nivel e tambem aumentar a felicidade e energia
        pass

    def update_pet(self, dt):
        self.velocidade_y += self.gravidade * dt # 0 = 900 * 0.016 = 
        self.y += self.velocidade_y * dt

    @property
    def esta_vivo(self):
        return self.estado.saude > 0
            

    def get_name(self):
        print(f"name is {self.nome_falado}")
        return self.nome_falado


class Game:
    def __init__(self, pet, inventario, tempo_game):
        pygame.init()
        pygame.display.set_caption("game")
        self.pet = pet
        self.inventario = inventario
        self.tempo_game = tempo_game
        self.larguura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.larguura, self.altura))
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 32)
        self.rodando = True

    def renderizar(self):
        self.tela.fill("white")

        self.desenhar_pet()
        self.desenhar_chao()
        tempo_texto = self.tempo_game.mostrar()
        self.desenhar_dia_hora(tempo_texto)
        
        pygame.display.flip()

    def desenhar_dia_hora(self, tempo_texto):
        texto_sufarce = self.fonte.render(tempo_texto, True, "black" )
        self.tela.blit(texto_sufarce, (20, 20))
        

    def desenhar_pet(self):
        pygame.draw.rect(self.tela, "black", (self.pet.x , self.pet.y, 50, 80))

    #mover para uma class Renderizar
    def desenhar_chao(self):
        pygame.draw.rect(self.tela, "green", (0, 500, 800, 80))

    

       
    def atualizar_game(self, dt):
           self.pet.update_pet(dt)
          
           teclas = pygame.key.get_pressed()

           if teclas[pygame.K_d]:
               self.pet.mover_direita()

           if teclas[pygame.K_a]:
               self.pet.mover_esquerda()


           if not self.pet.esta_vivo:
                print(f"[ALERTA] Seu pet {self.pet.nome_falado} morreu!")
                self.rodando = False

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.renderizar()
            dt= self.clock.tick(60) / 1000
            self.atualizar_game(dt)
            self.tempo_game.atualizar_dia(dt)
            
        

        pygame.quit()

    def processar_eventos(self):
        for evento in pygame.event.get():
           if evento.type == pygame.QUIT:
               self.rodando = False
           elif evento.type == pygame.KEYDOWN:
               if evento.key == pygame.K_SPACE:
                   self.pet.pular()

def main():

        inventario_instace = Inventario()
        

        #parte do inventario da casa/fazenda
        item1 = Item('Maça', 5, 5)
        item2 = Item("Uva", 10, 3)
        item3 = Item("Carne Bovida", 2, 30)

        inventario_instace.adicionar(item1)
        inventario_instace.adicionar(item2)
        inventario_instace.adicionar(item3)


        nome_pet = "mingau"
        estado = Estado()
        pet = Player('cat', nome_pet, 'cat.png',estado )
        dia = DiaNoGame()
        game = Game(pet, inventario_instace, dia)

            

        game.rodar()

 

if __name__ == '__main__':
    main()