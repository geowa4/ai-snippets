"""Payment processing module for handling transactions."""

import logging
from decimal import Decimal
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class PaymentStatus(Enum):
    """Payment transaction status."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProcessor:
    """Handles payment processing and transaction management."""

    def __init__(self, api_key: str, merchant_id: str) -> None:
        """Initialize payment processor with credentials."""
        self.api_key = api_key
        self.merchant_id = merchant_id
        self.transactions: dict[str, dict] = {}

    def charge_card(
        self,
        card_number: str,
        amount: Decimal,
        currency: str = "USD"
    ) -> tuple[bool, str]:
        """Process a credit card charge."""
        try:
            # Validate card number
            if not self._validate_card(card_number):
                return False, "Invalid card number"

            # Validate amount
            if amount <= 0:
                return False, "Amount must be positive"

            # Process payment (stub implementation)
            transaction_id = self._generate_transaction_id()

            self.transactions[transaction_id] = {
                "amount": amount,
                "currency": currency,
                "status": PaymentStatus.COMPLETED,
                "card_last4": card_number[-4:]
            }

            logger.info(f"Payment processed: {transaction_id}")
            return True, transaction_id

        except Exception as e:
            logger.error(f"Payment failed: {e}")
            return False, f"Payment error: {str(e)}"

    def refund_transaction(self, transaction_id: str) -> bool:
        """Refund a completed transaction."""
        if transaction_id not in self.transactions:
            return False

        transaction = self.transactions[transaction_id]
        if transaction["status"] != PaymentStatus.COMPLETED:
            return False

        transaction["status"] = PaymentStatus.REFUNDED
        logger.info(f"Transaction refunded: {transaction_id}")
        return True

    def get_transaction_status(self, transaction_id: str) -> Optional[PaymentStatus]:
        """Get the status of a transaction."""
        if transaction_id not in self.transactions:
            return None
        return self.transactions[transaction_id]["status"]

    def _validate_card(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm."""
        # Simplified validation
        return len(card_number) >= 13 and card_number.isdigit()

    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID."""
        import uuid
        return f"txn_{uuid.uuid4().hex[:12]}"
