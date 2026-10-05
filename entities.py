import re
 
from courier_delivery.value_objects import Weight
from courier_delivery.decorators import validated
 
TRACKING_PATTERN = re.compile(r"^[A-Z]{2}-\d{6,12}[A-Z]?$")
STATUS_VALUES = ("created", "in_transit", "delivered", "returned")
 
 
class Parcel:
    def __init__(self, tracking: str, weight, dest_city: str, cost: float) -> None:
        self.tracking = tracking
        self.weight = weight
        self.dest_city = dest_city
        self.cost = cost
        self._status = "created"
 
    # -- tracking -------------------------------------------------------
    @property
    def tracking(self) -> str:
        return self._tracking
 
    @tracking.setter
    def tracking(self, value: str) -> None:
        if not Parcel.is_valid_tracking(value):
            raise ValueError(
                "трек-номер посилки має бути у форматі 'XX-123456' "
                "(2 великі латинські літери, дефіс, 6-12 цифр, "
                "опційно літера в кінці)"
            )
        self._tracking = value
 
    # -- weight -----------------------------------------------------------
    @property
    def weight(self) -> Weight:
        return self._weight
 
    @weight.setter
    def weight(self, value) -> None:
        grams = value.grams if isinstance(value, Weight) else value
        if not isinstance(grams, (int, float)) or isinstance(grams, bool):
            raise ValueError("вага посилки повинна бути числом (у грамах)")
        if not (1 <= grams <= 30000):
            raise ValueError("вага посилки повинна бути в межах від 1 до 30000 грамів")
        self._weight = Weight(grams)
 
    # -- dest_city --------------------------------------------------------
    @property
    def dest_city(self) -> str:
        return self._dest_city
 
    @dest_city.setter
    def dest_city(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("місто призначення не може бути порожнім")
        self._dest_city = value.strip()
 
    # -- cost ---------------------------------------------------------------
    @property
    def cost(self) -> float:
        return self._cost
 
    @cost.setter
    def cost(self, value: float) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("вартість доставки повинна бути числом")
        if value <= 0:
            raise ValueError("вартість доставки повинна бути додатною")
        self._cost = float(value)
 
    # -- status (лише для читання ззовні; змінюється через change_status) ---
    @property
    def status(self) -> str:
        return self._status
 
    # -- зміна статусу, декорована валідаційним декоратором (5.1) -----------
    @validated(status="one_of:" + ",".join(STATUS_VALUES))
    def change_status(self, *, status: str) -> None:
        self._status = status
 
    # -- альтернативний конструктор (2.2) -----------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "Parcel":
        return cls(
            tracking=data["tracking"],
            weight=data["weight"],
            dest_city=data["dest_city"],
            cost=data["cost"],
        )
 
    # -- статичний метод перевірки формату (2.2) -----------------------------
    @staticmethod
    def is_valid_tracking(value: str) -> bool:
        if not isinstance(value, str):
            return False
        return bool(TRACKING_PATTERN.fullmatch(value))
 
    # -- рядкове подання для зручності демонстрації ------------------------
    def __repr__(self) -> str:
        return (
            f"Parcel(tracking={self.tracking!r}, weight={self.weight}, "
            f"dest_city={self.dest_city!r}, cost={self.cost}, "
            f"status={self.status!r})"
        )