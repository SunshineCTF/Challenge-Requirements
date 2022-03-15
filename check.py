import glob
import os
import sys


class Checker:
    def __init__(self, rules, path):
        self.rules = rules
        self.path = path

    def evaluate(self):
        """Evaluates a set of rules as defined at initialization

        Returns:
        {
            "challenge": "path to the challenge",
            "rule_results": [
                {
                    "rule": _see rule in main_,
                    "result": True if rule passed, False otherwise
                }
            ]
        }
        """
        res = {"challenge": self.path, "rule_results": []}
        for rule in self.rules:
            res["rule_results"].append(self.__evaluate_rule__(rule))
        return res

    def __evaluate_rule__(self, rule):
        """
        Evaluates a rule against the challenge

        Returns:
        {
            "rule": _see rule in main_,
            "result": True if the rule passed, False otherwise
        }
        """
        filename = rule.get("file", None)
        if not filename:
            # Going to assume if no file is returned then this rule is fine.
            return {"rule": rule, "result": True}

        # Determine if file exists
        optional = rule.get("optional", False)
        exists = os.path.exists(f"{self.path}/{filename}")
        if not optional and not exists:
            return {"rule": rule, "result": False}

        # todo: See if there's a good markdown parser and put it here

        return {"rule": rule, "result": True}


def main():
    message = """
    SUNSHINECTF Requirements Checker
    --------------------------------
    This requirements checker validates that your challenges have all
    of the requirements for a full SunshineCTF Challenge
    """
    print(message)
    rules = [
        {
            "name": "Challenge Must Have a flag.txt",
            "file": "flag.txt",
            "description": "Contains the challenge's flag",
        },
        {
            "name": "Challenge must have a description.md",
            "file": "description.md",
            "description": "Contains the flavortext description to be presented to challengers",
            "markdown": True,
        },
        {
            "name": "Challenge must have a README.md",
            "description": "Contains detailed information about how to build and deploy the challenge",
            "markdown": True,
        },
        {
            "name": "Challenge must have a solve.sh script",
            "description": "Contains a script that can validate that the challenge works as intended",
            "optional": True,
        },
    ]

    challenges = glob.glob("./*/*")
    chal_res = []

    for challenge in challenges:
        chkr = Checker(rules, challenge)
        chal_res.append(chkr.evaluate())

    failures = False
    for res in chal_res:
        print(f"Results for challenge {res['challenge']}")
        for rule in res["rule_results"]:
            if rule["result"]:
                print(f" ✅ {rule['rule']['name']}")
            else:
                print(f" ❌ {rule['rule']['name']}: {rule['rule']['description']}")
                failures = True

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
