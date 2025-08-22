import sys
import time
import logging
import asyncio
from api_solver import create_app


class CustomLogger(logging.Logger):
    COLORS = {
        'DEBUG': '\033[35m',    # Magenta
        'INFO': '\033[34m',     # Blue
        'SUCCESS': '\033[32m',  # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
    }
    RESET = '\033[0m'

    def format_message(self, level, message):
        timestamp = time.strftime('%H:%M:%S')
        return f"[{timestamp}] [{self.COLORS.get(level, '')}{level}{self.RESET}] -> {message}"

    def debug(self, message, *args, **kwargs):
        super().debug(self.format_message('DEBUG', message), *args, **kwargs)

    def info(self, message, *args, **kwargs):
        super().info(self.format_message('INFO', message), *args, **kwargs)

    def success(self, message, *args, **kwargs):
        super().info(self.format_message('SUCCESS', message), *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        super().warning(self.format_message('WARNING', message), *args, **kwargs)

    def error(self, message, *args, **kwargs):
        super().error(self.format_message('ERROR', message), *args, **kwargs)


logging.setLoggerClass(CustomLogger)
logger = logging.getLogger("TurnstileAPI")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class TurnstileAPI:
    async def run_api_server(self, debug=False, headless=False, useragent=None, browser_type="chromium", thread=1):
        """Run the API server automatically."""
        logger.info("Starting API server on http://localhost:5000")
        logger.info("API documentation available at http://localhost:5000/")

        try:
            app = create_app(debug=debug, headless=headless, useragent=useragent, browser_type=browser_type, thread=thread, proxy_support=False)
            import hypercorn.asyncio
            from hypercorn.config import Config

            config = Config()
            config.bind = ["0.0.0.0:7860"]
            await hypercorn.asyncio.serve(app, config)
        except Exception as e:
            logger.error(f"API server failed to start: {str(e)}")

    async def main(self):
        """Main entrypoint for direct API usage."""
        logger.info("Turnstile: Starting in API mode")
        await self.run_api_server()


if __name__ == "__main__":
    tester = TurnstileAPI()
    asyncio.run(tester.main())
