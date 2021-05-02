import faust


class TransactionModel(faust.Record):
    txn_hash: str
    from_address: str
    to_address: str
    value: float

    def __str__(self):
        return f"{self.from_address}-{self.to_address} {self.value}"
