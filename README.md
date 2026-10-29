# garmin-token

A small program that signs in to Garmin Connect once (email, password, MFA code) and saves the tokens to
`garmin.token.json`. You then upload that file to an app that reads your Garmin data on your behalf — for example the
Garmin section of the profile page in [fitness](https://github.com/kobyzskyi/fitness).

- Your password goes only to Garmin. Neither the password nor the tokens are printed or sent anywhere else.
- The sign-in is done by [python-garminconnect](https://github.com/cyberjunky/python-garminconnect); this program only
  saves three values from it: `di_token`, `di_refresh_token`, `di_client_id`.
- The whole program is one file, [`garmin_token.py`](garmin_token.py). The binaries are built by GitHub Actions from
  this repository ([build.yml](.github/workflows/build.yml)); every release comes with SHA-256 checksums.

## Download

From the [latest release](https://github.com/kobyzskyi/garmin-token/releases/latest), take the file for your system:

| System | File |
|---|---|
| Windows | `garmin-token-windows-x64.exe` |
| macOS (Apple Silicon) | `garmin-token-macos-arm64` |
| macOS (Intel) | `garmin-token-macos-x64` |
| Linux | `garmin-token-linux-x64` |

## Usage

1. Download the file and run it.
   - **Windows:** double-click it. If you see "Windows protected your PC", choose "More info" → "Run anyway"
     (the program is not code-signed).
   - **macOS:** in Terminal run `chmod +x ~/Downloads/garmin-token-macos-*` and
     `xattr -d com.apple.quarantine ~/Downloads/garmin-token-macos-*`, then start the file from Terminal.
   - **Linux:** `chmod +x garmin-token-linux-x64 && ./garmin-token-linux-x64`.
2. Enter your Garmin Connect email and password, then the MFA code if MFA is on.
3. `garmin.token.json` appears in the current directory. Upload it to your app.
4. **Delete the file.** The app refreshes the token by itself; a copy on disk is access to your Garmin account.

If the app later says the Garmin token has expired (for example after you changed your Garmin password), repeat these steps.

To verify a download (optional), compare `sha256sum <file>` (Windows: `certutil -hashfile <file> SHA256`) with
`SHA256SUMS.txt` in the release.

## Without the binaries

With Python 3.10+:

```
pip install -r requirements.txt
python garmin_token.py
```

## Releasing

Bump `__version__` in `garmin_token.py` (and the `garminconnect` version in `requirements.txt` if needed), then push a
tag: `git tag v1.0.1 && git push origin v1.0.1`. GitHub Actions builds the binaries and publishes the release.
