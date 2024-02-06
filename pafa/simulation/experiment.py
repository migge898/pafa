import os
import pandas as pd

from pafa.simulation.functions import generate_alert, generate_namespace

def init_namespaces():
    # generate needed namespaces
    generate_namespace("test-001")
    generate_namespace("test-002")
    generate_namespace("test-003")
    generate_namespace("test-004")
    
def init_alerts():
    pairs = []
    pairs.append(("bug_s1", "BugTicketServiceOverloaded"))

    # alerts for bugticketsvc
    generate_alert(
        description="BugTicketservice in namespace test-001 is using 90% of CPU.",
        alertname="BugTicketServiceOverloaded2",
        namespace="test-001",
        pod="bugticketsvc-main-1",
        active_at_time="2024-02-06T11:09:02.330354Z"
    )#bug_l1
    pairs.append(("bug_l1", "BugTicketServiceOverloaded2"))

    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh",
        namespace="test-001",
        pod="bugticketsvc-main-2",
        active_at_time="2024-02-06T11:09:02.330354Z"
    )#bug_l2
    pairs.append(("bug_l2", "TicketCountHigh"))

    generate_alert(
        description="BugTicketservice in namespace test-002 is using 90% of CPU.",
        alertname="BugTicketServiceOverloaded3",
        namespace="test-002",
        pod="bugticketsvc-main-0",
        active_at_time="2024-02-06T09:40:06.331935Z"
    )#bug_s3
    pairs.append(("bug_s3", "BugTicketServiceOverloaded3"))

    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh2",
        namespace="test-002",
        pod="bugticketsvc-main-1",
        active_at_time="2024-02-06T08:40:06.331935Z"
    )#bug_s2
    pairs.append(("bug_s2", "TicketCountHigh2"))

    generate_alert(
        description="BugTicketservice has exceeded 300 open tickets.",
        alertname="TicketCountHigh3",
        namespace="test-003",
        pod="bugticketsvc-main-0",
        active_at_time="2024-02-06T08:40:06.331935Z"
    )#bug_s4
    pairs.append(("bug_s4", "TicketCountHigh3"))
    # alerts for paymentsvc
    generate_alert(
        description="PaymentService in namespace test-000 not available.",
        alertname="PaymentServiceDown",
        namespace="test-000",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-04T19:22:47.862156Z"
    )#pay_l1
    pairs.append(("pay_l1", "PaymentServiceDown"))

    generate_alert(
        description="PaymentService in namespace test-001 is using 70% of CPU.",
        alertname="PaymentServiceOverloaded",
        namespace="test-002",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-05T22:57:37.332298Z"
    )#pay_l2
    pairs.append(("pay_l2", "PaymentServiceOverloaded"))

    generate_alert(
        description="No transactions from America-North in last 30 minutes.",
        alertname="NoTransactionsFromRegion",
        namespace="test-003",
        pod="paymentsvc-main-0",
        active_at_time="2024-02-06T12:00:51.333993Z"
    )#pay_s1
    pairs.append(("pay_s1", "NoTransactionsFromRegion"))

    generate_alert(
        description="More than 500 payments refunded in last 30 minutes.",
        alertname="RefundSpam",
        namespace="test-003",
        pod="paymentsvc-main-1",
        active_at_time="2024-02-05T20:46:16.334115Z"
    )#pay_s2
    pairs.append(("pay_s2", "RefundSpam"))

    # alerts for userauthsvc
    generate_alert(
        description="UserAuthService offline in namespace test-002.",
        alertname="UserAuthServiceDown",
        namespace="test-002",
        pod="userauthsvc-main-0",
        active_at_time="2024-02-06T03:58:51.852511Z"
    )#auth_l2
    pairs.append(("auth_l2", "UserAuthServiceDown"))

    generate_alert(
        description="More than 20000 users of America-North cannot login.",
        alertname="AuthServiceDownForRegion",
        namespace="test-003",
        pod="userauthsvc-main-0",
        active_at_time="2024-02-05T23:45:53.334234Z"
    )#auth_l1
    pairs.append(("auth_l1", "AuthServiceDownForRegion"))

    # alerts for messengersvc
    generate_alert(
        description="Last broadcast message promoted item for 0$",
        alertname="ZeroCostAlert",
        namespace="test-003",
        pod="messengersvc-main-0",
        active_at_time="2024-02-05T22:50:27.334353Z"
    )#msg_l1
    pairs.append(("msg_l1", "ZeroCostAlert"))

    generate_alert(
        description="More than 5 broadcasts with the same message were sent in last 30 minutes.",
        alertname="MessageSpam",
        namespace="test-003",
        pod="messengersvc-main-1",
        active_at_time="2024-02-06T08:10:02.334472Z"
    )#msg_l2
    pairs.append(("msg_l2", "MessageSpam"))

    generate_alert(
        description="No messages received from region: America-North in last 60 minutes.",
        alertname="NoMessagesFromRegion",
        namespace="test-003",
        pod="messengersvc-main-2",
        active_at_time="2024-02-06T03:32:32.334591Z"
    )#msg_s2
    pairs.append(("msg_s2", "NoMessagesFromRegion"))

    generate_alert(
        description="Messengerservice received messages below 30% of the average.",
        alertname="MessagesBelowAverage",
        namespace="test-004",
        pod="messengersvc-main-0",
        active_at_time="2024-02-05T21:37:21.336132Z"
    )#msg_s1
    pairs.append(("msg_s1", "MessagesBelowAverage"))

    # alerts for playerstatssvc
    generate_alert(
        description="Failed to load some statistics.",
        alertname="PlayerStatsMissing",
        namespace="test-002",
        pod="playerstatssvc-main-0",
        active_at_time="2024-02-06T10:33:38.333018Z"
    )#play_s1
    pairs.append(("play_s1", "PlayerStatsMissing"))

    generate_alert(
        description="Too many players affected by configuration change.",
        alertname="TooManyPlayersAffected",
        namespace="test-004",
        pod="playerstatssvc-main-0",
        active_at_time="2024-02-06T04:45:45.336485Z"
    )#play_l2
    pairs.append(("play_l2", "TooManyPlayersAffected"))

    generate_alert(
        description="PlayerStatsService in namespace test-002 is down.",
        alertname="PlayerStatsServiceDown",
        namespace="test-002",
        pod="playerstatssvc-main-2",
        active_at_time="2024-02-06T02:42:57.333252Z"
    )#play_l1
    pairs.append(("play_l1", "PlayerStatsServiceDown"))

    generate_alert(
        description="Users checked stats below 30% of the average.",
        alertname="StatsCheckBelowAverage",
        namespace="test-002",
        pod="playerstatssvc-main-1",
        active_at_time="2024-02-06T06:18:17.333135Z"
    )#play_s2
    pairs.append(("play_s2", "StatsCheckBelowAverage"))

    return pairs

