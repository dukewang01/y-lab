"""y-risk: 风险矩阵引擎"""
import json
from enum import IntEnum


class Likelihood(IntEnum):
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class Severity(IntEnum):
    MINOR = 1
    MODERATE = 2
    SERIOUS = 3
    FATAL = 4


LEVEL_NAMES = {1: "低", 2: "低", 3: "中", 4: "中",
               5: "高", 6: "高", 7: "高", 8: "极高",
               9: "极高", 10: "极高"}

RISK_MATRIX = {
    (1,1):1, (1,2):1, (1,3):2, (1,4):3,
    (2,1):1, (2,2):2, (2,3):3, (2,4):4,
    (3,1):2, (3,2):3, (3,3):5, (3,4):6,
    (4,1):3, (4,2):4, (4,3):6, (4,4):8,
    (5,1):3, (5,2):5, (5,3):7, (5,4):10,
}


class RiskItem:
    def __init__(self, name, category, likelihood, severity, owner=""):
        self.name = name
        self.category = category
        self.likelihood = likelihood
        self.severity = severity
        self.owner = owner
        self.score = RISK_MATRIX.get((likelihood, severity), 5)
        self.level = LEVEL_NAMES.get(self.score, "高")
        self.status = "open"

    def __repr__(self):
        return f"[{self.level}] {self.name} ({self.category})"


class RiskManager:
    def __init__(self):
        self.risks = []

    def register(self, name, category, likelihood, severity, owner=""):
        item = RiskItem(name, category, likelihood, severity, owner)
        self.risks.append(item)
        return item

    def assess(self):
        self.risks.sort(key=lambda r: -r.score)
        return {
            "total": len(self.risks),
            "by_level": {
                "高": len([r for r in self.risks if r.level in ("高","极高")]),
                "中": len([r for r in self.risks if r.level == "中"]),
                "低": len([r for r in self.risks if r.level == "低"]),
            },
            "high_risks": [r for r in self.risks if r.level in ("高","极高")],
        }
