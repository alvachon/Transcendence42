from django import forms

class GameCreationForm(forms.Form):
#    your_name = forms.CharField(label="Your name", max_length=100)
    gameMode = forms.CharField(label='gameMode', max_length=10, required=True)
    gameType = forms.CharField(label='gameType', max_length=10, required=True)

    # If game is tournament, this is the id of the specific tournament to join, else it is id of specific game to join.
    withAI = forms.CharField(label='withAI', max_length=10, required=False)
    eventID = forms.CharField(label='eventID', max_length=10, required=False)
