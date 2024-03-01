# Hyperdiv Docs

This repo contains the Hyperdiv documentation app, which is written in Hyperdiv.

![Docs Gif](https://github.com/hyperdiv/hyperdiv-docs/assets/5980501/34a9b312-ae0c-4af2-9889-42b52db63439)

# Opening the Documentation App

The documentation app ships with Hyperdiv when installing Hyperdiv from PyPI. After installing Hyperdiv, run this command to open the docs app in a browser tab:
```
hyperdiv docs
```

# For Developers

After cloning the Hyperdiv repo and installing its dependencies, you can simply clone this repo and run its `start.py` script within Hyperdiv's Poetry virtualenv:
```sh
cd hyperdiv
# Install Python dependencies
poetry install
# Install frontend dependencies
cd frontend
npm install
npm run build
cd ..
# Enter the virtualenv
poetry shell
# Run the docs app in the virtualenv
cd ../hyperdiv-docs
python start.py
```
