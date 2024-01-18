# env install
python --version
pip install poetry
poetry shell
poetry install

# aws config
- create iab user with programmatic type and `awsfullacces` policy and generate a key for it.
- in order to configure aws go to the terminal and type- `aws configure`