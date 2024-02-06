import pandas as pd

from pafa.simulation.functions import generate_alert, generate_namespace

def init_namespaces():
    # generate needed namespaces
    generate_namespace("test-001")
    generate_namespace("test-002")
    generate_namespace("test-003")
    generate_namespace("test-004")
    generate_namespace("test-005")
    pass
def init_alerts():
    # alerts for bugticketsvc
    generate_alert(
        description="BugTicketservice in namespace test-001 is using 90% of CPU.",
        alertname="BugTicketServiceOverloaded2",
        namespace="test-001",
        pod="bugticketsvc-main-1",
        active_at_time="2024-02-06T11:09:02.330354Z"
    )
    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh",
        namespace="test-001",
        pod="bugticketsvc-main-2",
        active_at_time="2024-02-06T11:09:02.330354Z"
    )
    generate_alert(
        description="BugTicketservice in namespace test-002 is using 90% of CPU.",
        alertname="BugTicketServiceOverloaded3",
        namespace="test-002",
        pod="bugticketsvc-main-0",
        active_at_time="2024-02-06T09:40:06.331935Z"
    )
    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh2",
        namespace="test-002",
        pod="bugticketsvc-main-1",
        active_at_time="2024-02-06T08:40:06.331935Z"
    )
    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh3",
        namespace="test-003",
        pod="bugticketsvc-main-0",
        active_at_time="2024-02-06T08:40:06.331935Z"
    )
    # alerts for paymentsvc
    generate_alert(
        description="PaymentService in namespace test-000 not available.",
        alertname="PaymentServiceDown",
        namespace="test-000",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-04T19:22:47.862156Z"
    )
    generate_alert(
        description="PaymentService in namespace test-001 is using 70% of CPU.",
        alertname="PaymentServiceOverloaded",
        namespace="test-002",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-05T22:57:37.332298Z"
    )
    generate_alert(
        description="No transactions from America-North in last 30 minutes.",
        alertname="NoTransactionsFromRegion",
        namespace="test-003",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-06T12:00:51.333993Z"
    )
    generate_alert(
        description="More than 500 payments refunded in last 30 minutes.",
        alertname="RefundSpam",
        namespace="test-003",
        pod="paymentsvc-main-1",
        active_at_time="2024-02-05T20:46:16.334115Z"
    )
    # alerts for userauthsvc
    generate_alert(
        description="UserAuthService offline in namespace test-002.",
        alertname="UserAuthServiceDown",
        namespace="test-002",
        pod="userauthsvc-main-0",
        active_at_time="2024-02-06T03:58:51.852511Z"
    )
    generate_alert(
        description="More than 20000 users of America-North cannot login.",
        alertname="AuthServiceDownForRegion",
        namespace="test-003",
        pod="userauthsvc-main-0",
        active_at_time="2024-02-05T23:45:53.334234Z"
    )
    # alerts for messengersvc
    generate_alert(
        description="Last broadcast message promoted item for 0$",
        alertname="ZeroCostAlert",
        namespace="test-003",
        pod="messengersvc-main-0",
        active_at_time="2024-02-05T22:50:27.334353Z"
    )
    generate_alert(
        description="More than 5 broadcasts with the same message were sent in last 30 minutes.",
        alertname="MessageSpam",
        namespace="test-003",
        pod="messengersvc-main-1",
        active_at_time="2024-02-06T08:10:02.334472Z"
    )
    generate_alert(
        description="No messages received from region: America-North in last 60 minutes.",
        alertname="NoMessagesFromRegion",
        namespace="test-003",
        pod="messengersvc-main-2",
        active_at_time="2024-02-06T03:32:32.334591Z"
    )
    generate_alert(
        description="Messengerservice received messages below 30% of the average.",
        alertname="MessagesBelowAverage",
        namespace="test-004",
        pod="messengersvc-main-0",
        active_at_time="2024-02-05T21:37:21.336132Z"
    )
    # alerts for playerstatssvc
    generate_alert(
        description="Failed to load statistcs.",
        alertname="PlayerStatsMissing",
        namespace="test-002",
        pod="playerstatssvc-main-0",
        active_at_time="2024-02-06T10:33:38.333018Z"
    )
    generate_alert(
        description="Too many players affected by configuration change.",
        alertname="TooManyPlayersAffected",
        namespace="test-004",
        pod="playerstatssvc-main-0",
        active_at_time="2024-02-06T04:45:45.336485Z"
    )
    generate_alert(
        description="PlayerStatsService in namespace test-002 is down.",
        alertname="PlayerStatsServiceDown",
        namespace="test-002",
        pod="playerstatssvc-main-2",
        active_at_time="2024-02-06T02:42:57.333252Z"
    )
    generate_alert(
        description="Users checked stats below 30% of the average.",
        alertname="StatsCheckBelowAverage",
        namespace="test-002",
        pod="playerstatssvc-main-1",
        active_at_time="2024-02-06T06:18:17.333135Z"
    )


def init_data():
    # a pandas dataframe is initialized with the data from the csv file
    pass

if __name__ == "__main__":
    init_namespaces()
    pass