def m_print(text: str, max_length: int = 100):
    # print text to maximum length. If text is longer print word in new line
    text = text.split(" ")
    line = ""
    for word in text:
        if len(line) + len(word) > max_length:
            print(line)
            line = ""
        line += word + " "
    print(line)

def add_scores(dataframe: pd.DataFrame):
    dataframe["score_rc"] = 0
    dataframe["score_s"] = 0
    dataframe["score_e"] = 0
    
    for index, row in dataframe.iterrows():
         #clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"ID: {row['id']}")
        print(f"\nAlert: {row['alertname']}")
        print(f"\nRoot cause\n{row['root_cause_real']}")
        print(f"\nSolution\n{row['solution_real']}")
        m_print(f"\nPredicted root cause\n{row['root_cause_pred']}")
        m_print(f"\nPredicted solution\n{row['solution_pred']}")
        m_print(f"\nPredicted evidence\n{row['evidence_pred']}")
        print(f"\nError: {row['error']}")

        # get the 3 additional scores per user input and insert them into the dataframe
        score_rc = int(input("Score for root cause: "))
        score_s = int(input("Score for solution: "))
        score_e = int(input("Score for evidence: "))
        score = 0.5 * score_rc + 0.3 * score_s + 0.2 * score_e
        dataframe.loc[index, "score_rc"] = score_rc
        dataframe.loc[index, "score_s"] = score_s
        dataframe.loc[index, "score_e"] = score_e
        dataframe.loc[index, "score"] = score

    return dataframe

if __name__ == "__main__":
    # df_3 = pd.read_csv('experiment_data/gpt-3.5-turbo.csv')

    # df_3 = add_scores(df_3)
    # df_3.to_csv('experiment_data/scored_gpt-3.5-turbo.csv')
    df_4 = pd.read_csv('experiment_data/gpt-4-turbo-preview.csv')
    df_4 = add_scores(df_4)
    df_4.to_csv('experiment_data/scored_gpt-4-turbo-preview.csv')
