# Books to Scrape - Web Scraper

Script de Web Scrapping desenvolvido como Etapa do processo seletivo no Estagio da FGV-IBRE

Coleta dados sobre os livros listados em [books.toscrape.com](https://books.toscrape.com): nome, preco e url

## Stack
- **Python3**
- **Requests** - coleta do HTML das paginas
- **BeautifulSoup4** - parsing e extracao dos dados do HTML
- **Pandas** - estruturacao dos dados e exportacao para tabela Excel (arquivo .xlsx)

## Como Rodar

1- Clonar o Repo:
```bash
   git clone https://github.com/MarquesMiguel/scrapping-fgv-PS.git
   cd scrapping-fgv-PS
```

2- Instalar as Dependencias:
```bash
   pip install -r requirements.txt
```

3- Executar o Script:
```bash
   python scrape.py
```
--> O arquivo 'itens.xlsx' sera gerado na root do projeto, contendo as colunas 'nome', 'preco', e 'url' para todos os livros

## Estrutura

scrape_all_books()  (orquestradora)
│
├── fetch_html(url)         → busca o HTML bruto da pagina
├── get_data(html, url)     → retorna os dados sobre o livro em formato de dict + a url da proxima pagina
│                              
├── build_df(books)         → constroi o DataFrame e normaliza os dados
│                              
└── export_excel(df)        → exporta o resultado final para itens.xlsx



