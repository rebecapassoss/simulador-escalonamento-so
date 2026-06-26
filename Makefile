ALG ?= ALL
INPUT ?= inputs/caso1.json

build:
	docker compose build

up:
	docker compose up --build

run:
	docker compose run --rm simulador --alg $(ALG) --input $(INPUT)

all-caso1:
	docker compose run --rm simulador --alg ALL --input inputs/caso1.json

all-preempcao:
	docker compose run --rm simulador --alg ALL --input inputs/caso_preempcao.json

all-ocioso:
	docker compose run --rm simulador --alg ALL --input inputs/caso_ocioso.json

all-deadline:
	docker compose run --rm simulador --alg ALL --input inputs/caso_deadline.json

all-sobrecarga:
	docker compose run --rm simulador --alg ALL --input inputs/caso_sobrecarga.json

clean:
	find outputs -type f \( -name "*.json" -o -name "*.png" -o -name "*.csv" -o -name "*.log" \) -delete

logs:
	cat outputs/logs/simulator.log

status:
	tree outputs

shell:
	docker compose run --rm simulador bash

test-cases: all-caso1 all-preempcao all-ocioso all-deadline all-sobrecarga

front:
	docker compose up --build streamlit

front-down:
	docker compose down