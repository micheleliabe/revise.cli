# Revise.cli

## Autor
Michel Eliabe Moreira Dias

## Suporte
Para qualquer dúvida ou sugestão, entre em contato através do email: micheldias.cloud@gmail.com

## Descrição da Aplicação
Revise.cli é uma ferramenta de linha de comando robusta e versátil, projetada para analisar e otimizar ambientes hospedados na AWS (Amazon Web Services). Com uma variedade de recursos, a aplicação visa facilitar a identificação de oportunidades de melhoria, especialmente no que diz respeito a custos e segurança.

## Funcionalidades
A seguir estão algumas das principais funcionalidades oferecidas pelo Revise.cli:

- **Localização de volumes GP2**
- **Identificação de elastic IPs não utilizados**
- **Identificação de volumes EBS Não utilizados**
- **Identificação de Volumes EBS em Instâncias EC2 Pausadas**
- **Verificação de bancos de dados RDS com acesso público ativado**
- **Localização de grupos de segurança com regras de entrada públicas**
- **Identificação de buckets S3 com bloqueio de acesso público desativado**
- **Identificação de snapshots antigos**

## Documentação
A documentação da aplicação está em desenvolvimento e ficará disponível em breve.

## Uso Básico
Para começar a utilizar o Revise.cli, siga os passos abaixo:

1. **Instalação**:
   - Clone o repositório git da aplicação.
   - Instale os pacotes necessários utilizando o comando `pip install -r requirements.txt`.

2. **Execução**:
   - Para obter recomendações para redução de custos em todas as regiões da AWS: `./revise aws costs`.
   - Para obter recomendações de segurança em todas as regiões da AWS: `./revise aws security`.
   - Para especificar regiões específicas, adicione a flag `--regions` seguida das regiões desejadas, por exemplo: `--regions "us-east-1 us-west-2"`.
   - Para obter recomendações específicas, utilize o comando `get` seguido do tipo de recomendação desejada. Por exemplo: `./revise aws get gp2-volumes`.

3. **Comandos Disponíveis para `get`**:
   - `gp2-volumes`: Identifica volumes do tipo GP2 que podem ser convertidos para GP3.
   - `volumes-on-stopped-instances`: Identifica volumes anexados em instâncias EC2 pausadas.
   - `detached-volumes`: Identifica volumes EBS não utilizados.
   - `detached-ips`: Identifica endereços IP elásticos não utilizados.
   - `old-snapshots`: Identifica snapshots antigos.
   - `public-egress-rules`: Identifica grupos de segurança com regras de entrada permitindo o acesso público.
   - `buckets-not-public-access-block`: Identifica buckets S3 com o bloqueio de acesso público desativado.
   - `rds-publicly-accessible`: Identifica bancos de dados RDS com a opção de liberar acesso público selecionada.

Explore os diferentes comandos disponíveis para otimizar seus recursos na AWS e garantir a segurança e eficiência do seu ambiente de nuvem.