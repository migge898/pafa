import random


DEFAULT_POD_LIST = {
    "services": [
        {
            "name": "bugticketsvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "bugticketsvc-main-1",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "bugticketsvc-main-2",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "paymentsvc-main-0",
            "ready": "3/3",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "paymentsvc-main-1",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "userauthsvc-main-0",
            "ready": "7/7",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-1",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-2",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-1",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-2",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
    ]
}


class Pairings:
    # 90% of the time, the number of tickets is between 10 and 30, otherwise it's between 31 and 100
    _ticket_num = lambda: (
        random.randint(10, 30) if random.random() < 0.9 else random.randint(31, 100)
    )
    _tag = lambda: random.choice(["paymentservice", "client", "launcher", "misc"])
    # Cpu over 10, 20 or 30
    _cpu_usage = lambda: random.choice([10, 20, 30])

    # infos = lambda x: list(filter(lambda x: x[0] == "INFO", x))
    # warns = lambda x: list(filter(lambda x: x[0] == "WARN", x))
    # returns a list of weights for the pairings like: 3 * [0.95] + 2 * [0.05] = [0.95, 0.95, 0.95, 0.05, 0.05]
    # weights_gen = lambda pairings, warn_weight: len(infos(pairings)) * [(1 - warn_weight)] + len(warns(pairings)) * [warn_weight]
    @staticmethod
    def _infos(x):
        return list(filter(lambda y: y[0] == "INFO", x))

    @staticmethod
    def _warns(x):
        return list(filter(lambda y: y[0] == "WARN", x))

    @staticmethod
    def _weights_gen(pairings, warn_weight):
        return len(Pairings._infos(pairings)) * [(1 - warn_weight)] + len(
            Pairings._warns(pairings)
        ) * [warn_weight]

    _BUG_TICKET_SVC = [
        ("INFO", f"{_ticket_num()} new open tickets for tag: {_tag()}"),
        ("INFO", f"{_ticket_num()} tickets have been closed for tag: {_tag()}"),
        ("INFO", f"{_ticket_num()// 3} tickets have been reopened for tag: {_tag()}"),
        ("INFO", f"{_ticket_num()*2//3} tickets have been assigned for tag: {_tag()}"),
        ("INFO", f"{_ticket_num()} tickets have been resolved for tag: {_tag()}"),
        (
            "WARN",
            f"{_ticket_num()// 5} tickets with tag {_tag()} have not been resolved for more than 3 days:",
        ),
        ("WARN", f"CPU usage of this pod over {_cpu_usage()}%."),
    ]

    _PAYMENT_SVC = []
    _USER_AUTH_SVC = []
    _MESSAGE_SVC = []
    _PLAYER_STATS_SVC = []

    @staticmethod
    def generate_bug_ticket_svc(num_rows: int, warn_weight: float = 0.05):
        weights = Pairings._weights_gen(Pairings._BUG_TICKET_SVC, warn_weight)
        return random.choices(
            Pairings._BUG_TICKET_SVC,
            k=num_rows,
            weights=weights,
        )

    @staticmethod
    def generate_payment_svc(num_rows: int, warn_weight: float = 0.05):
        raise NotImplementedError("generate_payment_svc not implemented")
        return random.choices(
            Pairings._PAYMENT_SVC,
            k=num_rows,
            weights=Pairings()._weights_gen(Pairings._PAYMENT_SVC, warn_weight),
        )

    @staticmethod
    def generate_user_auth_svc(num_rows: int, warn_weight: float = 0.05):
        raise NotImplementedError("generate_user_auth_svc not implemented")
        return random.choices(
            Pairings._USER_AUTH_SVC,
            k=num_rows,
            weights=Pairings()._weights_gen(Pairings._USER_AUTH_SVC, warn_weight),
        )

    @staticmethod
    def generate_message_svc(num_rows: int, warn_weight: float = 0.05):
        raise NotImplementedError("generate_message_svc not implemented")
        return random.choices(
            Pairings._MESSAGE_SVC,
            k=num_rows,
            weights=Pairings()._weights_gen(Pairings._MESSAGE_SVC, warn_weight),
        )

    @staticmethod
    def generate_player_stats_svc(num_rows: int, warn_weight: float = 0.05):
        raise NotImplementedError("generate_player_stats_svc not implemented")
        return random.choices(
            Pairings.PLAYER_STATS_SVC,
            k=num_rows,
            weights=Pairings()._weights_gen(Pairings._PLAYER_STATS_SVC, warn_weight),
        )
