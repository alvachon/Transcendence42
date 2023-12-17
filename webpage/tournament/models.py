#from django.contrib.auth.models import AbstractBaseTournament
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, OperationalError, IntegrityError
#from django.utils import timezone
#from .manager import TournamentManager


class Tournament(models.Model):
    # Fields of table Tournaments_Tournament
    id              = models.AutoField    (primary_key=True)
    max_players     = models.IntegerField (default=4)
    group_size      = models.IntegerField (default=2)
    
    tag_groupA      = models.CharField    (max_length=1, default='A')#Round1
    tag_groupB      = models.CharField    (max_length=1, default='B')#Round1
    tag_groupC      = models.CharField    (max_length=1, default='C')#Round2
    
    # members         = models.ManyToManyField();

    groupAGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupAGame', null=True, blank=True)#Round1
    groupBGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupBGame', null=True, blank=True)#Round1
    groupCGame      = models.ForeignKey   ('game.Game', on_delete=models.CASCADE, related_name='groupCGame', null=True, blank=True)#Round2
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_active       = models.BooleanField (default=False) #status online/offline

    # TournamentNAME_FIELD = "id"

    # Method that return a string with the information of the Tournament
    # objects = TournamentManager()

    def __str__(self):
        return f"Tournament {self.id} : {self.max_players} players, {self.group_size} players per group."


    @property
    def current_tournament(self):
        try:
            print('Tournament Model :: current_tournament')
            cur_tournaments = self.tournament_set.filter(is_active=True)
        except ObjectDoesNotExist:
            print('Tournament Model :: ObjectDoesNotExist')
            return None
        
        print('Tournament Model :: cur_tournaments.count() : ', cur_tournaments.count())
        if cur_tournaments.count() > 1:
            raise IntegrityError('Tournament should not be referenced in multiple running tournaments.')
        else:
            return cur_tournaments.first()

    @property
    def winner(self):
        if not self.groupCGame:
            return None
        return self.groupCGame.winner

    def addGroupAGame(self, game):
        self.groupAGame = game


    # @property
    # def is_intournament(self):
    #     return (self.current_tournament is not None)
    
    # @property
    # def round_tracking(self):
    #     try:    return self.tournament_set.filter(Tournament=self.id).count()
    #     except ObjectDoesNotExist: return 0

    # @property
    # def define_winners(self):
    #     try:    return self.tournament_set.filter(winner=self.id).count()
    #     except ObjectDoesNotExist: return 0

    # @property
    # def nb_losses(self):
    #     try:    return self.round_tracking - self.define_winners - self.nb_given_up
    #     except ObjectDoesNotExist: return 0
    
    # @property
    # def nb_given_up(self):
    #     try:    return self.tournament_set.filter(Tournament=self.id, gave_up=True).count()
    #     except ObjectDoesNotExist: return 0

    def join_tournament(self, tournament):
        cur_tournament = self.current_tournament
        if cur_tournament == tournament:
            return
        if cur_tournament and cur_tournament != tournament:
            raise OperationalError('Tournament trying to join tournament while already member of another.')

        tournament.add_player(self)
        self.save()


