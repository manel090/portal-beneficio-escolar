# Apoio Brasil — versão de preparação

## O que foi preparado
- Página de apresentação de serviço particular de orientação.
- Cadastro antes da etapa de pagamento.
- Tela final com valor de R$ 49,90 e opções Pix/cartão marcadas como em configuração.
- Políticas iniciais de privacidade, termos e cancelamento/reembolso.
- Cadastro guarda nome, e-mail e localização opcional em SQLite.
- CPF não é solicitado, pois não é necessário para comprar o material de orientação.

## Atenção antes de publicar
1. Esta versão NÃO realiza cobranças. A Beehive ainda não está integrada.
2. Configure um canal de atendimento comercial real nas páginas legais antes de aceitar pagamentos.
3. Revise os textos legais com os dados do responsável pelo serviço.
4. Configure `SECRET_KEY` como variável de ambiente forte na Render.
5. Configure armazenamento persistente para o banco SQLite ou migre para banco gerenciado. O disco padrão de serviços web da Render pode ser efêmero; não use esta configuração para guardar cadastros reais sem persistência.
6. Não solicite nem armazene CPF se não houver necessidade comprovada.
7. O conteúdo de orientação deve ser correto, atualizado e apontar para canais oficiais. Não prometa aprovação ou recebimento de benefícios.

## Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Root Directory: em branco se os arquivos estiverem na raiz do repositório.

## Variáveis sugeridas
- `SECRET_KEY`: gere uma chave aleatória forte e mantenha-a privada.
- `DATABASE_PATH`: caminho do banco em disco persistente, quando configurado.
