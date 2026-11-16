import argparse
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


WEBSITES = [
    "https://www.python.org",
    "https://github.com",
    "https://example.com",
]


def check_website(url, timeout):
    start = perf_counter()

    try:
        with urlopen(url, timeout=timeout) as response:
            status = "UP"
            code = response.status
            error = ""
    except HTTPError as exc:
        status = "DOWN"
        code = exc.code
        error = str(exc.reason)
    except (URLError, TimeoutError) as exc:
        status = "DOWN"
        code = "-"
        error = str(exc)

    elapsed_ms = (perf_counter() - start) * 1000
    print(f"{url:<25} {status:<5} {code!s:>4} {elapsed_ms:>8.0f} ms  {error}")


def main():
    parser = argparse.ArgumentParser(description="Check the status of three websites.")
    parser.add_argument("--timeout", type=float, default=5, help="Request timeout in seconds")
    args = parser.parse_args()

    if not 0 < args.timeout < float("inf"):
        parser.error("--timeout must be a finite number greater than zero")

    for website in WEBSITES:
        check_website(website, args.timeout)


if __name__ == "__main__":
    main()
