PYTHON := python3
VENV_NAME := .soiz
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
REQUIREMENTS := requirements.txt
MAIN_FILE := main.py
env: $(VENV_NAME)

$(VENV_NAME):
	@echo "Tạo môi trường ảo..."
	@python3 -m venv $(VENV_NAME)
	@. $(VENV_ACTIVATE) && pip install --upgrade pip

install: env
	@echo "Cài đặt các gói từ requirements.txt..."
	@. $(VENV_ACTIVATE) && pip install -r $(REQUIREMENTS)

run: env $(MAIN_FILE)
	@echo "Chạy chương trình..."
	@. $(VENV_ACTIVATE) && $(PYTHON) $(MAIN_FILE)

freeze: env
	@echo "Đóng băng các gói vào requirements.txt..."
	@. $(VENV_ACTIVATE) && pip freeze > $(REQUIREMENTS)