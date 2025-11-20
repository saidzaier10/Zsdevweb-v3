"""
Décorateurs pour l'application quotes
Centralise la gestion des erreurs et le logging
"""
import logging
from functools import wraps
from typing import Any, Callable
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def handle_service_errors(func: Callable) -> Callable:
    """
    Décorateur pour gérer les erreurs des services de manière uniforme

    Capture les exceptions et retourne une réponse d'erreur appropriée
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Erreur de validation dans {func.__name__}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionError as e:
            logger.warning(f"Erreur de permission dans {func.__name__}: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except FileNotFoundError as e:
            logger.error(f"Fichier non trouvé dans {func.__name__}: {str(e)}")
            return Response(
                {'error': "Ressource non trouvée"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Erreur inattendue dans {func.__name__}: {str(e)}", exc_info=True)
            return Response(
                {'error': "Une erreur inattendue s'est produite"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper


def log_quote_action(action: str):
    """
    Décorateur pour logger les actions sur les devis

    Args:
        action: Description de l'action effectuée
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Essayer de trouver l'ID du devis dans les arguments
            quote_id = None
            if args and hasattr(args[0], 'id'):
                quote_id = args[0].id
            elif 'quote_id' in kwargs:
                quote_id = kwargs['quote_id']
            elif 'pk' in kwargs:
                quote_id = kwargs['pk']

            log_prefix = f"[Devis {quote_id}]" if quote_id else "[Devis]"

            logger.info(f"{log_prefix} Début: {action}")

            try:
                result = func(*args, **kwargs)
                logger.info(f"{log_prefix} Succès: {action}")
                return result
            except Exception as e:
                logger.error(f"{log_prefix} Échec: {action} - {str(e)}")
                raise

        return wrapper
    return decorator
