# Back-end – Sistema de RH e Folha de Pagamento

Back-end em **Python + Flask + SQLite** feito a partir da *Especificação de Requisitos v1.0* (GTI 4º período).
Cobre a **Etapa 1** (login, perfis, filiais, colaboradores, histórico e logs) e o **motor de cálculo** da folha
(INSS, IRRF, horas extras, DSR, faltas, VT, VA, FGTS e férias). Dinheiro sempre em `Decimal`.

## Como rodar
```bash
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py init-db
python manage.py criar-usuario --nome "Maria" --email maria@empresa.com --perfil RH
python manage.py seed-demo            # opcional: filiais e colaboradores de exemplo
python run.py                         # http://localhost:5000
python -m unittest discover -s tests -t .    # 34 testes
```
Variáveis opcionais: `SECRET_KEY` (troque em produção), `DATABASE`, `TOKEN_HORAS`, `CORS_ORIGIN`.

## Perfis (seção 4)
`RH` cadastra e calcula · `DIRETORIA` consulta e vê logs · `ADMIN` gerencia usuários e vê logs.

## Endpoints (`Authorization: Bearer <token>`)
| Método | Rota | Perfis |
|---|---|---|
| POST | `/api/auth/login` | público |
| GET | `/api/auth/me` | logado |
| GET/POST/PATCH | `/api/usuarios` | ADMIN |
| GET | `/api/filiais` | RH, DIRETORIA |
| POST/PUT | `/api/filiais` · `/api/filiais/<id>` | RH |
| GET | `/api/colaboradores?busca=&filial_id=&situacao=` | RH, DIRETORIA |
| POST | `/api/colaboradores` | RH |
| GET | `/api/colaboradores/<id>` (gera log de consulta) | RH, DIRETORIA |
| PUT | `/api/colaboradores/<id>` | RH |
| DELETE | `/api/colaboradores/<id>` (**inativa**, não exclui) | RH |
| POST | `/api/colaboradores/<id>/reativar` | RH |
| GET | `/api/colaboradores/<id>/historico` · `/pendencias` | RH, DIRETORIA |
| GET | `/api/logs?usuario_email=&entidade=&acao=&de=&ate=` | DIRETORIA, ADMIN |
| GET | `/api/parametros?competencia=2026-10` | RH, DIRETORIA |
| POST | `/api/simulacao/folha` · `/api/simulacao/ferias` | RH |

## Estrutura
```
app/calculo.py        motor de cálculo (funções puras)
app/parametros.py     parâmetros legais 2026 com vigência (RN-01)
app/routes_*.py       rotas · app/security.py login/JWT/perfis · app/db.py tabelas e log
tests/                exemplos da seção 8 e cenários da seção 10
```

## Regras implementadas
RN-01 (parâmetros com vigência) · RN-02 (memória de cálculo) · RN-03 (arredondamento por verba) ·
RN-05/RN-10 (pendências do colaborador) · RN-07 (histórico) · RN-11 a RN-14 (CPF único e válido,
inativar, dados proibidos) · RN-21 a RN-24 · RN-30 a RN-33 · RN-41 · RN-50/RN-51 · RNF-01 a RNF-03
(senha com hash, sessão com expiração, log imutável por trigger do banco).

## Dúvidas para o GTI 4º período (a spec não define; não inventamos regra)
1. **Faltas e base de INSS/IRRF:** seguimos a spec ao pé da letra (falta é "demais desconto", etapa 6, depois dos impostos). Na prática as faltas costumam reduzir a base. Confirmar.
2. **DSR (RN-31):** a fórmula fala em "total de horas extras"; aplicamos sobre o **valor em R$** das horas extras. Confirmar.
3. **Perda do DSR por falta (RN-33):** sem fórmula na spec, **não implementado**.
4. **Abono pecuniário (RN-43):** a spec não diz se o abono recebe o 1/3. **Não implementado.**
5. **Proporcional de admitidos/desligados (RN-20)** e **afastamentos (RN-34/P-03):** hipóteses, **não implementados**.
6. **Jornada:** aceitamos de 1 a 44 h semanais (a spec só fala em 44).
7. **Parâmetros legais** têm fim em 31/12/2026; sem tabela nova, folha de 2027 dá erro de "sem vigência" (de propósito).
8. **Quem edita parâmetros** não está definido; por ora entram pelo seed/banco.

## Falta fazer (Etapas 2 a 4)
Lançamento de eventos, folha persistida com fechamento/reabertura, férias com saldo e alertas, documentos e exames,
contracheque e relatórios em PDF/Excel, cifragem de dados de saúde (RNF-04), backup (RNF-05) e retenção (RN-56).
