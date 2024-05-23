from enum import Enum


class EtatDemande(Enum):
    SENT = "Envoyée"
    IN_PROGRESS = "En cours"
    DONE = "Terminée"
    APPROVED = "Approuvée"
    ARCHIVED = "Archivée"
