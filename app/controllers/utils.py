import typing

from app.models import Indicator, RekonData


def calculate_indicator_ratio_and_mark(
    indicator: Indicator, rekon_data_list: list[RekonData]
) -> typing.Union[float, int]:
    """
    Calculate the indicator ratio based on the specific indicator and its associated RekonData.
    Returns the calculated ratio and mark, or None if the calculation is not possible.
    """
    indicator_name = indicator.name.lower()

    def check_accounts_exist(accounts: set[str], rekon_data_list: list[RekonData]) -> list[str]:
        existing_accounts = set(data.account_number for data in rekon_data_list)
        return [account for account in accounts if account not in existing_accounts]

    def calculate_resource(accounts: set[str], rekon_data_list: list[RekonData]) -> int:
        return sum(data.amount for data in rekon_data_list if data.account_number in accounts)

    def validate_accounts(accounts_dict: dict[str, set[str]]) -> None:
        missing_accounts = []
        for key, accounts in accounts_dict.items():
            missing = check_accounts_exist(accounts, rekon_data_list)
            if missing:
                missing_accounts.extend(missing)
        if missing_accounts:
            raise AssertionError(
                f"Erreur: Les numéros de compte suivants sont manquants pour le calcul de l'indicateur '{indicator_name}': {', '.join(missing_accounts)}"
            )

    def calculate_ratio(accounts_dict: dict[str, set[str]], formula: callable) -> float:
        resources = {key: calculate_resource(accounts, rekon_data_list) for key, accounts in accounts_dict.items()}
        return formula(**resources)

    def get_mark(ratio: float, thresholds: list[tuple[float, int]]) -> int:
        for threshold, mark in thresholds:
            if ratio <= threshold:
                return mark
        return thresholds[-1][1]  # Return the last mark if ratio exceeds all thresholds

    indicator_configs = {
        "limitation des risques": {
            "accounts": {
                "a": {
                    "A12",
                    "A2A",
                    "A3A",
                    "A70",
                    "B2D",
                    "B2N",
                    "B30",
                    "B40",
                    "B70",
                    "C10",
                    "D1E",
                    "D1L",
                    "N1A+N1J+N3A+Q1A",
                },
                "b": {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"},
            },
            "formula": lambda a, b: (a / b) * 100,
            "thresholds": [(200, 5), (210, 4), (220, 3), (230, 2), (250, 1), (float("inf"), 0)],
        },
        "couverture des emplois à mlt par des ressources stables": {
            "accounts": {
                "a": {"L01", "F2A", "F3F", "F50", "G15", "G2A", "G30", "G35", "G60", "G70"},
                "b": {
                    "A2H",
                    "A2I",
                    "A2J",
                    "A3C",
                    "A70",
                    "B30",
                    "B40",
                    "B70",
                    "D1E",
                    "D1L",
                    "D10",
                    "D1S",
                    "D23",
                    "D30",
                    "D40",
                },
            },
            "formula": lambda a, b: (a / b) * 100,
            "thresholds": [(60, 0), (70, 1), (80, 2), (90, 3), (100, 4), (float("inf"), 5)],
        },
        "limitation des risques pris sur une seule signature": {
            "accounts": {
                "a": {"A1X"},
                "b": {"F1A", "F2A", "F3A", "F50", "G2A", "G10", "G15", "G35", "G60", "G70", "L01"},
                "c": {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"},
            },
            "formula": lambda a, b, c: (a / (b - c)) * 100,
            "thresholds": [(10, 5), (12, 4), (14, 3), (16, 2), (18, 1), (float("inf"), 0)],
        },
        "norme de liquidité": {
            "accounts": {
                "a": {
                    "A10",
                    "A12",
                    "A2J",
                    "A2A",
                    "A3B",
                    "B2D",
                    "B2N",
                    "B30",
                    "B40",
                    "C10",
                    "C30",
                    "C40",
                    "C56",
                    "A60",
                    "B65",
                    "C55",
                    "N1A+N1J+N2A+N2J",
                },
                "b": {
                    "F1A",
                    "F2A",
                    "F3E",
                    "F3F",
                    "F50",
                    "G10",
                    "G15",
                    "G2A",
                    "G30",
                    "G35",
                    "G60",
                    "G70",
                    "H10",
                    "H40",
                    "F60",
                    "G90",
                    "N1H+N1K+N2H+N2M",
                },
            },
            "formula": lambda a, b: (a / b) * 100,
            "thresholds": [(60, 0), (70, 1), (80, 2), (90, 3), (100, 4), (float("inf"), 5)],
        },
        "la réserve générale": {
            "accounts": {"a": {"L80"}, "b": {"L70"}},
            "formula": lambda a, b: a + b,
            "thresholds": [(15, 1), (15, 2), (float("inf"), 3)],
        },
        "la norme de capitalisation": {
            "accounts": {
                "a": {
                    "L10",
                    "L20",
                    "L27",
                    "L30",
                    "L35",
                    "L41",
                    "L45",
                    "L50",
                    "L55",
                    "L59",
                    "L60",
                    "L65",
                    "L70",
                    "L75",
                    "L80",
                },
                "b": {"B"},
                "c": {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"},
            },
            "formula": lambda a, b, c: ((a - c) / b) * 100,
            "thresholds": [(7, 0), (9, 1), (11, 2), (13, 3), (15, 4), (float("inf"), 5)],
        },
        "la limitation des prises de participation": {
            "accounts": {
                "a": {"D1E"},
                "b": {
                    "L10",
                    "L20",
                    "L27",
                    "L30",
                    "L35",
                    "L41",
                    "L45",
                    "L50",
                    "L55",
                    "L59",
                    "L60",
                    "L65",
                    "L70",
                    "L75",
                    "L80",
                },
                "c": {"L62", "E05", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"},
            },
            "formula": lambda a, b, c: (a / (b - c)) * 100,
            "thresholds": [(25, 5), (27, 4), (29, 3), (31, 2), (33, 1), (float("inf"), 0)],
        },
        "la limitation des prêts aux dirigeants, au personn ainsi qu'aux personnes liées": {
            "accounts": {
                "a": {"A"},
                "b": {
                    "L10",
                    "L20",
                    "L27",
                    "L30",
                    "L35",
                    "L41",
                    "L45",
                    "L50",
                    "L55",
                    "L59",
                    "L60",
                    "L65",
                    "L70",
                    "L75",
                    "L80",
                },
                "c": {"L62", "E05", "D24", "D24+D31+D41+D46", "L70", "L80", "A2X", "A3X"},
            },
            "formula": lambda a, b, c: (a / (b - c)) * 100,
            "thresholds": [(10, 5), (12, 4), (14, 3), (16, 2), (18, 1), (float("inf"), 0)],
        },
        "La limitation des opérations autres que l'épargne et le crédit": {
            "accounts": {
                "a": {"A"},
                "b": {"A12", "A30", "A70", "B2D", "B2N", "B30", "B40", "B70", "C10", "D1E", "D1L", "N1A+N1J+N3A+Q1A"},
            },
            "formula": lambda a, b: (a / b) * 100,
            "thresholds": [(5, 5), (6, 4), (7, 3), (8, 2), (10, 1), (float("inf"), 0)],
        },
        "Le financement des immobilisations et des participants": {
            "accounts": {
                "a": {"D24", "D25", "D31", "D36", "D41", "D45", "D46", "D47", "D1E"},
                "b": {
                    "L10",
                    "L20",
                    "L27",
                    "L30",
                    "L35",
                    "L41",
                    "L45",
                    "L50",
                    "L55",
                    "L59",
                    "L60",
                    "L65",
                    "L70",
                    "L75",
                    "L80",
                },
                "c": {"L62", "E05", "D24", "D31", "D41", "D46", "L70", "L80", "A2X", "A3X"},
            },
            "formula": lambda a, b, c: (a / (b - c)) * 100,
            "thresholds": [(100, 5), (105, 4), (110, 3), (115, 2), (120, 1), (float("inf"), 0)],
        },
    }

    if indicator_name in indicator_configs:
        config = indicator_configs[indicator_name]
        validate_accounts(config["accounts"])
        ratio = calculate_ratio(config["accounts"], config["formula"])
        mark = get_mark(ratio, config["thresholds"])
        return ratio, mark

    return None
