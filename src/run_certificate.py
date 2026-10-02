import json
import sys

from certificate_service import InfraiPdfClient, Participant, issue_certificate


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "Amina Yusuf"
    participant = Participant(name=name, program="Community Food Bank", completed_hours=24)
    result = issue_certificate(participant, InfraiPdfClient())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

