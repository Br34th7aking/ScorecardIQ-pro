class Wicket:
    """ """

    def __init__(self, kind, player_out, fielders=[]):
        """

        Parameters
        ------------
          kind: str
            Type of dismissal of the player

          player_out: str
            Name of the player who got out

          fielders: array of objects
            Players from the fielding team who were involved in the dismissal
        """
        self.kind = kind
        self.player_out = player_out
        self.fielders = fielders

    def __str__(self) -> str:
        """
          Return the details of the dismissal
        """
        return f'{self.player_out} is out {self.kind}'
