# Ministério Público do Trabalho (MPT)

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Trabalho. O site com as informações da **Remuneração de Todos os Membros Ativos** e das **Indenizações e Remunerações Temporárias** pode ser acessado **[aqui](https://mpt.mp.br/MPTransparencia/)**.

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, no formato ODS e XLS, sendo cada uma referente a uma dessas categorias.

## Como usar

### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 
 - A imagem do contêiner do coletor poderá ser construída ou baixada. 

 - Construção da imagem:

     ```sh
    $ docker build --pull --rm -t parsermpt:latest .
     ```
 - Download da imagem:

    ```sh
    $ docker pull ghcr.io/dadosjusbr/parser-mpt:main
    ```
 - Execução:

    ```sh
    $ docker run -i --rm -e YEAR=2021 -e MONTH=03 -e OUTPUT_FOLDER=/output --name parsermpt --mount type=bind,src=/tmp/parsermpt,dst=/output parsermpt
    ```

### Execução sem Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório mpma, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.8+](https://www.python.org/downloads/) instalado, bem como o chromedriver compatível com a versão do seu Google Chrome. Ele pode ser baixado [aqui](https://chromedriver.chromium.org/downloads).

    ```sh
    $ YEAR=2018 MONTH=03 DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:

   ```sh
    $ pip install -r requirements.txt
   ```