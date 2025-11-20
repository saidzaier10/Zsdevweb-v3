"""
Validateurs pour l'application quotes
Centralise toute la logique de validation pour éviter la duplication
"""
from decimal import Decimal
from typing import Dict, Optional, Tuple
from .constants import (
    QuoteStatus,
    DiscountType,
    ErrorMessages,
    ValidationLimits,
)


class QuoteValidator:
    """Validateur pour les devis et leurs données associées"""

    @staticmethod
    def validate_discount(
        discount_type: Optional[str],
        discount_value: Optional[Decimal],
        total_ht: Decimal
    ) -> Tuple[bool, Optional[str]]:
        """
        Valide une remise appliquée à un devis

        Args:
            discount_type: Type de remise ('percent' ou 'fixed')
            discount_value: Valeur de la remise
            total_ht: Montant HT total du devis

        Returns:
            Tuple (is_valid, error_message)
        """
        if not discount_type or not discount_value:
            return True, None

        if discount_value < 0:
            return False, ErrorMessages.INVALID_DISCOUNT_VALUE

        if discount_type == DiscountType.PERCENT:
            if discount_value < ValidationLimits.MIN_DISCOUNT_PERCENT:
                return False, ErrorMessages.INVALID_DISCOUNT_VALUE
            if discount_value > ValidationLimits.MAX_DISCOUNT_PERCENT:
                return False, ErrorMessages.INVALID_DISCOUNT_VALUE

        elif discount_type == DiscountType.FIXED:
            if discount_value > total_ht:
                return False, ErrorMessages.DISCOUNT_EXCEEDS_TOTAL

        return True, None

    @staticmethod
    def validate_signature_data(data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Valide les données de signature d'un devis

        Args:
            data: Dictionnaire contenant les données de signature

        Returns:
            Tuple (is_valid, error_message)
        """
        # Vérifier la présence des champs obligatoires
        if 'signature' not in data or 'signer_name' not in data:
            return False, ErrorMessages.SIGNATURE_DATA_INCOMPLETE

        # Vérifier que la signature n'est pas vide
        signature = data.get('signature', '').strip()
        if not signature:
            return False, ErrorMessages.SIGNATURE_INVALID

        # Vérifier le format de la signature (data URL)
        if not signature.startswith('data:image/'):
            return False, ErrorMessages.SIGNATURE_INVALID

        # Vérifier le nom du signataire
        signer_name = data.get('signer_name', '').strip()
        if not signer_name:
            return False, ErrorMessages.SIGNATURE_NAME_REQUIRED

        # Vérifier l'acceptation des conditions
        terms_accepted = data.get('terms_accepted', False)
        if not terms_accepted:
            return False, ErrorMessages.TERMS_NOT_ACCEPTED

        return True, None

    @staticmethod
    def can_sign_quote(quote) -> Tuple[bool, Optional[str]]:
        """
        Vérifie si un devis peut être signé

        Args:
            quote: Instance de Quote

        Returns:
            Tuple (can_sign, error_message)
        """
        # Vérifier si déjà signé
        if quote.signed_at:
            return False, ErrorMessages.QUOTE_ALREADY_SIGNED

        # Vérifier si expiré
        if quote.is_expired:
            return False, ErrorMessages.QUOTE_EXPIRED

        # Vérifier le statut
        if quote.status not in QuoteStatus.SIGNABLE_STATUSES:
            return False, f"Le statut actuel ({quote.get_status_display()}) ne permet pas la signature"

        return True, None

    @staticmethod
    def can_edit_quote(quote) -> Tuple[bool, Optional[str]]:
        """
        Vérifie si un devis peut être modifié

        Args:
            quote: Instance de Quote

        Returns:
            Tuple (can_edit, error_message)
        """
        if quote.status not in QuoteStatus.EDITABLE_STATUSES:
            return False, f"Le statut actuel ({quote.get_status_display()}) ne permet pas la modification"

        if quote.signed_at:
            return False, "Un devis signé ne peut pas être modifié"

        return True, None

    @staticmethod
    def can_resend_quote(quote) -> Tuple[bool, Optional[str]]:
        """
        Vérifie si un devis peut être renvoyé

        Args:
            quote: Instance de Quote

        Returns:
            Tuple (can_resend, error_message)
        """
        if quote.status not in QuoteStatus.RESENDABLE_STATUSES:
            return False, f"Le statut actuel ({quote.get_status_display()}) ne permet pas le renvoi"

        if quote.is_expired:
            return False, ErrorMessages.QUOTE_EXPIRED

        return True, None

    @staticmethod
    def can_reject_quote(quote) -> Tuple[bool, Optional[str]]:
        """
        Vérifie si un devis peut être rejeté

        Args:
            quote: Instance de Quote

        Returns:
            Tuple (can_reject, error_message)
        """
        if quote.status == QuoteStatus.ACCEPTED:
            return False, ErrorMessages.QUOTE_ACCEPTED_CANNOT_REJECT

        if quote.signed_at:
            return False, "Un devis signé ne peut pas être rejeté"

        return True, None

    @staticmethod
    def validate_tva_rate(tva_rate: Decimal) -> Tuple[bool, Optional[str]]:
        """
        Valide un taux de TVA

        Args:
            tva_rate: Taux de TVA à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        if tva_rate < ValidationLimits.MIN_TVA_RATE:
            return False, f"Le taux de TVA ne peut pas être négatif"

        if tva_rate > ValidationLimits.MAX_TVA_RATE:
            return False, f"Le taux de TVA ne peut pas dépasser {ValidationLimits.MAX_TVA_RATE}%"

        return True, None

    @staticmethod
    def validate_price(price: Decimal, field_name: str = "Prix") -> Tuple[bool, Optional[str]]:
        """
        Valide un prix

        Args:
            price: Prix à valider
            field_name: Nom du champ pour le message d'erreur

        Returns:
            Tuple (is_valid, error_message)
        """
        if price < ValidationLimits.MIN_PRICE:
            return False, f"{field_name} ne peut pas être négatif"

        if price > ValidationLimits.MAX_PRICE:
            return False, f"{field_name} ne peut pas dépasser {ValidationLimits.MAX_PRICE}€"

        return True, None
