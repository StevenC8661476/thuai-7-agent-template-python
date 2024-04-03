import json

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Message:
    def __init__(self):
        self._message = {}

    def json(self):
        return json.dumps(self._message)

class PerformAbandonMessage(Message):
    def __init__(self, numb: int, token: str, targetSupply: str):
        super().__init__()
        self._message["messageType"] = "PERFORM_ABANDON"
        self._message["numb"] = numb
        self._message["token"] = token
        self._message["targetSupply"] = targetSupply

class PerformPickUpMessage(Message):
    def __init__(self, token: str, targetSupply: str, num: int, targetPosition: Position):
        super().__init__()
        self._message["messageType"] = "PERFORM_PICKUP"
        self._message["token"] = token
        self._message["targetSupply"] = targetSupply
        self._message["num"] = num
        self._message["targetPosition"] = {"x": targetPosition.x, "y": targetPosition.y}

class PerformSwitchArmMessage(Message):
    def __init__(self, token: str, targetFirearm: str):
        super().__init__()
        self._message["messageType"] = "PERFORM_SWITCH_ARM"
        self._message["token"] = token
        self._message["targetFirearm"] = targetFirearm

class PerformUseMedicineMessage(Message):
    def __init__(self, token: str, medicineName: str):
        super().__init__()
        self._message["messageType"] = "PERFORM_USE_MEDICINE"
        self._message["token"] = token
        self._message["medicineName"] = medicineName

class PerformUseGrenadeMessage(Message):
    def __init__(self, token: str, targetPosition: Position):
        super().__init__()
        self._message["messageType"] = "PERFORM_USE_GRENADE"
        self._message["token"] = token
        self._message["targetPosition"] = {"x": targetPosition.x, "y": targetPosition.y}

class PerformMoveMessage(Message):
    def __init__(self, token: str, destination: Position):
        super().__init__()
        self._message["messageType"] = "PERFORM_MOVE"
        self._message["token"] = token
        self._message["destination"] = {"x": destination.x, "y": destination.y}

class PerformStopMessage(Message):
    def __init__(self, token: str):
        super().__init__()
        self._message["messageType"] = "PERFORM_STOP"
        self._message["token"] = token

class PerformAttackMessage(Message):
    def __init__(self, token: str, targetPosition: Position):
        super().__init__()
        self._message["messageType"] = "PERFORM_ATTACK"
        self._message["token"] = token
        self._message["targetPosition"] = {"x": targetPosition.x, "y": targetPosition.y}

class GetPlayerInfoMessage(Message):
    def __init__(self, token: str):
        super().__init__()
        self._message["messageType"] = "GET_PLAYER_INFO"
        self._message["token"] = token

class GetMapMessage(Message):
    def __init__(self, token: str):
        super().__init__()
        self._message["messageType"] = "GET_MAP"
        self._message["token"] = token

class ChooseOriginMessage(Message):
    def __init__(self, token: str, originPosition: Position):
        super().__init__()
        self._message["messageType"] = "CHOOSE_ORIGIN"
        self._message["token"] = token
        self._message["originPosition"] = {"x": originPosition.x, "y": originPosition.y}
