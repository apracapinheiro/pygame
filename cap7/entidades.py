class GameEntity(object):
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2(0, 0)
        self.destination = Vector2(0, 0)
        self.speed = 0.
        self.brain = StateMachine()
        self.id = 0

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def process(self, time_passed):
        self.brain.think()

        if self.speed > 0 and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading


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


class Ant(GameEntity):

    def __init__(self, world, image):
        # chama o construtor da classe-base
        GameEntity.__init__(self, world, "ant", image)

        # cria instancias de cada um dos estados
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        # adiciona os estados a maquina de estados(self.brain)
        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)

        self.carry_image = None

    def carry(self, image):
        self.carry_image = image

    def drop(self, surface):
        # faz o blit da imagem 'carregada' no background e a reinicializa
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x-w, y-h/2))
            self.carry_image = None

    def render(self, surface):
        # chama a funcao render da classe-base
        GameEntity.render(self, surface)

        # codigo extra para renderizar a imagem 'carregada'
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))


class State(object):

    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_action(self):
        pass


class StateMachine(object):

    def __init__(self):
        self.state = {}  # armazena os estados
        self.active_state = None  # o estado ativo no momento

    def add_state(self, state):
        # adiciona um estado ao dicionario interno
        self.states[state.name] = state

    def think(self):
        #  continua somente se houver um estado ativo
        if self.active_state is None:
            return
        #  executa as acoes do estado ativo e verifica as condicoes
        self.active_state.do_actions()

        new_state_name = self.active_state.check_conditions()
        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        #  muda de estado e executa as acoes de saida/entrada
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.exit_actions()


class AntStateExploring(State):

    def __init__(self, ant):
        # chama o construtor da classe-base para inicializar State
        State.__init__(self, "exploring")
        # define a formiga que este State manipulará
        self.ant = ant

    def random_destination(self):
        # seleciona um ponto na tela
        w, h = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, w), range(0, h))

    def do_actions(self):
        # muda a direcao, 1 vez a cada 20 segundos
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        # se houver uma folha nas proximidades, muda para o estado Seeking(buscando)
        leaf = self.ant.world.get_close_entity("leaf", self.ant.location)
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return "seeking"

        # se houver uma aranha nas proximidades, muda para o estado Hunting(cacando)
        spider = self.ant.world.get_close_entity("spider", NEST_POSITION, NEST_SIZE)
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100.:
                self.ant.spider_id = spider.id
                return "hunting"

        return None

    def entry_actions(self):
        # comeca com velocidade e direcao aleatorias
        self.ant.speed = 120. + randint(-30, 30)
        self.random_destination()