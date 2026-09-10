"""
Planner de conteúdo SINDIPI 2027.

Base de dados das publicações extraídas do calendário impresso 2026 (datas
comemorativas, feriados, aniversários das cidades da base e períodos de
defeso/safra, já adaptados para os dias da semana de 2027) mais as datas
comemorativas complementares (Dia do Médico Veterinário, Dia Mundial dos
Oceanos etc.) incluídas depois para ampliar as pautas de posts e stories.

É a mesma base de dados usada pelo planner publicado como Artifact — este
arquivo serve como cópia local/editável em Python, com exportação para CSV
e JSON.

Uso:
    python planner_sindipi_2027.py
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

# id -> também usado como nome do registro; quando duas publicações caem no
# mesmo dia, o segundo id recebe o sufixo "-2".
POSTS: list[dict] = [
    {"id": "2027-01-01", "date": "2027-01-01", "title": "Confraternização Mundial", "category": "feriado", "suggestion": "Card de feriado — Feliz Ano Novo, sem expediente.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-01-26", "date": "2027-01-26", "title": "Fechamento do defeso do camarão (começa 28/01)", "category": "defeso", "suggestion": "Aviso: o defeso do camarão começa dia 28/01 — reforce a data para a frota se preparar.", "status": "A planejar", "scheduledAt": "", "notes": "Camarão-rosa, sete-barbas, branco, santana, vermelho e barba-ruça. Defeso vai até 30/04."},
    {"id": "2027-02-09", "date": "2027-02-09", "title": "Carnaval", "category": "feriado", "suggestion": "Comunicado de recesso de Carnaval.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-02-10", "date": "2027-02-10", "title": "Quarta-feira de Cinzas", "category": "comemorativa", "suggestion": "Opcional — mensagem de encerramento do Carnaval.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-02-25", "date": "2027-02-25", "title": "Fim do defeso da sardinha-verdadeira (Cerco)", "category": "defeso", "suggestion": "Anuncie o fim do defeso — a safra reabre em 1º de março.", "status": "A planejar", "scheduledAt": "", "notes": "Defeso em vigor desde 01/10/2026."},
    {"id": "2027-03-01", "date": "2027-03-01", "title": "Início da safra da sardinha-verdadeira (Cerco)", "category": "safra", "suggestion": "Começou a safra da sardinha-verdadeira (cerco)!", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-08", "date": "2027-03-08", "title": "Dia Internacional da Mulher", "category": "comemorativa", "suggestion": "Post ou story homenageando as mulheres da pesca e da comunidade pesqueira.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-15", "date": "2027-03-15", "title": "Aniversário de Bombinhas", "category": "comemorativa", "suggestion": "Post de parabéns ao município de Bombinhas.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-20", "date": "2027-03-20", "title": "Início do Outono", "category": "comemorativa", "suggestion": "Post sazonal sobre a chegada do outono.", "status": "A planejar", "scheduledAt": "", "notes": "Data aproximada do equinócio — conferir horário oficial."},
    {"id": "2027-03-22", "date": "2027-03-22", "title": "Dia Mundial da Água", "category": "comemorativa", "suggestion": "Story educativo sobre a importância da água e dos recursos hídricos para a pesca.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-26", "date": "2027-03-26", "title": "Paixão de Cristo (Sexta-feira Santa)", "category": "feriado", "suggestion": "Card de feriado religioso.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-28", "date": "2027-03-28", "title": "Páscoa", "category": "feriado", "suggestion": "Mensagem de Páscoa para a categoria.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-03-29", "date": "2027-03-29", "title": "Fim do defeso da Anchova", "category": "defeso", "suggestion": "O defeso da anchova termina dia 31/03 — safra reabre em 01/04.", "status": "A planejar", "scheduledAt": "", "notes": "Defeso em vigor desde 01/12/2026."},
    {"id": "2027-04-01", "date": "2027-04-01", "title": "Início da safra da Anchova", "category": "safra", "suggestion": "Começou a safra da anchova!", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-04-21", "date": "2027-04-21", "title": "Tiradentes", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-04-22", "date": "2027-04-22", "title": "Descobrimento do Brasil", "category": "comemorativa", "suggestion": "Post histórico/educativo.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-04-28", "date": "2027-04-28", "title": "SINDIPI comemora 47 anos", "category": "institucional", "suggestion": "Publicação institucional: SINDIPI completa 47 anos.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-04-28-2", "date": "2027-04-28", "title": "Dia Mundial da Segurança e Saúde no Trabalho", "category": "institucional", "suggestion": "Post sobre segurança no trabalho a bordo — EPIs e prevenção de acidentes na pesca.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-04-29", "date": "2027-04-29", "title": "Fim do defeso do Camarão", "category": "defeso", "suggestion": "O defeso do camarão termina dia 30/04 — safra reabre em 01/05.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-05-01", "date": "2027-05-01", "title": "Dia do Trabalhador", "category": "feriado", "suggestion": "Card de feriado — Dia do Trabalhador.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-05-01-2", "date": "2027-05-01", "title": "Início da safra do Camarão", "category": "safra", "suggestion": "Começou a safra do camarão!", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-05-09", "date": "2027-05-09", "title": "Dia das Mães", "category": "comemorativa", "suggestion": "Post ou story especial para as mães da categoria.", "status": "A planejar", "scheduledAt": "", "notes": "2º domingo de maio."},
    {"id": "2027-05-13", "date": "2027-05-13", "title": "Aviso: paralisação da frota de Emalhe (começa 15/05)", "category": "defeso", "suggestion": "Aviso: a paralisação da frota de emalhe começa dia 15/05.", "status": "A planejar", "scheduledAt": "", "notes": "Vai até 15/06."},
    {"id": "2027-05-27", "date": "2027-05-27", "title": "Corpus Christi", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-01", "date": "2027-06-01", "title": "Início da safra da Tainha", "category": "safra", "suggestion": "Começou a safra da tainha! — pauta de destaque do mês.", "status": "A planejar", "scheduledAt": "", "notes": "Temporada oficial vai até 31/07."},
    {"id": "2027-06-05", "date": "2027-06-05", "title": "Dia Mundial do Meio Ambiente", "category": "comemorativa", "suggestion": "Post sobre preservação ambiental e pesca sustentável.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-08", "date": "2027-06-08", "title": "Dia Mundial dos Oceanos", "category": "comemorativa", "suggestion": "Pauta de destaque: conscientização sobre a saúde dos oceanos e a pesca sustentável.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-13", "date": "2027-06-13", "title": "Fim da paralisação da frota de Emalhe", "category": "defeso", "suggestion": "Retomada das atividades da frota de emalhe em 16/06.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-15", "date": "2027-06-15", "title": "Aniversário de Itajaí", "category": "comemorativa", "suggestion": "Post de parabéns ao município de Itajaí.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-15-2", "date": "2027-06-15", "title": "Início do defeso da Sardinha-verdadeira (isca-viva)", "category": "defeso", "suggestion": "Aviso: começa o defeso da sardinha-verdadeira como isca-viva, até 31/07.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-06-21", "date": "2027-06-21", "title": "Início do Inverno", "category": "comemorativa", "suggestion": "Post sazonal sobre o início do inverno.", "status": "A planejar", "scheduledAt": "", "notes": "Data aproximada do solstício."},
    {"id": "2027-06-29", "date": "2027-06-29", "title": "Dia do Pescador", "category": "comemorativa", "suggestion": "Homenagem à categoria — pauta especial do Dia do Pescador.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-07-19", "date": "2027-07-19", "title": "Aniversário de Penha", "category": "comemorativa", "suggestion": "Post de parabéns ao município de Penha.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-07-20", "date": "2027-07-20", "title": "Aniversário de Balneário Camboriú", "category": "comemorativa", "suggestion": "Post de parabéns a Balneário Camboriú.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-07-29", "date": "2027-07-29", "title": "Reta final da safra da Tainha", "category": "safra", "suggestion": "Últimos dias da safra da tainha 2027 — encerra dia 31/07.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-07-30", "date": "2027-07-30", "title": "Fim do defeso da Sardinha-verdadeira (isca-viva)", "category": "defeso", "suggestion": "Liberada a partir de 01/08 a captura da sardinha-verdadeira como isca-viva.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-08-01", "date": "2027-08-01", "title": "Início do defeso: Badejo-amarelo, Sirigado, Garoupa-de-São Tomé e Caranha", "category": "defeso", "suggestion": "Aviso: começa o defeso do badejo-amarelo, sirigado, garoupa-de-são-tomé e caranha, até 30/09.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-08-01-2", "date": "2027-08-01", "title": "Início da safra da Sardinha-verdadeira (isca-viva)", "category": "safra", "suggestion": "Liberada a captura da sardinha-verdadeira como isca-viva.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-08-04", "date": "2027-08-04", "title": "Aniversário de Brusque", "category": "comemorativa", "suggestion": "Post de parabéns a Brusque.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-08-08", "date": "2027-08-08", "title": "Dia dos Pais", "category": "comemorativa", "suggestion": "Post ou story especial para os pais da categoria.", "status": "A planejar", "scheduledAt": "", "notes": "2º domingo de agosto."},
    {"id": "2027-08-26", "date": "2027-08-26", "title": "Aniversário de Navegantes", "category": "comemorativa", "suggestion": "Post de parabéns a Navegantes.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-09-01", "date": "2027-09-01", "title": "Início do defeso: Cherne-verdadeiro e Peixe-batata", "category": "defeso", "suggestion": "Aviso: começa o defeso do cherne-verdadeiro e peixe-batata, até 31/10.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-09-07", "date": "2027-09-07", "title": "Independência do Brasil", "category": "feriado", "suggestion": "Card de feriado cívico.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-09-09", "date": "2027-09-09", "title": "Dia do Médico Veterinário", "category": "comemorativa", "suggestion": "Story sobre cuidado sanitário do pescado e parceria com médicos veterinários.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-09-22", "date": "2027-09-22", "title": "Início da Primavera", "category": "comemorativa", "suggestion": "Post sazonal sobre a primavera.", "status": "A planejar", "scheduledAt": "", "notes": "Data aproximada do equinócio."},
    {"id": "2027-09-28", "date": "2027-09-28", "title": "Fim do defeso: Badejo-amarelo, Sirigado, Garoupa-de-São Tomé e Caranha", "category": "defeso", "suggestion": "Anuncie o fim do defeso — safra reabre em 01/10.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-01", "date": "2027-10-01", "title": "Novo ciclo do defeso da Sardinha-verdadeira (Cerco)", "category": "defeso", "suggestion": "Aviso: novo defeso da sardinha-verdadeira (cerco) até fevereiro/2028.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-01-2", "date": "2027-10-01", "title": "Início da safra: Badejo-amarelo, Sirigado, Garoupa-de-São Tomé e Caranha", "category": "safra", "suggestion": "Reaberta a captura do badejo-amarelo, sirigado, garoupa-de-são-tomé e caranha.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-04", "date": "2027-10-04", "title": "Dia Mundial dos Animais", "category": "comemorativa", "suggestion": "Post sobre bem-estar animal e fauna marinha.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-12", "date": "2027-10-12", "title": "Nossa Senhora Aparecida", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-13", "date": "2027-10-13", "title": "Aniversário de Porto Belo", "category": "comemorativa", "suggestion": "Post de parabéns a Porto Belo.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-16", "date": "2027-10-16", "title": "Dia Mundial da Alimentação", "category": "comemorativa", "suggestion": "Post sobre o pescado como fonte de alimento saudável e sustentável.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-10-29", "date": "2027-10-29", "title": "Fim do defeso: Cherne-verdadeiro e Peixe-batata", "category": "defeso", "suggestion": "Anuncie o fim do defeso — safra reabre em 01/11.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-11-01", "date": "2027-11-01", "title": "Início da safra do Cherne-verdadeiro e Peixe-batata", "category": "safra", "suggestion": "Começou a safra do cherne-verdadeiro e peixe-batata!", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-11-02", "date": "2027-11-02", "title": "Finados", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-11-15", "date": "2027-11-15", "title": "Proclamação da República", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-11-20", "date": "2027-11-20", "title": "Dia Nacional de Zumbi e da Consciência Negra", "category": "feriado", "suggestion": "Post de reflexão sobre o Dia da Consciência Negra.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-01", "date": "2027-12-01", "title": "Novo ciclo do defeso da Anchova", "category": "defeso", "suggestion": "Aviso: novo defeso da anchova até março/2028.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-07", "date": "2027-12-07", "title": "Aniversário de Barra Velha", "category": "comemorativa", "suggestion": "Post de parabéns a Barra Velha.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-14", "date": "2027-12-14", "title": "Aniversário de Piçarras", "category": "comemorativa", "suggestion": "Post de parabéns a Piçarras.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-21", "date": "2027-12-21", "title": "Início do Verão", "category": "comemorativa", "suggestion": "Post sazonal sobre o início do verão.", "status": "A planejar", "scheduledAt": "", "notes": "Data aproximada do solstício."},
    {"id": "2027-12-24", "date": "2027-12-24", "title": "Véspera de Natal", "category": "institucional", "suggestion": "Mensagem de Natal para a categoria.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-25", "date": "2027-12-25", "title": "Natal", "category": "feriado", "suggestion": "Card de feriado.", "status": "A planejar", "scheduledAt": "", "notes": ""},
    {"id": "2027-12-31", "date": "2027-12-31", "title": "Véspera de Ano Novo", "category": "institucional", "suggestion": "Mensagem de Ano Novo para a categoria.", "status": "A planejar", "scheduledAt": "", "notes": ""},
]

CATEGORY_LABELS = {
    "feriado": "Feriado",
    "comemorativa": "Comemorativa",
    "defeso": "Defeso",
    "safra": "Safra",
    "institucional": "Institucional",
    "outro": "Outro",
}

# date.weekday(): Segunda=0 ... Domingo=6
_WEEKDAYS_PT = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]


def weekday_label(date_str: str) -> str:
    """Nome do dia da semana (em português) para uma data 'YYYY-MM-DD'."""
    y, m, d = (int(part) for part in date_str.split("-"))
    return _WEEKDAYS_PT[date(y, m, d).weekday()]


def sorted_posts() -> list[dict]:
    return sorted(POSTS, key=lambda p: (p["date"], p["id"]))


def export_csv(path: str | Path = "planner-sindipi-2027.csv") -> Path:
    """Exporta o planner para CSV (mesmas colunas do botão 'Baixar CSV' do planner online)."""
    path = Path(path)
    header = ["Data", "Dia da semana", "Categoria", "Tema", "Sugestão de legenda", "Status", "Agendar para", "Observações"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for p in sorted_posts():
            writer.writerow([
                p["date"],
                weekday_label(p["date"]),
                CATEGORY_LABELS.get(p["category"], p["category"]),
                p["title"],
                p["suggestion"],
                p["status"],
                p["scheduledAt"],
                p["notes"],
            ])
    return path


def export_json(path: str | Path = "planner-sindipi-2027.json") -> Path:
    """Exporta o planner completo (todos os campos) para JSON."""
    path = Path(path)
    path.write_text(json.dumps(sorted_posts(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def print_summary() -> None:
    by_category = Counter(p["category"] for p in POSTS)
    by_status = Counter(p["status"] for p in POSTS)
    print(f"Total de publicações: {len(POSTS)}")
    print("\nPor categoria:")
    for cat, label in CATEGORY_LABELS.items():
        if by_category.get(cat):
            print(f"  {label}: {by_category[cat]}")
    print("\nPor status:")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    csv_path = export_csv()
    json_path = export_json()
    print_summary()
    print(f"\nCSV salvo em:  {csv_path.resolve()}")
    print(f"JSON salvo em: {json_path.resolve()}")
