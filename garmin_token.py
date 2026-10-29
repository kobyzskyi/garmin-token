#!/usr/bin/env python3
"""garmin-token: a one-time sign-in to Garmin Connect (email, password, MFA code) that saves the DI OAuth2 tokens
to garmin.token.json. The sign-in itself is done by python-garminconnect; this program only writes di_token,
di_refresh_token and di_client_id to the file.

    garmin-token [path]          (default: garmin.token.json in the current directory)

The password goes only to Garmin; neither it nor the tokens are printed or sent anywhere else.
"""
import getpass
import json
import sys
from pathlib import Path

from garminconnect import Garmin

__version__ = "1.0.0"
KEYS = ("di_token", "di_refresh_token", "di_client_id")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help", "-V", "--version"):
        print(f"garmin-token {__version__}\n\n{__doc__}")
        return 0
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "garmin.token.json")
    print("Sign in to Garmin Connect. Your password and tokens go only to Garmin and to the file, nowhere else.")
    email = input("Garmin Connect email: ").strip()
    password = getpass.getpass("Password (hidden): ")
    garmin = Garmin(email, password, prompt_mfa=lambda: input("MFA code (from the email or the app): ").strip())
    try:
        garmin.login()
    except Exception as e:  # wrong password, MFA, Garmin blocking the request: say it plainly, without a traceback
        print(f"Sign-in failed: {e}", file=sys.stderr)
        return 1

    tokens = json.loads(garmin.client.dumps())
    if not tokens.get("di_refresh_token") or not tokens.get("di_client_id"):
        print("Signed in, but Garmin returned no DI refresh token (the cookie fallback was used). "
              "Download the latest garmin-token and try again.", file=sys.stderr)
        return 1

    out.write_text(json.dumps({k: tokens[k] for k in KEYS if k in tokens}), encoding="utf-8")
    print(f"\nDone: {out.resolve()}")
    print("Next: upload this file where your app asks for garmin.token.json.")
    print("Then delete it: the app refreshes the token itself, and a copy on disk is access to your Garmin account.")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        code = 130
    if getattr(sys, "frozen", False) and sys.platform == "win32":
        input("\nPress Enter to close this window...")  # started by a double click: keep the window open to read the result
    sys.exit(code)
