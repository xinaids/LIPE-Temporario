#!/usr/bin/env python
# coding: utf-8
"""
Analisador do execucoes.log do LIPE.

Uso (com a venv ativa):
    python analisar_log.py                 -> analisa todos os .log da pasta atual
    python analisar_log.py aluno1.log      -> analisa um arquivo
    python analisar_log.py joao.log ana.log maria.log   -> varios alunos

Fluxo sugerido para o teste do Edimar:
    1. Teste um aluno no jogo.
    2. Renomeie o execucoes.log para algo como "pedro_pequeno.log".
       (no PowerShell:  Rename-Item execucoes.log pedro_pequeno.log )
    3. Teste o proximo aluno (um novo execucoes.log e criado).
    4. No fim, rode este script passando todos os arquivos.
"""

import sys
import glob
import re
from collections import defaultdict

# nomes dos 4 movimentos, identificados pela parte SEM acento
# (o log as vezes grava "M o" no lugar de "Mao", entao casamos pelo trecho seguro)
MOV_KEYS = {
    "esquerda": "Mão Esquerda",
    "direita": "Mão Direita",
    "pule": "Pule",
    "agache": "Agache",
}

LINE_RE = re.compile(
    r"Movimento Esperado:\s*(.*?),\s*Retornado:\s*(.*?),.*?body_unit:\s*([-\d.eE]+)"
)

# captura o nome do jogador, quando presente ("Jogador: Fulano,")
PLAYER_RE = re.compile(r"Jogador:\s*(.*?),")


def normaliza_mov(texto: str) -> str:
    t = texto.strip().lower()
    for chave, nome in MOV_KEYS.items():
        if chave in t:
            return nome
    return "DESCONHECIDO(" + texto.strip() + ")"


def ler_arquivo(caminho: str):
    # tenta utf-8; se falhar por causa do acento mal gravado, usa latin-1
    for enc in ("utf-8", "latin-1"):
        try:
            with open(caminho, "r", encoding=enc) as f:
                return f.readlines()
        except (UnicodeDecodeError, FileNotFoundError) as e:
            if isinstance(e, FileNotFoundError):
                print(f"  [erro] arquivo nao encontrado: {caminho}")
                return []
    return []


def analisa_grupo(nome_grupo: str, linhas_match):
    """Recebe uma lista de tuplas (esperado, retornado, body_unit) e imprime o relatorio."""
    tabela = defaultdict(lambda: defaultdict(int))
    body_units = []
    total = 0

    for esperado, retornado, bu in linhas_match:
        tabela[esperado][retornado] += 1
        total += 1
        if bu is not None:
            body_units.append(bu)

    print("=" * 60)
    print(f"JOGADOR: {nome_grupo}")
    print("=" * 60)

    if total == 0:
        print("  Nenhuma tentativa registrada.\n")
        return None

    print(f"Tentativas registradas (frames): {total}")
    if body_units:
        print(
            f"Calibracao body_unit: min {min(body_units):.4f}  "
            f"max {max(body_units):.4f}  "
            f"(quanto MENOR, mais perto/curvado na calibracao)"
        )
    print()

    acertos_total = 0
    pedidos_total = 0

    print("Acerto por movimento PEDIDO:")
    for esperado in sorted(tabela.keys()):
        retornos = tabela[esperado]
        pedidos = sum(retornos.values())
        acertos = retornos.get(esperado, 0)
        pct = 100 * acertos / pedidos if pedidos else 0
        pedidos_total += pedidos
        acertos_total += acertos
        print(f"  {esperado:<14}: {acertos:>4}/{pedidos:<4} ({pct:5.1f}%)")
    print()

    confusoes = []
    for esperado, retornos in tabela.items():
        for retornado, qtd in retornos.items():
            if retornado != esperado:
                confusoes.append((qtd, esperado, retornado))
    confusoes.sort(reverse=True)

    if confusoes:
        print("Quando ERROU, o que detectou no lugar:")
        for qtd, esperado, retornado in confusoes:
            print(f"  {esperado}  ->  {retornado} : {qtd}x")
        print()

    pct_geral = 100 * acertos_total / pedidos_total if pedidos_total else 0
    print(f"RESUMO: {acertos_total}/{pedidos_total} frames corretos ({pct_geral:.1f}%)")
    print()

    return {
        "aluno": nome_grupo,
        "acertos": acertos_total,
        "pedidos": pedidos_total,
        "pct": pct_geral,
        "body_min": min(body_units) if body_units else None,
    }


def analisa(caminho: str):
    """Le um arquivo de log e separa os dados por nome de jogador.
    Se as linhas nao tiverem nome (logs antigos), agrupa tudo sob o nome do arquivo."""
    linhas = ler_arquivo(caminho)

    # jogador -> lista de (esperado, retornado, body_unit)
    por_jogador = defaultdict(list)

    for linha in linhas:
        m = LINE_RE.search(linha)
        if not m:
            continue
        esperado = normaliza_mov(m.group(1))
        retornado = normaliza_mov(m.group(2))
        try:
            bu = float(m.group(3))
        except ValueError:
            bu = None

        pm = PLAYER_RE.search(linha)
        jogador = pm.group(1).strip() if pm and pm.group(1).strip() else f"(sem nome) {caminho}"

        por_jogador[jogador].append((esperado, retornado, bu))

    if not por_jogador:
        print("=" * 60)
        print(f"ARQUIVO: {caminho}")
        print("=" * 60)
        print("  Nenhuma tentativa registrada neste arquivo.\n")
        return []

    print("#" * 60)
    print(f"ARQUIVO: {caminho}")
    print("#" * 60 + "\n")

    resumos = []
    for jogador in sorted(por_jogador.keys()):
        r = analisa_grupo(jogador, por_jogador[jogador])
        if r:
            resumos.append(r)
    return resumos


def main():
    args = sys.argv[1:]
    if args:
        arquivos = args
    else:
        arquivos = sorted(glob.glob("*.log"))

    if not arquivos:
        print("Nenhum arquivo .log encontrado. Passe o nome do arquivo como argumento,")
        print("ex.:  python analisar_log.py execucoes.log")
        return

    resumos = []
    for arq in arquivos:
        resumos.extend(analisa(arq))

    # comparacao final entre jogadores (util para menores x maiores)
    if len(resumos) > 1:
        print("#" * 60)
        print("COMPARACAO ENTRE JOGADORES")
        print("#" * 60)
        print(f"{'Aluno':<28}{'Acertos':>10}{'Taxa':>9}{'body_unit':>12}")
        for r in resumos:
            bu = f"{r['body_min']:.3f}" if r["body_min"] is not None else "-"
            print(
                f"{r['aluno'][:27]:<28}"
                f"{str(r['acertos']) + '/' + str(r['pedidos']):>10}"
                f"{r['pct']:>8.1f}%"
                f"{bu:>12}"
            )


if __name__ == "__main__":
    main()