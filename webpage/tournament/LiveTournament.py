import sys
from game.MatchMaker import LobbyGame, LobbyPlayer
from users.models import User
from tournament.models import Tournament
from tournament.consumers import TournamentConnector
from asgiref.sync import sync_to_async


def eprint(*args):
    print(*args, file=sys.stderr)


class LiveTournamentException(Exception):
    pass

class LiveTournament:
    __id_counter = 0
    gameConnectorFactory: callable = None
    gameManager: callable = None

    @classmethod
    def set_gameconnector_initializer(cls, gameConnectorClass):
        if not cls.gameConnectorFactory:
            cls.gameManager = gameConnectorClass
    @classmethod
    def set_gamemanager_initializer(cls, gameManagerRef):
        if not cls.gameManager:
            cls.gameManager = gameManagerRef

    def __init__(self, tconn, initLobbyGame: LobbyGame):

        self.__id = self.get_id()
        self.__tconn = tconn

        # Pseudo lobby only used as tournamanent initializer
        self.__init_lobby = initLobbyGame

        self._groupA: LobbyGame = None
        self._groupB: LobbyGame = None
        self._groupC: LobbyGame = None



    @classmethod
    def get_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    @property
    def init_lobby(self):
        return self.__init_lobby

    @property
    def is_first_stage(self):
        return self._groupC is None
    @property
    def is_second_stage(self):
        return self._groupC is not None
    @property
    def tournament(self):
        return self.__tconn.tournament

    @property
    def connector(self):
        return self.__tconn

    @property
    def is_setup(self):
        return self.__init_lobby and self._groupA and self._groupB
    
    # def add_member(self, user: User):
    #     self.tournament.add_member(user)

    @sync_to_async
    def setup_game_lobbies_start(self):
        if not self.__init_lobby:
            raise ValueError('LiveTournament trying to setup_game_lobbies_start() while not initLobby exist')
        formStage1 = {
            'gameMode': 'Multiplayer',
            'gameType': 'Pong',
            'withAI': False,
            'eventID': 0,
        }
        plys = self.__init_lobby.players

        # if len(plys) != 2:
        if len(plys) != 4:
            raise ValueError(f'LiveTournament trying to setup_game_lobbies_start while missing players in init_lobby ({len(plys)}).')

        eprint('setup_game_lobbies_start :: players : ', plys)
        for ply in plys:
            self.tournament.add_member(ply.user)

        players = self.__init_lobby.players

        eprint('GroupA players: ', players[:2])
        eprint('GroupB players: ', players[2:])

        # Do sophisticated Player Matching
        self._groupA = LobbyGame(formStage1, players[:2])
        self._groupB = LobbyGame(formStage1, players[2:])

        ## ... Start both tournament games
        self.tournament.addGroupAGame(self._groupA)
        self.tournament.addGroupBGame(self._groupB)
        self.tournament.declare_started()
        return (self._groupA, self._groupB)



    async def connect_player(self, user: User, consumer):

        if self._groupA and user in self._groupA:
            lgame = self._groupA
            lply = LobbyPlayer(user, is_connected=True, is_ready=True)
            self._groupA.add_player(lply)
        elif self._groupB and user in self._groupB:
            lgame = self._groupB
        elif self._groupC and user in self._groupC:
            lgame = self._groupC
        else:
            raise LiveTournamentException("Trying to connect_player to LiveTournament, but either the tournament hasn't been setup properly or The player isn't a member of any toiurnament game.")

        sockID = lgame.sockID
        if not lgame.game_connector:
            gconn = self.gameConnectorFactory(sockID)
            lgame.set_game_connector(gconn)
            gconn.set_lobby_game(lgame)
        else:
            gconn = lgame.game_connector


        await gconn.connect_player(consumer.user, consumer, is_tournament_stage1=True)
        await gconn.send_init_state(self.gameManager.getInitInfo(lgame.gameType))




    def __get_bracket_template(self):
        return {
            'groupA': {
                'p1': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'p2': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            },
            'groupB': {
                'p3': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'p4': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            },
            'groupC': {
                'winner1': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
                'winner1': {
                    'login': None,
                    'score': '-',
                    'won': False
                },
            }
        }

    def get_brackets_info(self):
        brackets = self.__get_bracket_template()
        plys_list = self.__init_lobby.players

        if self._groupA:
            gconnA = self._groupA.game_connector
            gameA = gconnA.game
            if gameA.winner == plys_list[0].id:
                winnerA = plys_list[0]
                brackets['groupA']['p1']['won'] = True
            elif gameA.winner == plys_list[1].id:
                winnerA = plys_list[1]
                brackets['groupA']['p2']['won'] = True

        if self._groupB:
            gconnB = self._groupC.game_connector
            gameB = gconnB.game
            if gameB.winner == plys_list[2].id:
                winnerB = plys_list[2]
                brackets['groupB']['p3']['won'] = True
            elif gameB.winner == plys_list[3].id:
                winnerB = plys_list[3]
                brackets['groupB']['p4']['won'] = True

        if self._groupC:
            gconnC = self._groupC.game_connector
            gameC = gconnC.game
            if gameC.winner == winnerA.id:
                winnerC = winnerA
                brackets['groupC']['winner1']['won'] = True
            elif gameC.winner == winnerB.id:
                winnerC = winnerB
                brackets['groupC']['winner2']['won'] = True

        if len(plys_list) > 0:
            brackets['groupA']['p1']['login'] = plys_list[0].login
        elif len(plys_list) > 1:
            brackets['groupA']['p2']['login'] = plys_list[1].login
        elif len(plys_list) > 2:
            brackets['groupB']['p3']['login'] = plys_list[2].login
        elif len(plys_list) > 3:
            brackets['groupB']['p4']['login'] = plys_list[3].login

        return brackets



    # def __contains__(self, game: LobbyGame):
    #     return next((True for g in self if g == game), False)

    # def __iter__(self):
    #     if self._groupA:
    #         yield self._groupA
    #     if self._groupB:
    #         yield self._groupB
    #     if self._groupC:
    #         yield self._groupC

    # def __repr__(self):
    #     return f"Tournament {self.__id}, {self.__tconn}"

    # @property
    # def id(self):
    #     return self.__id

    # @property
    # def tconn(self):
    #     return self.__tconn

    # @tconn.setter
    # def tconn(self, value):
    #     self.__tconn = value

    # @property
    # def groupA(self):
    #     return self._groupA

    # @groupA.setter
    # def groupA(self, value):
    #     self._groupA = value

    # @property
    # def groupB(self):
    #     return self._groupB

    # @groupB.setter
    # def groupB(self, value):
    #     self._groupB = value

    # @property
    # def groupC(self):
    #     return self._groupC

    # @groupC.setter
    # def groupC(self, value):
    #     self._groupC = value

    # @property
    # def is_full_R1(self):
    #     return self._groupA and self._groupB

    # @property
    # def is_full_R2(self):
    #     return self._groupC

#    @property
#    def is_readyR1(self):
#        return not self._groupA.is_ready and self._groupB.is_ready

#     @property
#     def is_readyR2(self):
#         return not self._groupC.is_ready




    #  SETTER  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    #  EVENTS  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

