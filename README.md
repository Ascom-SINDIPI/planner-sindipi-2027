# Planner SINDIPI 2027

Duas versões do mesmo calendário de conteúdo:

- **Versão interna (editável)** — publicada como Artifact no Claude, com balão de sugestão de conteúdo editável e salvamento automático para toda a equipe. Link já em uso pela equipe.
- **Versão pública (somente leitura)** — [`index.html`](index.html) deste repositório, pensada para ser hospedada no GitHub Pages. Mostra o mesmo calendário e as mesmas sugestões de conteúdo, mas sem edição (a edição continua sendo feita na versão interna).

Também incluído:

- [`planner_sindipi_2027.py`](planner_sindipi_2027.py) — script Python com todas as 64 publicações em formato de dados, com funções para exportar CSV e JSON.

## Como publicar `index.html` no GitHub Pages

1. Crie uma conta em [github.com/signup](https://github.com/signup), se ainda não tiver.
2. No canto superior direito do GitHub, clique em **+** → **New repository**.
   - Nome sugerido: `planner-sindipi-2027`
   - Marque **Public**
   - Clique em **Create repository**
3. Na página do repositório recém-criado, clique em **Add file → Upload files**.
4. Arraste o arquivo `index.html` (e opcionalmente este `README.md`) para a área de upload e clique em **Commit changes**.
5. Vá em **Settings → Pages** (menu lateral esquerdo).
6. Em **Build and deployment → Source**, selecione **Deploy from a branch**.
7. Em **Branch**, selecione `main` e a pasta `/ (root)`, depois **Save**.
8. Aguarde cerca de 1 minuto — o GitHub mostrará o link público, algo como:
   `https://SEU-USUARIO.github.io/planner-sindipi-2027/`

Esse link pode ser compartilhado com qualquer pessoa, sem necessidade de login no Claude.

## Atualizando o conteúdo público depois

Sempre que a versão interna mudar bastante, é só pedir para o Claude gerar um novo `index.html` atualizado e repetir o passo 3–4 (Add file → Upload files, escolhendo "substituir" o arquivo existente).
