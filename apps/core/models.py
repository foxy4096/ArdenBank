from django.db import models
from django.contrib.auth import get_user_model
from secrets import SystemRandom as sr


class Account(models.Model):
    """
    This is a simple Account models which is connected to the django's default user model.
    """

    SECURITY_QUESTION = (
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What is your best friend's name?", "What is your best friend's name?"),
        ("What is your favorite color?", "What is your favorite color?"),
        ("What is your favorite movie?", "What is your favorite movie?"),
        ("What is your favorite food?", "What is your favorite food?"),
        ("What is your favorite sport?", "What is your favorite sport?"),
        ("What is your favorite book?", "What is your favorite book?"),
        ("What is your favorite animal?", "What is your favorite animal?"),
        ("What is your favorite TV show?", "What is your favorite TV show?"),
        ("What is your favorite band?", "What is your favorite band?"),
        ("What is your favorite musician?", "What is your favorite musician?"),
        ("What is your favorite actor?", "What is your favorite actor?"),
        ("What is your favorite game?", "What is your favorite game?"),
        ("What is your favorite TV show?", "What is your favorite TV show?"),
        ("What is your favorite TV show?", "What is your favorite TV show?"),
        ("What is your favorite actress?", "What is your favorite actress?"),
        ("What is your favorite game?", "What is your favorite game?"),
        ("What is your favorite TV genre?", "What is your favorite TV genre?"),
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    account_number = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    security_question = models.CharField(
        max_length=100,
        choices=SECURITY_QUESTION,
        default="What is your mother's maiden name?",
    )
    answer_digest = models.CharField(
        verbose_name="Answer",
        help_text="The answer will be saved in the form of hash digest so no one even us can see the real answer",
        max_length=100,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account_number} {self.user.get_full_name()}"

    def generate_account_no(self):
        """
        A simple code snipped to generate the account no.
        """
        return sr().randint(100000000000, 999999999999)

    def status(self):
        return "Active" if self.is_active else "Inactive"

    def save(self, *args, **kwargs):
        """
        Overriding the default save method to save the account with account no.
        """
        if self.account_number is None:
            account_no = self.generate_account_no()
            self.account_number = account_no
        super().save(*args, **kwargs)

    def deposit(self, amount):
        """
        A simple method to deposit the amount into the account.
        """
        self.balance += amount
        Transaction.objects.create(
            receiver=self,
            transaction_type="Deposit",
            amount=amount,
            description="Deposit from the bank",
        )
        self.save()

    def transfer(self, amount, receiver):
        """
        A simple method to transfer the amount into the account.
        """
        receiver_ac = Account.objects.filter(account_number=receiver)
        if self.balance >= amount and receiver_ac.exists() and receiver_ac[0] != self:
            self.balance -= amount
            receiver_ac = receiver_ac[0]
            receiver_ac.balance += amount
            Transaction.objects.create(
                sender=self,
                receiver=receiver_ac,
                transaction_type="Transfer",
                amount=amount,
                description=f"Transfer of ${amount} to the {receiver_ac.user.get_full_name()}",
            )
            self.save()
            receiver_ac.save()
            return True
        else:
            return False

    def withdraw(self, amount):
        """
        A simple method to withdraw the amount from the account.
        """
        if self.balance >= amount:
            self.balance -= amount
            Transaction.objects.create(
                receiver=self,
                transaction_type="Withdrawal",
                amount=amount,
                description="Withdrawal from the bank",
            )
            self.save()
            return True
        else:
            return False


class Transaction(models.Model):
    """
    This is a simple Transaction model which is connected to the Account model.
    """

    TRANSACTION_TYPE = (
        ("Deposit", "Deposit"),
        ("Withdrawal", "Withdrawal"),
        ("Transfer", "Transfer"),
    )
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="sender", null=True, blank=True
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="receiver"
    )
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPE, default="Deposit"
    )
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.date} {self.description} {self.amount}"

    class Meta:
        ordering = ["-date"]