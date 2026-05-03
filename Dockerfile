FROM python:3.14-alpine
WORKDIR /coffee_shop
RUN pip install uv --no-cache-dir
COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --no-cache
COPY ./ ./
CMD [ "uv", "run", "python", "-m", "coffee_shop.main" ]