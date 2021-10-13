import argparse
import asyncio
import logging

from .clight import Clight


logging.basicConfig(level=logging.WARN)

logger = logging.getLogger(__package__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    backlight = subparsers.add_parser("backlight")
    backlight_sub = backlight.add_subparsers(dest="subcommand", required=True)

    backlight_sub.add_parser("get")

    backlight_set = backlight_sub.add_parser("set")
    backlight_set.add_argument("value", type=int)

    backlight_increase = backlight_sub.add_parser("increase")
    backlight_increase.add_argument("value", type=int)

    backlight_decrease = backlight_sub.add_parser("decrease")
    backlight_decrease.add_argument("value", type=int)

    return parser.parse_args()


async def async_main() -> None:
    args = parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug(args)

    clight = Clight()

    if args.command == "backlight" and args.subcommand == "get":
        b = await clight.get_backlight()
        print(b)
    elif args.command == "backlight" and args.subcommand == "set":
        await clight.set_backlight(args.value)
    elif args.command == "backlight" and args.subcommand == "increase":
        await clight.increase_backlight(args.value)
    elif args.command == "backlight" and args.subcommand == "decrease":
        await clight.decrease_backlight(args.value)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
