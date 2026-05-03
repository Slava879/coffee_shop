import uvicorn

from coffee_shop.core.setup import setup_app

if __name__ == "__main__":
    app = setup_app()
    uvicorn.run(app, host='0.0.0.0')
