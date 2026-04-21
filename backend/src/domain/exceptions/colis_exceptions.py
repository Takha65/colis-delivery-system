"""Exceptions specifiques au domaine Colis."""


class ColisError(Exception):
    """Exception de base pour toutes les erreurs liees aux colis."""


class ColisNotFoundError(ColisError):
    """Leve lorsqu'un colis demande n'existe pas."""

    def __init__(self, colis_id: str) -> None:
        super().__init__(f"Colis avec id '{colis_id}' introuvable")
        self.colis_id = colis_id


class InvalidColisError(ColisError):
    """Leve lorsqu'un colis a des donnees invalides."""


class InvalidTransitionError(ColisError):
    """Leve lorsqu'une transition d'etat est impossible."""

    def __init__(self, statut_actuel: str, statut_cible: str) -> None:
        super().__init__(
            f"Transition impossible de '{statut_actuel}' vers '{statut_cible}'"
        )
        self.statut_actuel = statut_actuel
        self.statut_cible = statut_cible
