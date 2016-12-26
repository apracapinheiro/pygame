class World(object):

    def __init__(self):
        self.entities = {}  # armazena todas as entidades
        self.entity_id = 0  # ultimo id de entidade atribuido

        # Desenha o formigueiro (um circulo) no background
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((0, 0, 0))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))

    def add_entity(self, entity):
        # Armazena a entidade e incrementa o id atual
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        # Encontra a entidade, dado o seu id (ou retorna None se ela nao for encontrada)
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):
        # Processa todas as entidades do mundo do jogo
        time_passed_seconds = time_passed / 1000.0

        for entity in self.entities.itervalues():
            entity.process(time_passed_seconds)

    def render(self, surface):
        # desenha o background e todas as entidades
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, e_range=100):
        # encontra uma entidade em um raio a partir de uma posicao
        location = Vector2(*location)

        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < e_range:
                    return entity
        return None